#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import pyodbc as db
from cryptography.fernet import Fernet

import os
#os.environ['HTTP_PROXY']="http://usuario:clave@150.1.50.22:80"
os.environ['HTTP_PROXY']="http://150.1.70.102:3129"

key = "Vf_gOpTUF5OwarDYi8pGl8dVhpVZaFMAez9D__ElakE="
cipher_suite = Fernet(key)
encryptedpwd = ""
#Abro el archivo con la clave encriptada
with open('mssql_password.bin', 'rb') as file_object: 
    for line in file_object:
        encryptedpwd = line
uncipher_text = cipher_suite.decrypt(encryptedpwd)
cotizaciones = pd.read_html("http://www.bna.com.ar/Personas")[1]

dFecha = cotizaciones.columns[0].split('/')
dFecha = dFecha[2] + ('0' + dFecha[1])[-2::] + ('0' + dFecha[0])[-2::]

cotizaciones.columns = ['Moneda','Compra','Venta']

dfDolar = cotizaciones[cotizaciones["Moneda"] == "Dolar U.S.A"]
dfEuro = cotizaciones[cotizaciones["Moneda"] == "Euro"]

dCompraD = dfDolar["Compra"][0]
dVentaD = dfDolar["Venta"][0]
dCompraE = dfEuro["Compra"][2]
dVentaE = dfEuro["Venta"][2]

conn = db.connect('Driver={ODBC Driver 13 for SQL Server};'
                      'Server=150.1.40.107;'
                      'Database=AKAPOLSA;'
                      #'Trusted_Connection=yes;'
                      'UID=CWADBUser;'
                      'PWD='+ bytes(uncipher_text).decode("utf-8"))

conn106 = db.connect('Driver={ODBC Driver 13 for SQL Server};'
                      'Server=150.1.40.106;'
                      'Database=AKAPOLSA;'
                      #'Trusted_Connection=yes;'
                      'UID=CWADBUser;'
                      'PWD='+ bytes(uncipher_text).decode("utf-8"))

sSql = "EXEC SP_INS_GRTVAL "
sSql = sSql + "@CODCOF = 'USD', @FECCAL = '" + dFecha + "', @CIECOM = " + str(dCompraD) + ", @CIEVEN = " + str(dVentaD) + ", @USERID = 'ADMIN'"
print(sSql)
conn.execute(sSql)
conn.commit()
conn106.execute(sSql)
conn106.commit()

sSql = "EXEC SP_INS_GRTVAL "
sSql = sSql + "@CODCOF = 'EUR', @FECCAL = '" + dFecha + "', @CIECOM = " + str(dCompraE) + ", @CIEVEN = " + str(dVentaE) + ", @USERID = 'ADMIN'"
print(sSql)
conn.execute(sSql)
conn.commit()
conn106.execute(sSql)
conn106.commit()

conn.close()
conn106.close()
