# views.py
import os
from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.repository.repository import Repository
from franz.openrdf.query.query import QueryLanguage
from franz.openrdf.connect import ag_connect

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


	# Nao olvidar de liberar as conexoes
	connection_lattes21.close()
	repository_lattes21.shutDown()

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

	with ag_connect('lattes21') as connection_lattes21:
		print('Connected to repository lattes21')
		print('Size of statements:', connection_lattes21.size())

		# Trying queries
		query_string = "SELECT ?s ?p ?o  WHERE {?s dc:language ?o .} LIMIT 20"
		tuple_query = connection_lattes21.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
		result = tuple_query.evaluate()
		with result:
			print("s,             p,             o:")
			for binding_set in result:
				s = binding_set.getValue("s")
				p = binding_set.getValue("p")
				o = binding_set.getValue("o")
				print("%s %s %s" % (s, p, o))


		print("\n\n\n")
		print('SPARQL filter match')
		connection_lattes21.executeTupleQuery(query_string, output=True)  # Shows directly in console

		print("\n\n\n")
		print('Other type of query')
		connection_lattes21.executeTupleQuery('''SELECT ?s ?o WHERE {?s ?p ?o .
			filter (fn:lower-case(str(?o)) = "português")} LIMIT 20''', output=True)


		print("\n\n\n")
		print('Ordered languages')
		connection_lattes21.executeTupleQuery('''SELECT DISTINCT ?o WHERE {?s dc:language ?o .} ORDER BY ?o''', output=True)


		print("\n\n\n")
		# Trying statements
		print('Statements where object = "Português"')
		portugues = connection_lattes21.createLiteral("Português") # Para criar subject é createURI()
		statements = connection_lattes21.getStatements(subject=None, predicate=None, object=portugues, limit=20) # It is a RepositoryResult object
		with statements:
			#statements.enableDuplicateFilter()
			for statement in statements:
				print(statement)



	return render_template("about.html")