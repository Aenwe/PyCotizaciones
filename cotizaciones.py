#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import pyodbc as db
from cryptography.fernet import Fernet

key = "Vf_gOpTUF5OwarDYi8pGl8dVhpVZaFMAez9D__ElakE="
cipher_suite = Fernet(key)
encryptedpwd = ""
#Abro el archivo con la clave encriptada
with open('mssql_password.bin', 'rb') as file_object: 
    for line in file_object:
        encryptedpwd = line
uncipher_text = (cipher_suite.decrypt(encryptedpwd))


conn = db.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=DESKTOP-I8O8VVG;'
                      'Database=tESTsOFT;'
                      #'Trusted_Connection=yes;'
                      'UID=CWADBUser;'
                      'PWD='+ bytes(uncipher_text).decode("utf-8"))


cotizaciones = pd.read_html("http://www.bna.com.ar/Personas")[1].iloc(0)[0]


dCompra = cotizaciones.loc['Compra']
dVenta = cotizaciones.loc['Venta']
dFecha = cotizaciones.index[0].split('/')
dFecha = dFecha[2] + ('0' + dFecha[1])[-2::] + dFecha[0]

sSql = "INSERT INTO GRTVAL "
sSql = sSql + " SELECT 'USD', '" + dFecha + "', " + str(dCompra) + ", " + str(dVenta)

conn.execute(sSql)
conn.commit()
conn.close()




