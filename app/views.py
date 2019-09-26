# views.py
import os
from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.repository.repository import Repository
from franz.openrdf.query.query import QueryLanguage

from flask import render_template

from app import app

@app.route('/')
def index():
	AGRAPH_HOST = os.environ.get('AGRAPH_HOST')
	AGRAPH_PORT = int(os.environ.get('AGRAPH_PORT', '10035'))
	AGRAPH_USER = os.environ.get('AGRAPH_USER')
	AGRAPH_PASSWORD = os.environ.get('AGRAPH_PASSWORD')

	server = AllegroGraphServer(host=AGRAPH_HOST, port=AGRAPH_PORT, user=AGRAPH_USER, password=AGRAPH_PASSWORD)
	catalog = server.openCatalog()
	#print(catalog.getRepository("lattes", Repository.ACCESS).getConnection().isEmpty())
	#print(catalog.getRepository("lattes", Repository.ACCESS).getConnection().listIndices())

	print("Available catalogs:")
	for cat_name in server.listCatalogs():
		if cat_name is None:
			print('  - <root catalog>')
		else:
			print('  - ' + str(cat_name))


	print("Available repositories in catalog '%s':" % catalog.getName())
	for repo_name in catalog.listRepositories():
		print('  - ' + repo_name)

	mode = Repository.OPEN # opens an existing repository, or throws an exception if the repository is not found.
	repository_lattes21 = catalog.getRepository('lattes21', mode)
	connection_lattes21 = repository_lattes21.getConnection()
	print('Repository %s is up!' % repository_lattes21.getDatabaseName())
	print('It contains %d statement(s).' % connection_lattes21.size())



	'''query_string = "SELECT ?s ?p ?o  WHERE { ?s dc:language ?o . }"
	tuple_query = conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
	result = tuple_query.evaluate()
	with result:
		for binding_set in result:
			s = binding_set.getValue("s")
			p = binding_set.getValue("p")
			o = binding_set.getValue("o")
			print("%s %s %s" % (s, p, o))'''


	return render_template("index.html")

@app.route('/about')
def about():
	return render_template("about.html")