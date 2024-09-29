import tkinter as tk
from tkinter import *
from tkinter import ttk 
import tkinter.messagebox as tkmsgbox
import pymysql
import pandas as pd
import numpy as np

def help():
    frameHelp = Tk()
    frameHelp.title("Mall Management System")
    r=0
    Label(frameHelp, height=10, width=50,bg = 'aquamarine1', text="Welcome to our mall management system \n\
if you have any issue related to our management\n\
system please contact:\n\
akmanagement@gmail.com\n\
http://www.akofficial.com").grid(row=r, column=0)
    frameHelp.mainloop()
    
def about():    
    frameHelp = Tk()
    frameHelp.title("Mall Management System")
    r=0
    Label(frameHelp, height=10, width=50,bg = 'aquamarine1', text="Welcome to our mall management system \n \
                                                Our software is a conducive problem solver at our service. \
                                                \n It will assist  in managing your auspicious mall. \n\n \
                                                for any query please visit our website \n \
                                                http://www.akofficial.com").grid(row=r,column=5)
    frameHelp.mainloop()
def manual():    
    frameHelp = Tk()
    frameHelp.title("Mall Management System")
    r=0
    Label(frameHelp, height=10, width=50,bg = 'aquamarine1', text="Welcome to our mall management system. \n \
Just login to our Mall Management System and using the user\n\
friendly interface. If you have any problem then just visit our\n\
official website or get in touch with us on Gmail.").grid(row=r,column=5)
    frameHelp.mainloop()
