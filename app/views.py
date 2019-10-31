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
			print(string_buscada)

			# print('Repository lattes is up!, It contains %d statement(s).' % lattes.size())
			print('Repository lattes21 is up!, It contains %d statement(s).' % lattes21.size())


			#fedRepository = server.openFederated([lattes, lattes21])
			#print('Federated repository is up!, It contains %d statement(s).' % fedRepository.size())
			queryString = "PREFIX type:<http://purl.org/ontology/bibo/>  " \
			" SELECT DISTINCT (UCASE(str(?author_name)) as ?names) " \
			" WHERE {?s ?p ?type; dc:language 'Português'; dc:creator ?author; dc:title ?title . "\
			" ?author foaf:name ?author_name. filter (regex(fn:lower-case(str(?title)), fn:lower-case('" + string_buscada + "'))) . }" \
			" ORDER BY ?author_name"

			# print("Lattes:")
			# res = lattes.executeTupleQuery(queryString)
			# for binding_set in res:
			# 	conta = binding_set.getValue("conta")
			# 	print("%s" % (conta))


			print("\n\n\n")
			print("Lattes21:")
			res21 = lattes21.executeTupleQuery(queryString)

			nResultados=res21.rowCount() # number of elements in the result

			results=[]
			for binding_set in res21:
				#conta = binding_set.getValue("conta")
				authorName = str(binding_set.getValue("names"))
				authorName=authorName[1:-1] # fora os " "
				results.append(authorName)
				print("%s" % (authorName))

		return render_template("/index.html", form=form, dados=results, busca=string_buscada, nResultados=nResultados)


	# server = AllegroGraphServer(host=connection.AGRAPH_HOST, port=connection.AGRAPH_PORT, user=connection.AGRAPH_USER, password=connection.AGRAPH_PASSWORD)
	# catalog = server.openCatalog()

	# print("Available catalogs:")
	# for cat_name in server.listCatalogs():
	# 	if cat_name is None:
	# 		print('  - <root catalog>')
	# 	else:
	# 		print('  - ' + str(cat_name))


	# print("Available repositories in catalog '%s':" % catalog.getName())
	# for repo_name in catalog.listRepositories():
	# 	print('  - ' + repo_name)

	# mode = Repository.OPEN # opens an existing repository, or throws an exception if the repository is not found.
	# repository_lattes21 = catalog.getRepository('lattes21', mode)
	# connection.lattes21 = repository_lattes21.getConnection()
	# print('Repository %s is up!' % repository_lattes21.getDatabaseName())
	# print('It contains %d statement(s).' % connection.lattes21.size())


	# # Nao olvidar (esquecer kkkk) de liberar as conexoes
	# connection.lattes21.close()
	# repository_lattes21.shutDown()

	# '''query_string = "SELECT ?s ?p ?o  WHERE { ?s dc:language ?o . }"
	# tuple_query = conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
	# result = tuple_query.evaluate()
	# with result:
	# 	for binding_set in result:
	# 		s = binding_set.getValue("s")
	# 		p = binding_set.getValue("p")
	# 		o = binding_set.getValue("o")
	# 		print("%s %s %s" % (s, p, o))'''

	#lattes21
	#AQUIIIIIIIII
	# print('Connected to repository lattes21')
	# print('Size of statements:', connection.lattes21.size())

	# # Trying queries
	# query_string = "SELECT ?s ?p ?o  WHERE {?s dc:language ?o .} LIMIT 20"
	# tuple_query = connection.lattes21.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
	# result = tuple_query.evaluate()
	# with result:
	# 	print("s,             p,             o:")
	# 	for binding_set in result:
	# 		s = binding_set.getValue("s")
	# 		p = binding_set.getValue("p")
	# 		o = binding_set.getValue("o")
	# 		print("%s %s %s" % (s, p, o))
	#AQUI

	# print("\n\n\n")
	# print('SPARQL filter match')
	# connection.lattes21.executeTupleQuery(query_string, output=True)  # Shows directly in console

	# print("\n\n\n")
	# print('Other type of query')
	# connection.lattes21.executeTupleQuery('''SELECT ?s ?o WHERE {?s ?p ?o .
	# 	filter (fn:lower-case(str(?o)) = "português")} LIMIT 20''', output=True)


	# print("\n\n\n")
	# print('Ordered languages')
	# connection.lattes21.executeTupleQuery('''SELECT DISTINCT ?o WHERE {?s dc:language ?o .} ORDER BY ?o''', output=True)


	#AQUI
	# print("\n\n\n")
	# # Trying statements
	# print('Statements where object = "Português"')
	# portugues = connection.lattes21.createLiteral("Português") # Para criar subject é createURI()
	# statements = connection.lattes21.getStatements(subject=None, predicate=None, object=portugues, limit=20) # It is a RepositoryResult object
	# with statements:
	# 	#statements.enableDuplicateFilter()
	# 	for statement in statements:
	# 		print(statement)



	return render_template("/index.html", form=form)

@app.route('/about')
def about():

	with connection.lattes21:
		print('Connected to repository lattes21')
		print('Size of statements:', connection.lattes21.size())

		# Trying queries
		query_string = "SELECT ?s ?p ?o  WHERE {?s dc:language ?o .} LIMIT 20"
		tuple_query = connection.lattes21.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
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
		connection.lattes21.executeTupleQuery(query_string, output=True)  # Shows directly in console

		print("\n\n\n")
		print('Other type of query')
		connection.lattes21.executeTupleQuery('''SELECT ?s ?o WHERE {?s ?p ?o .
			filter (fn:lower-case(str(?o)) = "português")} LIMIT 20''', output=True)


		print("\n\n\n")
		print('Ordered languages')
		connection.lattes21.executeTupleQuery('''SELECT DISTINCT ?o WHERE {?s dc:language ?o .} ORDER BY ?o''', output=True)


		print("\n\n\n")
		# Trying statements
		print('Statements where object = "Português"')
		portugues = connection.lattes21.createLiteral("Português") # Para criar subject é createURI()
		statements = connection.lattes21.getStatements(subject=None, predicate=None, object=portugues, limit=20) # It is a RepositoryResult object
		with statements:
			#statements.enableDuplicateFilter()
			for statement in statements:
				print(statement)



	return render_template("about.html")


@app.route('/testes')
def testes():

	# server = AllegroGraphServer(host=connection.AGRAPH_HOST, port=AGRAPH_PORT, user=AGRAPH_USER, password=AGRAPH_PASSWORD)
	# catalog = server.openCatalog()
	# lattes = catalog.getRepository("lattes", Repository.OPEN).getConnection()
	# lattes21 = catalog.getRepository("lattes21", Repository.OPEN).getConnection()
	with connection.lattes21 as lattes21:
		# print('Repository lattes is up!, It contains %d statement(s).' % lattes.size())
		print('Repository lattes21 is up!, It contains %d statement(s).' % lattes21.size())


		#fedRepository = server.openFederated([lattes, lattes21])
		#print('Federated repository is up!, It contains %d statement(s).' % fedRepository.size())
		suastring = "meio ambiente"
		queryString = "PREFIX type:<http://purl.org/ontology/bibo/> SELECT (count(*) as ?conta) " \
		" WHERE {?s ?p ?type; dc:language 'Português'; dc:creator ?author; dc:title ?title . "\
		" ?author foaf:name ?author_name. filter (regex(fn:lower-case(str(?title)), '" + suastring + "')) . }"

		# print("Lattes:")
		# res = lattes.executeTupleQuery(queryString)
		# for binding_set in res:
		# 	conta = binding_set.getValue("conta")
		# 	print("%s" % (conta))


		print("\n\n\n")
		print("Lattes21:")
		res21 = lattes21.executeTupleQuery(queryString)
		for binding_set in res21:
			conta = binding_set.getValue("conta")
			print("%s" % (conta))


		'''print("\n\n\n")
		print("Federated Repositories:")
		resF = fedRepository.executeTupleQuery(queryString)
		for binding_set in resF:
			conta = binding_set.getValue("conta")
			print("%s" % (conta))
		'''

	# Nao olvidar de liberar as conexoes
	# lattes.close()
	lattes21.close()

	return render_template("about.html")