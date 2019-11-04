# views.py
from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.repository.repository import Repository
from franz.openrdf.query.query import QueryLanguage
from franz.openrdf.connect import ag_connect

from flask import render_template, request

from app import app

from . import connection
from .forms import SearchForm

@app.route('/', methods=['GET','POST'])
def index():

	form = SearchForm()

	if request.method == 'POST':
		string_buscada = form.busca.data

		with connection.lattes21 as lattes21:
			
			queryString = " SELECT ?author_name (COUNT(?s) AS ?nOcorrencias) " \
			" WHERE{ ?s dc:title ?title; dc:creator ?author. " \
			" ?author foaf:name ?author_name ." \
			" filter (regex(fn:lower-case(str(?title)), fn:lower-case('" + string_buscada + "'))) . }" \
			"  GROUP BY ?author_name ORDER BY DESC(?nOcorrencias)"

			res21 = lattes21.executeTupleQuery(queryString)

			nResultados=res21.rowCount() # number of elements in the result

			resultsDic ={}
			for binding_set in res21:
				authorName = str(binding_set.getValue("author_name"))
				nOcorrencias = int(str(binding_set.getValue("nOcorrencias")).replace('"^^<http://www.w3.org/2001/XMLSchema#integer>',"").strip('"')) #.strip('"^^<http://www.w3.org/2001/XMLSchema#integer>')
				authorName=authorName[1:-1] # fora os " "
				#results.append(authorName)
				resultsDic.update({authorName : nOcorrencias})

		return render_template("/index.html", form=form, dados=resultsDic, busca=string_buscada, nResultados=nResultados)

	return render_template("/index.html", form=form)


@app.route('/about')
def about():
	pessoa = request.args.get('pessoa')
	busca = request.args.get('busca')

	with connection.lattes21 as lattes21:

		queryString = " SELECT DISTINCT (str(?tipo) as ?Tipo) (str(?title) as ?Title) " \
		" WHERE{ ?s dc:title ?title; rdf:type ?tipo ; dc:creator ?author. " \
		" ?author foaf:name ?author_name ." \
		" filter (regex(fn:lower-case(str(?title)), fn:lower-case('" + busca + "'))) . " \
		" filter (regex(fn:lower-case(str(?author_name)), fn:lower-case('" + pessoa + "'))) . }" \
		" ORDER BY ?tipo "

		res21 = lattes21.executeTupleQuery(queryString)

		resultsDic={}

		artigos=[]
		livros=[]
		teses=[]
		capitulos=[]
		documentos=[]

		for binding_set in res21:
			tipo = str(binding_set.getValue("Tipo"))
			tipo = tipo.replace('http://purl.org/ontology/bibo/',"").strip('"')

			if tipo == 'Article' :
				artigos.append(str(binding_set.getValue("Title"))[1:-1])
			elif tipo == 'Book' :
				livros.append(str(binding_set.getValue("Title"))[1:-1])
			elif tipo == 'Thesis' :
				teses.append(str(binding_set.getValue("Title"))[1:-1])
			elif tipo == 'Chapter':
				capitulos.append(str(binding_set.getValue("Title"))[1:-1])
			else:
				documentos.append(str(binding_set.getValue("Title"))[1:-1])


		resultsDic['artigos']= artigos
		resultsDic['livros']= livros
		resultsDic['teses']= teses
		resultsDic['capitulos']= capitulos
		resultsDic['documentos']= documentos

	return render_template("about.html", pessoa=pessoa, busca=busca, dados=resultsDic)



@app.route('/testes')
def testes():

	return render_template("about.html")