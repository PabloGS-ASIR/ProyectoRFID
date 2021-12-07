from tkinter import *                 # Librería para la creación de la interfaz gráfica
from tkinter import messagebox
import mysql.connector				  # Librería para la conexión de la base de datos
from decimal import *
import RPi.GPIO as GPIO			      # Librería para la gestión de los pines de terminal RFID
from mfrc522 import SimpleMFRC522	  # Librería para el tratamiento información RFID


#-CONEXION MYSQL-----------------------------------------------------

#-conexion basica----------------------

def conex():

	
	global cnx


	cnx = mysql.connector.connect(user='admin', password='uned123',
                              host='192.168.80.2',
                              database='proyectoRFID')


