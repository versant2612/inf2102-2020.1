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

@app.route('/', methods=['GET','POST'])
def index():

	form = SearchForm()

	if request.method == 'POST':
		string_buscada = form.busca.data

		resultsDic ={}

		lattesRep = connection.lattes
		lattes21Rep = connection.lattes21
		lattes22Rep = connection.lattes22
		lattes23Rep = connection.lattes23

		repositorios = [lattesRep,lattes21Rep,lattes22Rep,lattes23Rep]
		nResultados = 0

		for numRepo in range(0,4):
			lattesUsed = repositorios[numRepo]
			#with connection.lattes as lattesRep:
			queryString = " SELECT ?author_name (COUNT(?s) AS ?nOcorrencias) " \
			" WHERE{ ?s dc:title ?title; dc:creator ?author. " \
			" ?author foaf:name ?author_name ." \
			" filter (regex(fn:lower-case(str(?title)), fn:lower-case('" + string_buscada + "'))) . }" \
			"  GROUP BY ?author_name ORDER BY DESC(?nOcorrencias)"

			result = lattesUsed.executeTupleQuery(queryString)

			nResultados += result.rowCount() # number of elements in the result

			for binding_set in result:
				authorName = str(binding_set.getValue("author_name"))
				nOcorrencias = int(str(binding_set.getValue("nOcorrencias")).replace('"^^<http://www.w3.org/2001/XMLSchema#integer>',"").strip('"')) #.strip('"^^<http://www.w3.org/2001/XMLSchema#integer>')
				authorName=authorName[1:-1] # fora os " "
					#results.append(authorName)
				resultsDic.update({authorName : [nOcorrencias,numRepo]})

		lattesRep.close()
		lattes21Rep.close()
		lattes22Rep.close()
		lattes23Rep.close()

		return render_template("/index.html", form=form, dados=resultsDic, busca=string_buscada, nResultados=nResultados)

	return render_template("/index.html", form=form)


@app.route('/about')
def about():
	pessoa = request.args.get('pessoa')
	busca = request.args.get('busca')
	nRepositorio = int(request.args.get('nRepositorio'))

	if nRepositorio == 0:
		lattesRep = connection.lattes
	elif nRepositorio ==1:
		lattesRep = connection.lattes21
	elif nRepositorio ==2:
		lattesRep = connection.lattes22
	else:
		lattesRep = connection.lattes23

	#repositorios = [lattesRep,lattes21Rep,lattes22Rep,lattes23Rep]

	#lattesUsed = repositorios[nRepositorio]

	queryString = " SELECT DISTINCT (str(?tipo) as ?Tipo) " \
	"(replace(replace(replace(str(?title),'ê','e'),'â','a'),'ã','a') as ?Title) " \
	" WHERE{ ?s dc:title ?title; rdf:type ?tipo ; dc:creator ?author. " \
	" ?author foaf:name ?author_name ." \
	" filter (regex(fn:lower-case(str(?title)), fn:lower-case('" + busca + "'))) . " \
	" filter (regex(fn:lower-case(str(?author_name)), fn:lower-case('" + pessoa + "'))) . }" \
	" ORDER BY ?Title "

	resultados = lattesRep.executeTupleQuery(queryString)

	resultsDic={}

	artigos=[]
	livros=[]
	teses=[]
	capitulos=[]
	documentos=[]

	for binding_set in resultados:
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

	lattesRep.close()
	#lattes21Rep.close()
	#lattes22Rep.close()
	#lattes23Rep.close()

	return render_template("about.html", pessoa=pessoa, busca=busca, dados=resultsDic)



@app.route('/testes')
def testes():

	return render_template("about.html")