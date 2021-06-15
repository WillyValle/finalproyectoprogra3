
from flask import Flask, render_template, request, url_for, redirect, flash, url_for
from flask import Flask, session
import json
import networkx as nx
import graphviz
from networkx.algorithms.clique import node_clique_number
from networkx.algorithms.operators.product import _init_product_graph
from networkx.drawing import nx_agraph
from networkx.generators.degree_seq import expected_degree_graph
from networkx.generators.trees import prefix_tree
from networkx.readwrite import json_graph
import os
from werkzeug import security
from werkzeug.utils import secure_filename

R = nx.DiGraph()

listaNodosInicio = []
listaNodosFinal = []

primera=0
PrimeraAux=""

exfinal = Flask(__name__)

exfinal.secret_key= 'secretodeamor'

exfinal.config['UPLOAD_FOLDER'] = 'static/Fondos'
exfinal.config['UPLOAD_FOLDER2'] = 'static/img'


@exfinal.route('/')
def crear():
	return render_template("Crear.html")

@exfinal.route('/AgregarNodo',  methods=["POST"])
def agregarNodo():
	if request.method == 'POST':
		
		nombre = request.form['nombre']
		R.add_node(nombre)
		listaNodosInicio.exfinalend(nombre)
		listaNodosFinal.exfinalend(nombre)
		R.nodes[nombre]["Titulo"] = ""
		R.nodes[nombre]["Texto"] = ""
		R.nodes[nombre]["Fondo"] = ""
		R.nodes[nombre]["Imagen"] = ""
		R.nodes[nombre]["Primera"] = 0
		return render_template("Crear.html")


@exfinal.route('/Unir')
def unir():
	
	return render_template("Unir.html", data=listaNodosInicio, data1=listaNodosFinal)

@exfinal.route('/Lista')
def lista():
	return render_template("ListaNodos.html", data=R.nodes)

@exfinal.route('/UnirNodos',  methods=["POST"])
def UnirNodos():
	if request.method == 'POST':
		nombre1 = request.form['nodo1']
		nombre2 = request.form['nodo2']
		R.add_edge(nombre1, nombre2)
		listaNodosInicio.remove(nombre1)
		listaNodosFinal.remove(nombre2)
		return render_template("Unir.html", data=listaNodosInicio, data1=listaNodosFinal)

@exfinal.route('/EditarInfo',  methods=["POST"])
def EditarInfo():
	if request.method == 'POST':
		nombre= request.form['nodoaenviar']
		Imagen=str(R.nodes[nombre]["Imagen"])
		Fondo=str(R.nodes[nombre]["Fondo"])
		Texto=str(R.nodes[nombre]["Texto"])
		Titulo=str(R.nodes[nombre]["Titulo"])
		
		prim=str(R.nodes[nombre]["Primera"])
		
		return render_template("EditarInfoNodo.html",Titulo=Titulo,texto=Texto,fondo=Fondo,imagen=Imagen, name=nombre,Primera=int(primera),prima=int(prim))


@exfinal.route('/GuardarInfo', methods=['POST'])
def GuardarInfo():
	if request.method=='POST':
		nombre=request.form['Nombre']
		try:
			if request.form.getlist('Primera')[0]=='1':
				global primera
				primera=1
				R.nodes[nombre]["Primera"] = 1
				global PrimeraAux
				PrimeraAux=nombre
			else:
				print(":v")
		except:
			if R.nodes[nombre]["Primera"]==1:
				primera=0
				R.nodes[nombre]["Primera"] = 0
				PrimeraAux=""	
			else:
				R.nodes[nombre]["Primera"] = 0
				

			print("No existe :p")
		
		print("Si1")
		try:
			f = request.files['Imagen3']
			filename = secure_filename(f.filename)
			f.save(os.path.join(exfinal.config['UPLOAD_FOLDER2'], filename))
			ruta='img/'+filename
			R.nodes[nombre]["Imagen"] =ruta
			print("Ruta de la imagen "+str(R.nodes[nombre]["Imagen"]))
		except:
			try:
				R.nodes[nombre]["Imagen"] = (request.form['Imagen'])
			except:
				R.nodes[nombre]["Imagen"] = ""

		try:
			f2 = request.files['Fondo3']
			filename1 = secure_filename(f2.filename)
			f2.save(os.path.join(exfinal.config['UPLOAD_FOLDER'], filename1))
			ruta2='Fondos/'+filename1
			R.nodes[nombre]["Fondo"] =ruta2
			print("Ruta del fondo "+str(R.nodes[nombre]["Fondo"]))
			print("si2")
		except:
			R.nodes[nombre]["Fondo"] =(request.form['Fondo'])

		R.nodes[nombre]["Titulo"] = request.form['Titulo']
		R.nodes[nombre]["Texto"] = request.form['Texto']
		#R.nodes[nombre]["Fondo"] = request.form['Fondo']
		#R.nodes[nombre]["Imagen"] = request.form['Imagen']

		Imagen=str(R.nodes[nombre]["Imagen"])
		Fondo=str(R.nodes[nombre]["Fondo"])
		Texto=str(R.nodes[nombre]["Texto"])
		Titulo=str(R.nodes[nombre]["Titulo"])
		prim=str(R.nodes[nombre]["Primera"])
		print(prim)
		return render_template("EditarInfoNodo.html",Titulo=Titulo,texto=Texto,fondo=Fondo,imagen=Imagen, name=nombre, Primera=int(primera), prima=int(prim))

@exfinal.route('/VerDiapositiva')
def Verdiapositiva():
	
	if len(R.nodes)<1:
		return render_template("VerDiapositiva.html", nohay=-1)

	nombre=PrimeraAux
	Imagen=str(R.nodes[nombre]["Imagen"])
	Fondo=str(R.nodes[nombre]["Fondo"])
	Texto=str(R.nodes[nombre]["Texto"])
	Titulo=str(R.nodes[nombre]["Titulo"])
	
	try:
		
		if list(R.successors(nombre)):
			print("Aqui 1")
			Siguiente=list(R.successors(nombre))[0]
		else:
			Siguiente=-1
	except:
		print("Aqui 2")
		Siguiente=-1
	try:
		if list(R.predecessors(nombre))[0]:
			print("Aqui 3")
			Antes=list(R.predecessors(nombre))[0]
		else:
			Antes=-1
	except:
		print("Aqui 4")
		Antes=-1
	print(Antes)
	print(Siguiente)

	return render_template("VerDiapositiva.html",titulo=Titulo,texto=Texto,fondo=Fondo,imagen=Imagen, name=nombre, sigue=Siguiente, antes=Antes)

@exfinal.route('/Siguiente/<valor>')
def Siguiente(valor):
	nombre=valor
	Imagen=str(R.nodes[nombre]["Imagen"])
	Fondo=str(R.nodes[nombre]["Fondo"])
	Texto=str(R.nodes[nombre]["Texto"])
	Titulo=str(R.nodes[nombre]["Titulo"])
	x=0
	Siguiente=-1
	try:
		if list(R.successors(nombre)):
			x=1
			Siguiente=list(R.successors(nombre))[0]
	except:
		Siguiente=-1
	try:
		if list(R.predecessors(nombre))[0]:
			Antes=list(R.predecessors(nombre))[0]
	except:
		Antes=-1
	return render_template("VerDiapositiva.html",titulo=Titulo,texto=Texto,fondo=Fondo,imagen=Imagen, name=nombre, sigue=Siguiente, antes=Antes)


@exfinal.route('/Anterior/<valor>')
def Anterior(valor):
	nombre=valor
	Siguiente=-1
	Imagen=str(R.nodes[nombre]["Imagen"])
	Fondo=str(R.nodes[nombre]["Fondo"])
	Texto=str(R.nodes[nombre]["Texto"])
	Titulo=str(R.nodes[nombre]["Titulo"])
	try:
		if list(R.successors(nombre)):
			Siguiente=list(R.successors(nombre))[0]
		
	except:
		Siguiente=-1
	try:
		if list(R.predecessors(nombre))[0]:
			Antes=list(R.predecessors(nombre))[0]
	except:
		Antes=-1

	return render_template("VerDiapositiva.html",titulo=Titulo,texto=Texto,fondo=Fondo,imagen=Imagen, name=nombre, sigue=Siguiente, antes=Antes)


@exfinal.route('/VerMatris')
def Matris():
	Columnas=[]
	Filas=[]
	lista=[]
	lista2=[]
	for i in R.nodes:
		Columnas.exfinalend(i)
		Filas.exfinalend(i)

	r = len(Columnas)+1
	for i in range (r):
		lista.exfinalend(0)
		lista2.exfinalend(0)

	#print(lista)
	listaFinal=[]
	#print(lista[0])
	
	x=1
	for i in Filas:
		lista=lista2.copy()
		lista[0]=i
		for edge in R.edges:
			
			
			x=1
			for j in Columnas:
				
				if ((i==edge[0] and j == edge[1]) or (i==edge[1] and j == edge[0])):
					lista[x]=1
				x+=1
		
		print("Lista a guardar: " + str(lista))
		listaFinal.exfinalend(lista)
		print("Se vuelven 0 otra vez")
	
		
	return render_template("Matris.html", data=listaFinal, columnas=Columnas)

@exfinal.route('/Prueba')
def proba():
	A = nx.nx_agraph.to_agraph(R)
	A.layout('dot')
	A.draw('static/nodo.png') 
	graphviz.Source(A.to_string()) 
	return render_template("VerNodos.html")

if __name__=="__main__":
	exfinal.run(port=8000,debug=True)