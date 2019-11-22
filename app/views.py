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

def searchInRepository(repository, string_buscada, resultsDic, numRepo):
	lattesRep = repository
	queryString = " SELECT ?author_name ?nOcorrencias " \
	" WHERE { ?s foaf:name ?author_name; ?univOrigem 'PUC-Rio' . " \
	" { SELECT ?author_name (COUNT(DISTINCT ?s) AS ?nOcorrencias) " \
	" WHERE{ ?s dc:title ?title; dc:creator ?author. " \
	" ?author foaf:name ?author_name ." \
	" filter (regex(fn:lower-case(str(?title)), fn:lower-case('" + string_buscada + "'))) . }" \
	"  GROUP BY ?author_name }} ORDER BY DESC(?nOcorrencias)"

	result = lattesRep.executeTupleQuery(queryString)
	#nResults[numRepo] = result.rowCount() # number of elements in the result
	for binding_set in result:
		authorName = str(binding_set.getValue("author_name"))
		nOcorrencias = int(str(binding_set.getValue("nOcorrencias")).replace('"^^<http://www.w3.org/2001/XMLSchema#integer>',"").strip('"'))
		authorName=authorName[1:-1] # fora os " "
		resultsDic.update({authorName : [nOcorrencias,numRepo]})

	lattesRep.close()

def mergeDict(dict1, dict2):
   ''' Merge dictionaries and keep values of common keys in list'''
   dict3 = {**dict1, **dict2}
   for key, value in dict3.items():
       if key in dict1 and key in dict2:
               dict3[key] = [value , dict1[key]]
 
   return dict3


@app.route('/', methods=['GET','POST'])
def index():

	form = SearchForm()

	if request.method == 'POST':
		string_buscada = form.busca.data

		resultsLattes1 = {}
		resultsLattes21= {}
		resultsLattes22= {}
		resultsLattes23 = {}

		#nResults = [0,0,0,0]

		try:
			t1 = threading.Thread(target=searchInRepository,args=(connection.lattes, string_buscada,resultsLattes1, 0))
			t21 = threading.Thread(target=searchInRepository,args=(connection.lattes21, string_buscada,resultsLattes21, 1))
			t22 = threading.Thread(target=searchInRepository,args=(connection.lattes22, string_buscada,resultsLattes22, 2))
			t23 = threading.Thread(target=searchInRepository,args=(connection.lattes23, string_buscada,resultsLattes23, 3))

			threads = [t1,t21,t22,t23]

			for t in threads:
				t.start()

			for t in threads:
				t.join()

			#resultsFinal = mergeDict(resultsLattes1, resultsLattes21)
			resultsFinal = {**resultsLattes1, **resultsLattes21, **resultsLattes22, **resultsLattes23}

			resultsFinal = sorted(resultsFinal.items(), key=operator.itemgetter(1,0), reverse=True)
			print(resultsFinal)

			return render_template("/index.html", form=form, dados=resultsFinal, busca=string_buscada, nResultados=len(resultsFinal))#, pagination=pagination)
		
		except Exception as e:
			print("Exception : ", e)
			return render_template("error.html")

	return render_template("/index.html", form=form)


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
		elif nRepositorio ==2:
			lattesRep = connection.lattes22
		else:
			lattesRep = connection.lattes23

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
		resultsDic = {}

		artigos = {}
		livros = {}
		teses = {}
		capitulos = {}
		documentos = {}

		for binding_set in resultados:
			tipo = str(binding_set.getValue("Tipo"))
			tipo = tipo.replace('http://purl.org/ontology/bibo/',"").strip('"')
			data = int(str(binding_set.getValue("data")).strip('"'))
			title = str(binding_set.getValue("Title"))[1:-1]
			autor = str(binding_set.getValue("author2_citationName"))[1:-1].split(';')[0]

			if tipo == 'Article' :
				if (title,data) in artigos:
					artigos[title,data].append(autor)
				else:
					artigos[title,data] = [autor]
				#artigos.setdefault((title,data),[]).append(autor)
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
			else:
				if (title,data) in documentos:
					documentos[title,data].append(autor)
				else:
					documentos[title,data] = [autor]

		resultsDic['artigos']= artigos
		resultsDic['livros']= livros
		resultsDic['teses']= teses
		resultsDic['capitulos']= capitulos
		resultsDic['documentos']= documentos
		
		lattesRep.close()
		return render_template("about.html", pessoa=pessoa, busca=busca, dados=resultsDic)
	
	except Exception as e:
		print("Exception : ", e)
		return render_template("error.html")




@app.route('/error')
def testes():

	return render_template("error.html")