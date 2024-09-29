'''
Import this "libraryImports.py" in other python files as "import libraryImports"
and reference its content as with "libraryImports.function"
and to avoid dot notation, import this library of libarires as "from libraryImports import *"
'''

#GUI library
import tkinter as tk
from tkinter import *
from tkinter import ttk 
import tkinter.messagebox as tkmsgbox #for messagebox
from tkinter.messagebox import askokcancel, showinfo, WARNING
from tkinter import filedialog
#from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkcalendar import Calendar
from tkcalendar import DateEntry
import datetime
from  datetime import date
from  datetime import datetime
import PIL.Image #to avoid namespace conflicts as image is a common name
from PIL import Image, ImageTk #for image resize
#for file upload and calender
import os, shutil
from pathlib import Path
import time
#MySQL connectivity
import pymysql
from pandastable import Table
#Data & Visualization
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Install FPDF2 ver. 2.7.0+ (for table, page background etc.)
# pip install fpdf2==2.7.0
#from fpdf import FPDF
#from fpdf.fonts import FontFace
#from fpdf.enums import XPos, YPos

#to split a string with multiple delimiters
#e.g. mathematical expression as string to be splitted at + - * / ....
import re  

#====================================================================================
#MySQL Connectivity
myhost = 'localhost'
myuser = 'root'
mypassword = '244901'
mydatabase = 'ak_mall'
#keep following conn and cursor outside any scope incl. try and except for global access
conn=''
cursor=''
try:
        conn = pymysql.connect( host=myhost,
                                user=myuser,
                                password=mypassword,
                                db=mydatabase, 
                                cursorclass=pymysql.cursors.DictCursor
                                )
        #msg = "Connection established successfully."
        #tk.messagebox.showinfo("SUCCESS: ", msg)
except:
        conn = pymysql.connect(host='localhost', user='root', password='244901')
        cursor = conn.cursor()
        #create mysql database
        cursor.execute("CREATE DATABASE IF NOT EXISTS "+mydatabase)
        msg = "SUCCESS: Database "+ mydatabase +" created successfully."
        print(msg)
#open mysql database
#if conn is not None and conn.is_connected():
conn = pymysql.connect( host=myhost, user=myuser, password=mypassword, db=mydatabase, 
                                cursorclass=pymysql.cursors.DictCursor
                                )
cursor = conn.cursor()

#print('Connection established.')

#====================================================================================

