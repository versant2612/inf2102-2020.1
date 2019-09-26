# views.py
from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.repository.repository import Repository

from flask import render_template

from app import app

@app.route('/')
def index():
	server = AllegroGraphServer(host="localhost", port=10035, user="nima", password="nima2019")
	catalog = server.openCatalog()
	print(catalog.getRepository("lattes", Repository.ACCESS).getConnection().isEmpty())
	print(catalog.getRepository("lattes", Repository.ACCESS).getConnection().listIndices())

	return render_template("index.html")

@app.route('/about')
def about():
	return render_template("about.html")