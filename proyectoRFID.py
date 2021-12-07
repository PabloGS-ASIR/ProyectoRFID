from tkinter import *                     # Librería para la creación de la interfaz gráfica
from tkinter import messagebox
from tkinter import ttk
import mysql.connector					  # Librería para la conexión de la base de datos                
import RPi.GPIO as GPIO					  # Librería para la gestión de los pines de terminal RFID
from mfrc522 import SimpleMFRC522		  # Librería para el tratamiento información RFID
import funcionesRFID as F     			  # Fichero con Funciones de conexión del programa

root=Tk()
root.title("PROYECTO RFID")
root.geometry("450x280")

#-MENUS-----------------------------------------------------

def menu(pantalla): # Menu accesible en pantalla para los usuarios registrados como usuarios

	barraMenu=Menu(pantalla)
	pantalla.config(menu=barraMenu, width=300, height=300)

	movimientosMenu=Menu(barraMenu, tearoff=0)
	barraMenu.add_cascade(label="Movimientos", menu=movimientosMenu)
	movimientosMenu.add_command(label="Entrada", command=entryProduct)
	movimientosMenu.add_command(label="Salida", command=exitProduct)

	inventariosMenu=Menu(barraMenu, tearoff=0)
	barraMenu.add_cascade(label="Inventarios", menu=inventariosMenu)
	inventariosMenu.add_command(label="Nuevo", command=newinvtryQuery)


	consultaStockMenu=Menu(barraMenu, tearoff=0)
	barraMenu.add_cascade(label="Consulta Stock", menu=consultaStockMenu)
	consultaStockMenu.add_command(label="Stock", command=stockQuery)
	consultaStockMenu.add_command(label="Negativos")

	userMenu=Menu(barraMenu, tearoff=0)
	barraMenu.add_cascade(label="Usuarios", menu=userMenu)
	userMenu.add_command(label="Entrar")
	userMenu.add_command(label="Datos")
	userMenu.add_separator()
	userMenu.add_command(label="Salir")

def menuAdmin(pantalla): # Menu accesible en pantalla para los usuarios registrados como administradores

	barraMenu=Menu(pantalla)
	pantalla.config(menu=barraMenu, width=300, height=300)

	movimientosMenu=Menu(barraMenu, tearoff=0)
	barraMenu.add_cascade(label="Movimientos", menu=movimientosMenu)
	movimientosMenu.add_command(label="Entrada", command=entryProduct)
	movimientosMenu.add_command(label="Salida", command=exitProduct)

	inventariosMenu=Menu(barraMenu, tearoff=0)
	barraMenu.add_cascade(label="Inventarios", menu=inventariosMenu)
	inventariosMenu.add_command(label="Nuevo", command=newinvtryQuery)


	maestroProducto=Menu(barraMenu, tearoff=0)
	barraMenu.add_cascade(label="Maestro Producto", menu=maestroProducto)
	maestroProducto.add_command(label="Nuevo")
	maestroProducto.add_command(label="Borrar")

	maestroUser=Menu(barraMenu, tearoff=0)
	barraMenu.add_cascade(label="Maestro Usuarios", menu=maestroUser)
	maestroUser.add_command(label="Nuevo")
	maestroUser.add_command(label="Borrar")

	consultaStockMenu=Menu(barraMenu, tearoff=0)
	barraMenu.add_cascade(label="Consulta Stock", menu=consultaStockMenu)
	consultaStockMenu.add_command(label="Stock", command=stockQuery)
	consultaStockMenu.add_command(label="Negativos")

	userMenu=Menu(barraMenu, tearoff=0)
	barraMenu.add_cascade(label="Usuarios", menu=userMenu)
	userMenu.add_command(label="Entrar")
	userMenu.add_command(label="Datos")
	userMenu.add_separator()
	userMenu.add_command(label="Salir")

#--FIN DE MENU

loginMsg=Label(root, text="Login")
loginMsg.pack()

#--Variables---------------------------------------

global userCheck
global passCheck
global userCategory
global cnx
global read

userCheck = StringVar()
passCheck = StringVar()
userCategory = StringVar()


#-PANTALLA REGISTRO----------------------------------

def iniUser(): # Funcion para la creación de pantalla de login inicial

	#--Frame-------------------------------------------

	inicioFrame=Frame(root, width=1000, height=600)
	inicioFrame.pack()

	#--usuario-----------------------------------------

	userLabel=Label(inicioFrame, text="Usuario: ")
	userLabel.grid(row=0, column=0)
	userText=Entry(inicioFrame, textvariable=userCheck)
	userText.grid(row=0, column=1)

	#--password----------------------------------------

	passLabel=Label(inicioFrame, text="Password: ")
	passLabel.grid(row=1, column=0)
	passText=Entry(inicioFrame, textvariable = passCheck)
	passText.grid(row=1, column=1)
	passText.config(show="*")

	#------botonLogin----------------------------------

	botonEnvio=Button(root, text="Enviar", command=loginUser)
	botonEnvio.pack()

#-PANTALLA BIENVENIDA----------------------------------	

def loginUser(): # Funcion para comprobacion de usuario y contraseña en la base de datos

	F.conex()

	cursor = F.cnx.cursor()

	query = ("select userID, uName, uCategory from users where uName=%(uName)s and password=%(password)s")

	cursor.execute(query, { 'uName': userCheck.get(), 'password': passCheck.get() })

	result=cursor.fetchone()


	if not result:

		unwelcomeMsg=Label(root, text="Usuario o contraseña no validos")
		unwelcomeMsg.pack()

		root.state(newstate="normal")

	global userSession
	global userName
	
	userSession=result[0]
	userName=result[1]
	userCategory=result[2]

	login=Toplevel(root)
	login.title("Proyecto RFID - Usuario " + userName)
	login.geometry("750x450")

	loginFrame=Frame(login, width=1000, height=600)
	loginFrame.pack()

	#--- TIPO MENU --------------------------------

	if userCategory=='admin':

		menuAdmin(login)

	else:

		menu(login)

	welcomeMsg=Label(loginFrame, text="Bienvenido, su permiso es de " + userCategory)
	welcomeMsg.pack()

	root.state(newstate="withdraw")
	login.state(newstate="normal")

	cursor.close()

	F.cnx.close()

	login.mainloop()

#--MOVIMIENTOS

#--ENTRADAS-------------------------------------------

def entryCatalog(): # Funcion para la creacion de pantalla con catálogo de productos dados de alta en la base de datos

	entryCat=Toplevel(root)
	entryCat.title("Catálogo")
	entryCat.geometry("150x450")

	catFrame=Frame(entryCat, width=1000, height=600)
	catFrame.pack()

	#CONEXION --- CATALOGO

	F.conex()

	cursor = F.cnx.cursor()

	query = ("select productID, prodDescription from products")

	cursor.execute(query)

	result = cursor.fetchall()

	F.cnx.commit()

	heading1 = Label(catFrame, text='Producto')
	heading1.grid(row=0, column=0)
	heading2 = Label(catFrame, text='Description')
	heading2.grid(row=0, column=1)

	i=1
	j=0

	for x in range(len(result)):

		prod = Label(catFrame, text=int(result[j][0]))
		prod.grid(row=i, column=0)

		desc = Label(catFrame, text=result[j][1])
		desc.grid(row=i, column=1)
		
		i = i + 1
		j = j + 1

	cursor.close()

	F.cnx.close()

	#FIN --- CATALOGO

	entryCat.mainloop()

def entryProduct():  # Funcion para la creacion de pantalla de entrada de stock

	entry=Toplevel(root)
	entry.title("Entrada Producto")
	entry.geometry("450x150")

	entryFrame=Frame(entry, width=1000, height=600)
	entryFrame.pack()

	#--product-----------------------------------------

	global convertProd
	global intProd
	global productText

	productLabel=Label(entryFrame, text="Seleccione Producto:  ")
	productLabel.grid(row=0, column=0)
	productText=ttk.Combobox(entryFrame)

	#CONEXION --- ELECCION PRODUCTO

	F.conex()

	cursor = F.cnx.cursor()

	query = ("select productID from products")

	cursor.execute(query)

	result = cursor.fetchall()

	F.cnx.commit()

	cursor.close()

	F.cnx.close()

	productText['values'] = (result)

	#FIN --- ELECCION PRODUCTO

	productText.grid(row=0, column=1)
	productCatalog=Button(entryFrame, text='Catálogo Productos', command=entryCatalog)	
	productCatalog.grid(row=0, column=2)

	def entryQuery(): # Funcion para insercion del registro de entrada en la base de datos

		#CONEXION

		F.conex()

		cursor = F.cnx.cursor()

		try:

			testT = ("select sum(movSign) from movements where rfidID=%(rfidID)s;")
			cursor.execute(testT, { 'rfidID': read[0] } )
			testTag = cursor.fetchone()

			# se comprueba que el tag RFID no está en stock

			if testTag[0] is None or testTag[0] == 0:
				cursor.close()
				F.cnx.close()
				F.conex()
				cursor2 = F.cnx.cursor()
				query = ("insert into movements (productID, userID, type, creationMovDate, rfidID, movSign) values (%(productID)s, %(userID)s, 'ENTRADA',now(), %(rfidID)s, 1)")
				cursor2.execute(query, {'productID': int(productText.get()),'userID': int(userSession), 'rfidID': read[0] })
				F.cnx.commit()
				messagebox.showinfo('Entrada Producto','Entrada Confirmada')
				cursor.close()
				F.conex()
			else:
				messagebox.showinfo('Entrada no permitida', 'Tag en stock')
				cursor.close()
				F.cnx.close()       
                                     
		except Exception as e:

			messagebox.showinfo('Entrada Producto', e)
			F.cnx.rollback()

		cursor.close()

		F.cnx.close()

		productText.delete(0, 'end')

	#--tag RFID-----------------------------------------

	global convertQty
	global intQty
	global qtyText

	rfidLabel=Label(entryFrame, text="RFID tag: ")
	rfidLabel.grid(row=1, column=0)
	
	def readRFID():# PARA LEER EL TAG RFID
                    
		global read
		
		try:
			readRFID = SimpleMFRC522()
			read = readRFID.read()
			labelRFID = Label(entryFrame, text = int(read[0]))
			labelRFID.grid(row = 1, column = 1)

			tag = int(read[0])
			print(tag)

		finally:

			GPIO.cleanup()
		
	#--botonRFID----------------------------------

	buttonRFID=Button(entryFrame, text="Detectar RFID", command=readRFID)
	buttonRFID.grid(row=2, column=1)

	#--botonEntry----------------------------------

	buttonEntry=Button(entryFrame, text="Entrada", command=entryQuery)
	buttonEntry.grid(row=2, column=2)
	

	entry.mainloop()

#--SALIDAS-------------------------------------------

def exitProduct(): # Funcion para la creacion de pantalla de salida de stock

	exit=Toplevel(root)
	exit.title("Salida Producto")
	exit.geometry("450x150")

	exitFrame=Frame(exit, width=1000, height=600)
	exitFrame.pack()

	def readExitRFID():# PARA LEER EL TAG RFID
                    
		global readExit
		
		try:
			readRFIDExit = SimpleMFRC522()
			readExit = readRFIDExit.read()
			labelRFID = Label(exitFrame, text = int(readExit[0]))
			labelRFID.grid(row = 0, column = 1)

		finally:

			GPIO.cleanup()

	#--product-----------------------------------------

	global convertProd
	global intProd
	global productText

	productLabel=Label(exitFrame, text="RFID tag: ")
	productLabel.grid(row=0, column=0)

	def exitQuery(): # Funcion para insercion del registro de salida en la base de datos

		#CONEXION

		F.conex()

		cursor = F.cnx.cursor()

		try:

			testE = ("select sum(movSign), productID, rfidID from movements where rfidID=%(rfidID)s and creationMovDate=(select max(creationMovDate) from movements where rfidID=%(rfidID)s) group by productID order by sum(movSign) desc;")
			cursor.execute(testE, { 'rfidID': readExit[0] } )
			testExit = cursor.fetchone()

			if testExit[0] == 1:

				cursor.close()
				F.cnx.close()
				F.conex()
				cursor2 = F.cnx.cursor()
				query2 = ("insert into movements (productID, userID, type, creationMovDate, rfidID, movSign) values (%(productID)s, %(userID)s, 'SALIDA',now(), %(rfidID)s, -1);")
				cursor2.execute(query2, {'productID': int(testExit[1]),'userID': int(userSession), 'rfidID': readExit[0] })
				F.cnx.commit()
				messagebox.showinfo('Salida Producto','Salida Confirmada')
				cursor2.close()
				F.cnx.close()

			else:

				messagebox.showinfo('Salida no permitida', 'Tag no está stock')
				cursor.close()
				F.cnx.close()  

		except Exception as e:

			messagebox.showinfo('Salida Producto','Se ha producido un error')
			cnx.rollback()

		cursor.close()

		F.cnx.close()

	#--Botones----------------------------------

	buttonEntry=Button(exitFrame, text="Detectar RFID", command=readExitRFID)
	buttonEntry.grid(row=2, column=1)
	buttonEntry=Button(exitFrame, text="Salida", command=exitQuery)
	buttonEntry.grid(row=2, column=2)

	exit.mainloop()

#--CONSULTA STOCK

#--STOCK-------------------------------------------

def stockQuery(): # Funcion para la creacion de la pantalla de consulta de stock

	stock=Toplevel(root)
	stock.title("Consulta Stock")
	stock.geometry("450x150")

	stockFrame=Frame(stock, width=1000, height=600)
	stockFrame.pack()

	#CONEXION

	F.conex()

	cursor = F.cnx.cursor()

	query = ("select productID, count(rfidID) as Qty from movements group by productID")

	cursor.execute(query)

	result = cursor.fetchall()

	F.cnx.commit()

	heading1 = Label(stockFrame, text='Producto')
	heading1.grid(row=0, column=0)
	heading2 = Label(stockFrame, text='Cantidad')
	heading2.grid(row=0, column=1)

	i=1
	j=0

	for x in range(len(result)):

		prod = Label(stockFrame, text=int(result[j][0]))
		prod.grid(row=i, column=0)

		qty = Label(stockFrame, text=int(result[j][1]))
		qty.grid(row=i, column=1)
		
		i = i + 1
		j = j + 1

	cursor.close()

	F.cnx.close()

	stock.mainloop()

#--INVENTARIOS

def newinvtryQuery(): # Funcion para la creacion de la pantalla de inventario

	newInv=Toplevel(root)
	newInv.title("Nuevo Inventario")
	newInv.geometry("550x250")

	newInvFrame=Frame(newInv, width=1000, height=600)
	newInvFrame.pack()

	scrollbar = Scrollbar(newInv)
	scrollbar.pack(side = RIGHT, fill = Y)

	menu(newInv)

	#CONEXION

	# ---- BORRADO TABLA SI EXISTIA --------#

	F.conex()

	cursorInv = F.cnx.cursor()

	query = ("drop table if exists newInv;")

	cursorInv.execute(query)

	cursorInv.close()

	F.cnx.close()

	F.conex()

	# ---- CREACION TABLA --------#

	cursorInv = F.cnx.cursor()

	query = ("create table newInv(productID int not null,rfidID varchar(255) not null,inventory varchar(2));")

	cursorInv.execute(query)

	cursorInv.close()

	F.cnx.close()

	# ---- INSERT TABLA --------#

	F.conex()

	cursorInvIns = F.cnx.cursor()

	queryInvIns = ("insert into newInv(productID, rfidID) select productID, rfidID from movements group by productID,rfidID having (sum(movSign) = 1);")

	cursorInvIns.execute(queryInvIns)

	F.cnx.commit()

	cursorInvIns.close()

	F.cnx.close()

	# ---- SELECT TABLA --------#

	def actInv(): # Crea la pantalla con los datos de stock

		def exeInv(): # Funcion para ejecutar inventario y que inserta en la base de datos los casos no identificados en el inventario

			try:

				F.conex()

				cursorExe = F.cnx.cursor()

				cursorExe.execute("select * from where inventory is NULL;")

				resultExe = cursorExe.fetchall()

				if resultExe is None:

					messagebox.showinfo('Alerta inventario', 'No hay regularizaciones')

					cursorExe.close()

					F.cnx.close()

				else:

					j=0
				
					for x in range(len(resultInv)):

						F.conex()

						cursorReg = F.cnx.cursor()

						queryReg = ("insert into movements (productID, userID, type, creationMovDate, rfidID, movSign) values (%(productID)s, %(userID)s, 'INVENTARIO',now(), %(rfidID)s, -1)")

						cursorReg.execute(queryReg, {'productID': resultExe[j][0],'userID': int(userSession), 'rfidID': resultExe[j][1] })

			finally:

					messagebox.showinfo('Alerta inventario', 'Inventario finalizado')

					cursorReg.close()

					F.cnx.close()

		global resultInv
		global cursorInvSel

		F.conex()

		cursorInvSel = F.cnx.cursor()

		queryInv = ("select productID, rfidID, inventory from newInv;")

		cursorInvSel.execute(queryInv)

		resultInv = cursorInvSel.fetchall()

		F.cnx.commit()

		heading1 = Label(newInvFrame, text='Producto')
		heading1.grid(row=0, column=0)
		heading2 = Label(newInvFrame, text='Tag')
		heading2.grid(row=0, column=1)
		heading3 = Label(newInvFrame, text='Inventario')
		heading3.grid(row=0, column=2)

		i=1
		j=0

		for x in range(len(resultInv)):

			prod = Label(newInvFrame, text=int(resultInv[j][0]))
			prod.grid(row=i, column=0)

			tag = Label(newInvFrame, text=int(resultInv[j][1]))
			tag.grid(row=i, column=1)

			inv = Label(newInvFrame, text=resultInv[j][2])
			inv.grid(row=i, column=2)
		
			i = i + 1
			j = j + 1

		invButton = Button(newInvFrame, text = "Detectar Tag", command = insertTag)
		invButton.grid(row=i, column=0)

		actButton = Button(newInvFrame, text = "Actualizar", command = actInv)
		actButton.grid(row=i, column=1)

		exeButton = Button(newInvFrame, text = "Ejecutar", command = exeInv)
		exeButton.grid(row=i, column=2)

		cursorInvSel.close()

		F.cnx.close()

	def insertTag(): # Funcion para insertar tag en la pantalla del inventario

		def updateTag(): # Funcion para update tag inventario

			F.conex()

			cursorInvUpd = F.cnx.cursor()

			try:

				testInv = ("select sum(movSign) from movements where rfidID=%(rfidID)s;")
				cursorInvUpd.execute(testInv, { 'rfidID': read[0] } )
				testTag = cursorInvUpd.fetchone()

				if testTag[0] == 1:
					cursor.close()
					F.cnx.close()
					F.conex()
					cursor2 = F.cnx.cursor()
					queryInvUpd = ("update newInv set inventory = 'SI' where rfidID = %(rfidID)s;")
					cursorInvUpd.execute(queryInvUpd, { 'rfidID': read[0] })
					F.cnx.commit()
					messagebox.showinfo('Entrada Inventario','Entrada inventario confirmada')
					cursor2.close()
					F.cnx.close()
				else:
					messagebox.showinfo('Alerta inventario', 'Tag no está en stock')
					cursor2.close()
					F.cnx.close()
			except Exception as e:

				messagebox.showinfo('Error inventario', e)
				F.cnx.rollback()
				F.cnx.close()

			cursorInvUpd.close()

			F.cnx.close()

			actInv() # Actualiza la pantalla de inventario cuando se inserta un tagRFID

		def readRFID():# PARA LEER EL TAG RFID
                    
			global read
		
			try:
				readRFID = SimpleMFRC522()
				read = readRFID.read()
				labelRFIDInv = Label(insTagFrame, text = int(read[0]))
				labelRFIDInv.grid(row = 0, column = 1)

			finally:

				GPIO.cleanup()

		insTag=Toplevel(newInv)
		insTag.title("Insertar Tag")
		insTag.geometry("450x150")

		insTagFrame=Frame(insTag, width=1000, height=600)
		insTagFrame.pack()	

		insTagLabel=Label(insTagFrame, text="Tag: ")
		insTagLabel.grid(row=0, column=0)

		insDectButton = Button(insTagFrame, text = "Detectar Tag", command = readRFID)
		insDectButton.grid(row=1, column=1)
		insTagButton = Button(insTagFrame, text = "Insertar Tag", command = updateTag)
		insTagButton.grid(row=1, column=2)

		insTag.mainloop()

	actInv()	

	def exeInv(): # Funcion para ejecutar inventario y que inserta en la base de datos los casos no identificados en el inventario

		try:

			F.conex()

			cursorExe = F.cnx.cursor()

			cursorExe.execute("select * from where inventory is NULL;")

			resultExe = cursorExe.fetchall()

			if resultExe is None:

				messagebox.showinfo('Alerta inventario', 'No hay regularizaciones')

				cursorExe.close()

				F.cnx.close()

			else:

				j=0
				
				for x in range(len(resultInv)):

					F.conex()

					cursorReg = F.cnx.cursor()

					queryReg = ("insert into movements (productID, userID, type, creationMovDate, rfidID, movSign) values (%(productID)s, %(userID)s, 'INVENTARIO',now(), %(rfidID)s, -1)")

					cursorReg.execute(queryReg, {'productID': resultExe[j][0],'userID': int(userSession), 'rfidID': resultExe[j][1] })

		finally:

				messagebox.showinfo('Alerta inventario', 'Inventario finalizado')

				cursorReg.close()

				F.cnx.close()	

	newInv.mainloop()

#--INICIO PROGRAMA----

iniUser()

root.mainloop()



