import pyodbc
import tkinter as tk
from tkinter import *
from tkinter import simpledialog, filedialog, messagebox
 
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-TBID11H\\SQLEXPRESS;"
    "DATABASE=BookCo;"
    "UID=APIREST;"
    "PWD=0000;"
)
 
print("Connexion OK")