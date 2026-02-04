import pyodbc
import tkinter as tk
from tkinter import *
from tkinter import simpledialog, filedialog, messagebox
 
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=GIBCYWIN\\SQLEXPRESS01;"
    "DATABASE=BookCo;"
    "UID=APIREST1;"
    "PWD=7zHDG4Ybj6y3m3;"
    "Encrypt=no;"
    
)

 
print("Connexion OK")