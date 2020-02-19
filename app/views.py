# views.py
from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.repository.repository import Repository
from franz.openrdf.query.query import QueryLanguage
from franz.openrdf.connect import ag_connect
from flask import render_template, request
from app import app
from . import connection
from .forms import SearchForm
import operator
import threading
from collections import defaultdict

@app.route('/', methods=['GET','POST'])
def index():
	form = SearchForm()

	if request.method == 'POST':
		string_buscada = form.busca.data
		artigos = form.artigos.data
		livros = form.livros.data
		teses = form.teses.data
		capitulos = form.capitulos.data

		resultsLattes1 = {}
		resultsLattes21= {}
		resultsLattes22= {}

		try:
			t1 = threading.Thread(target=searchInRepository, args=(connection.lattes, string_buscada, resultsLattes1, 0, artigos, livros, teses, capitulos))
			t21 = threading.Thread(target=searchInRepository, args=(connection.lattes21, string_buscada, resultsLattes21, 1, artigos, livros, teses, capitulos))
			t22 = threading.Thread(target=searchInRepository, args=(connection.lattes22, string_buscada, resultsLattes22, 2, artigos, livros, teses, capitulos))

			threads = [t1,t21,t22]

			for t in threads:
				t.start()

			for t in threads:
				t.join()

			results = {**resultsLattes1, **resultsLattes21, **resultsLattes22}
			resultsFiltered = {k: v for k, v in results.items() if v[0] != 0}
			resultsFinal = sorted(resultsFiltered.items(), key=operator.itemgetter(1,0), reverse=True)

			return render_template("/index.html", form=form, dados=resultsFinal, busca=string_buscada, nResultados=len(resultsFinal))

		except Exception as e:
			print("Exception : ", e)
			return render_template("error.html")

	return render_template("/index.html", form=form)

def searchInRepository(repository, string_buscada, resultsDic, numRepo, artigos, livros, teses, capitulos):
	lattesRep = repository

	incluidos = list()
	incluidos.append("<http://xmlns.com/foaf/0.1/Document>")

	if artigos != False:	
		incluidos.append("<http://purl.org/ontology/bibo/Article>") 
	if livros != False:
		incluidos.append("<http://purl.org/ontology/bibo/Book>") 
	if teses != False:
		incluidos.append("<http://purl.org/ontology/bibo/Thesis>") 
	if capitulos != False:
		incluidos.append("<http://purl.org/ontology/bibo/Chapter>") 

	incluidos = ','.join(incluidos)	

	queryString = " SELECT ?author_name (COUNT(*) AS ?nOcorrencias) " \
	" { " \
	" {SELECT ?author_name ?bio " \
	" WHERE { ?s bio:biography ?bio; foaf:name ?author_name. " \
	" filter (regex(fn:lower-case(str(?bio)), fn:lower-case('"+ string_buscada +"'))) .}} " \
	" UNION " \
	" {SELECT DISTINCT ?author_name (str(?title) as ?Title) " \
	" WHERE { ?s dc:title ?title; dc:creator ?author; rdf:type ?prod_type. " \
	" ?author foaf:name ?author_name . " \
	" filter (regex(fn:lower-case(str(?title)), fn:lower-case('"+ string_buscada +"'))) . " \
	" filter (?prod_type IN ("+ incluidos +")) .}} " \
	" } " \
	" GROUP BY ?author_name " \
	" ORDER BY DESC(?nOcorrencias) " \

	result = lattesRep.executeTupleQuery(queryString)
	if numRepo == 0:
		tipo = 'Aluno'
	else:
		tipo = 'Professor'

	for binding_set in result:
		authorName = str(binding_set.getValue("author_name"))
		nOcorrencias = int(str(binding_set.getValue("nOcorrencias")).replace('"^^<http://www.w3.org/2001/XMLSchema#integer>',"").strip('"'))
		authorName=authorName[1:-1] # fora os " "
		resultsDic.update({authorName : [nOcorrencias, numRepo, tipo]})

	lattesRep.close()

def mergeDict(dict1, dict2):
   ''' Merge dictionaries and keep values of common keys in list'''
   dict3 = {**dict1, **dict2}
   for key, value in dict3.items():
       if key in dict1 and key in dict2:
               dict3[key] = [value , dict1[key]]
 
   return dict3


@app.route('/about')
def about():

	pessoa = request.args.get('pessoa')
	busca = request.args.get('busca')
	nRepositorio = int(request.args.get('nRepositorio'))

	try:
		if nRepositorio == 0:
			lattesRep = connection.lattes
		elif nRepositorio ==1:
			lattesRep = connection.lattes21
		else:
			lattesRep = connection.lattes22

		resultsDic = {}

		queryStringInfos = "SELECT ?id ?p ?o " \
		" WHERE{ ?s dc:title ?title; bibo:identifier ?id; dc:creator ?author. ?author ?p ?o. " \
		" filter (regex(fn:lower-case(str(?title)), fn:lower-case('CV Lattes de'))) . " \
		" filter (regex(fn:lower-case(str(?title)), fn:lower-case('"+ pessoa +"'))) . }  " \

		site = {}
		email = {}
		homepage = {}
		mbox = {}
		biography = {}

		infos = lattesRep.executeTupleQuery(queryStringInfos)
		for binding_set in infos:
			idp = str(binding_set.getValue("id")).strip('"')
			p = str(binding_set.getValue("p"))
			conteudo = str(binding_set.getValue("o")).strip('"')
			if p == '<site>':
				site.setdefault(idp,[]).append(conteudo)
			elif p == '<email>':
				email.setdefault(idp,[]).append(conteudo)
			elif p == '<http://xmlns.com/foaf/0.1/homepage>':
				homepage.setdefault(idp,[]).append(conteudo)
			# elif p == 'foaf:mbox':
			# 	mbox[idp,p].append(conteudo)
			elif p == '<http://purl.org/vocab/bio/0.1/biography>':
				biography.setdefault(idp,[]).append(conteudo)

		#bio = [[value for key, value in biography.items()] for biography in resultsDic]
		
		l=[]
		[l.extend([k,v]) for k,v in biography.items()]

		resultsDic['site']= site
		resultsDic['email']= email
		resultsDic['homepage']= homepage
		# resultsDic['mbox']= mbox
		resultsDic['biography']= l

		queryString = " SELECT DISTINCT (str(?tipo) as ?Tipo) " \
		"(replace(replace(replace(str(?title),'ê','e'),'â','a'),'ã','a') as ?Title)  ?data ?author2_citationName " \
		" WHERE{ ?s dc:title ?title; rdf:type ?tipo ; dcterms:issued ?data; dc:creator ?author. " \
		" ?author foaf:name ?author_name ." \
		" {SELECT ?title ?author2_citationName WHERE { ?s dc:title ?title; dc:creator ?author2_id . " \
		" ?author2_id foaf:citationName ?author2_citationName . } }" \
		" filter (regex(fn:lower-case(str(?title)), fn:lower-case('" + busca + "'))) . " \
		" filter (regex(fn:lower-case(str(?author_name)), fn:lower-case('" + pessoa + "'))) . }" \
		" ORDER BY ?Title "

		resultados = lattesRep.executeTupleQuery(queryString)

		artigos = {}
		livros = {}
		teses = {}
		capitulos = {}

		for binding_set in resultados:
			tipo = str(binding_set.getValue("Tipo"))
			tipo = tipo.replace('http://purl.org/ontology/bibo/',"").strip('"')
			data = int(str(binding_set.getValue("data")).strip('"')[-4:])
			title = str(binding_set.getValue("Title"))[1:-1]
			autor = str(binding_set.getValue("author2_citationName"))[1:-1].split(';')[0]

			if tipo == 'Article' :
				if (title,data) in artigos:
					artigos[title,data].append(autor)
				else:
					artigos[title,data] = [autor]
			elif tipo == 'Book' :
				if (title,data) in livros:
					livros[title,data].append(autor)
				else:
					livros[title,data] = [autor]
			elif tipo == 'Thesis' :
				if (title,data) in teses:
					teses[title,data].append(autor)
				else:
					teses[title,data] = [autor]
			elif tipo == 'Chapter':
				if (title,data) in capitulos:
					capitulos[title,data].append(autor)
				else:
					capitulos[title,data] = [autor]

		queryStringLattes = " SELECT DISTINCT (str(?tipo) as ?Tipo) " \
		"(replace(replace(replace(str(?title),'ê','e'),'â','a'),'ã','a') as ?Title)  ?data ?author2_citationName " \
		" WHERE{ ?s dc:title ?title; rdf:type ?tipo ; dcterms:issued ?data; dc:creator ?author. " \
		" ?author foaf:name ?author_name ." \
		" {SELECT ?title ?author2_citationName WHERE { ?s dc:title ?title; dc:creator ?author2_id . " \
		" ?author2_id foaf:citationName ?author2_citationName . } }" \
		" filter (regex(fn:lower-case(str(?title)), fn:lower-case('" + pessoa + "'))) . " \
		" filter (regex(fn:lower-case(str(?author_name)), fn:lower-case('" + pessoa + "'))) . }" \
		" ORDER BY ?Title "

		documentos = {}

		lattespessoa = lattesRep.executeTupleQuery(queryStringLattes)
		for binding_set in lattespessoa:
			data = int(str(binding_set.getValue("data")).strip('"')[-4:])
			title = str(binding_set.getValue("Title"))[1:-1]
			autor = str(binding_set.getValue("author2_citationName"))[1:-1].split(';')[0]
			if (title,data) in artigos:
				documentos[title,data].append(autor)
			else:
				documentos[title,data] = [autor]

		resultsDic['artigos']= artigos
		resultsDic['livros']= livros
		resultsDic['teses']= teses
		resultsDic['capitulos']= capitulos
		resultsDic['documentos']= documentos
		
		lattesRep.close()
		return render_template("about.html", pessoa=pessoa, busca=busca, dados=resultsDic, idp=idp)
	
	except Exception as e:
		print("Exception : ", e)
		return render_template("error.html")


@app.route('/error')
def testes():
	return render_template("error.html")