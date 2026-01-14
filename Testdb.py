import pyodbc
import tkinter as tk
from tkinter import *
from tkinter import simpledialog, filedialog, messagebox
 
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=ORDINATEUR-DE-J\\SQLEXPRESS;"
    "DATABASE=BookCo;"
    "UID=APIREST1;"
    "PWD=123Luteur*;"
)
 
print("Connexion OK")