from tkinter import *
from tkinter import ttk #for combobox
import tkinter.messagebox as tkmsgbox
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfilename
import pymysql
from pandastable import Table
import pandas as pd
import matplotlib.pyplot as plt

globalDF = pd.DataFrame()
def dataAnalysis(dbname):
    #============================================
    #database connection
    #============================================
    #dbname='mastertrans'
    conn = pymysql.connect( host='localhost',user='root',port='',password='',db=dbname,cursorclass=pymysql.cursors.DictCursor)
    cursor=conn.cursor()
    #============================================
    #FUNCTIONS
    #============================================
    def createDataFrame(sqltable): #pass the dataframe as an element of a list - alternate of call by reference
        cursor.execute("select count(*) as numofrows from "+sqltable)
        numofrows = cursor.fetchone()['numofrows']
        if numofrows > 0:
            cursor.execute("select * from "+sqltable)
            data = cursor.fetchall()
            df=pd.DataFrame(data)
            return df
        else:
            tkmsgbox.showinfo("ATTENTION PLEASE!","The '"+cboTables.get().upper()+"' table is empty.", parent=rootDA)

            df=pd.DataFrame()
            return df #return empty dataframe
    def displayPandasTable(df):
        #width=rootDA.winfo_screenwidth()-50
        global globalDF
        globalDF = df
        pt = Table(framePandasTable, dataframe=globalDF)    
        pt.show()
    #============================================
    #GUI
    #============================================
    rootDA = Toplevel()
    rootDA.title('My Python Project')
    w, h = rootDA.winfo_screenwidth()-20, rootDA.winfo_screenheight()-100
    rootDA.geometry("%dx%d+0+0" % (w, h))
    rootDA.configure(background="#88cffa") #"light grey"
    
    #----------------------------------------
    #FRAME - control frames
    #----------------------------------------
    frameControls = Frame(rootDA, height=300, width=300, bg='#ccffcc')
    frameControls.grid(row=0, column=0, sticky=W, padx=20, pady=20)
    #----------------------------------------
    #label frame - frame1/display table and column names in combo box
    frame1 = LabelFrame(frameControls, text='frame1', font=('Times', 14), bd=5, relief=RIDGE)
    frame1.grid(row=0, column=0, sticky=W, padx=20, pady=20)
    r=0;
    Label(frame1, text="").grid(row=r, column=0, sticky=W, padx=4, pady=2) #for top padding
    r+=1;
    #combo box - display database table names
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='"+dbname+"'") 
    tablesdict = cursor.fetchall()
    tables=[]
    for i in range(len(tablesdict)):
        tables.append(tablesdict[i]['TABLE_NAME'])
    Label(frame1, text="Select Table").grid(row=r, column=0, sticky='W')
    cboTables=ttk.Combobox(frame1, values=tables)
    cboTables.grid(row=r, column=1, sticky='W')
    r+=1;
    Label(frame1, text="").grid(row=r, column=0, sticky=W, padx=4, pady=2) #for padding
    r+=1
    Label(frame1, text="Columns in table").grid(row=r, column=0, sticky='E')
    #cboColumns=ttk.Combobox(frame4, values=fields)
    cboColumns=ttk.Combobox(frame1)
    cboColumns.grid(row=r, column=1)
    cboTables.current(0)
    def fillColumnsCbo():
        cursor.execute("DESC "+cboTables.get())
        fieldsdict = cursor.fetchall()
        fields=[]
        for i in range(len(fieldsdict)):
            fields.append(fieldsdict[i]['Field']) #show column names of the specified table
        cboColumns['values'] = fields #update columns combo box upon selecting table in cboTables
        cboColumns.current(0)
        try:
            cboXaxis['values'] = fields
            cboXaxis.current(0)
            cboYaxis['values'] = fields
            cboYaxis.current(0)
            cbofields['values'] = fields
            cbofields.current(0)
        except:
            a=1
    def cboTablesSelectedEvent(event):#display pandasTable using selected table
        df=createDataFrame(cboTables.get())
        if df.empty==False:
            displayPandasTable(df)
            fillColumnsCbo()
    cboTables.bind("<<ComboboxSelected>>", cboTablesSelectedEvent)
    fillColumnsCbo() #to fill cboColumns on startup
    r+=1;
    Label(frame1, text="").grid(row=r, column=2, sticky=W, padx=4, pady=2) #for bottom padding
    #----------------------------------------
    ##label frame - frame5/filter dataframe data
    frame5 = LabelFrame(frameControls, text='frame5', font=('Times', 14), bd=5, relief=RIDGE)
    frame5.grid(row=0, column=4, sticky=W, padx=20, pady=20)
    r=0
    Label(frame5, text="").grid(row=r, column=0, sticky=W, padx=4, pady=2)
    r+=1
    Label(frame5, text="FILTER DF DATA").grid(row=r, column=0, columnspan=2, sticky='W')
    r+=1
    expTXT = Text(frame5, height=3, width=30)
    expTXT.grid(row=r, column=0, columnspan=2, rowspan=3, padx=4)
    r+=3
    Label(frame5, text="Column").grid(row=r, column=0, sticky=W)
    cbofields=ttk.Combobox(frame5, values=cboColumns['values'])
    cbofields.grid(row=r, column=1, sticky=W)
    cbofields.current(0)
    r+=1
    Label(frame5, text="Operator").grid(row=r, column=0, sticky=W)
    cboop=ttk.Combobox(frame5, values=['<','>','==','<=','>=','&','|'])
    cboop.grid(row=r, column=1, sticky=W)
    cboop.current(0)
    r+=1
    Label(frame5, text="Value").grid(row=r, column=0, sticky=W)
    valTXT = Text(frame5, height=1, width=15)
    valTXT.grid(row=r, column=1, sticky=W)
    def filterDataBtnClickEvent():
        df=createDataFrame(cboTables.get())
        expTXT.insert(INSERT, valTXT.get("1.0", "end-1c"))
        expTXT.insert(INSERT, ')]')
        df = eval(expTXT.get('1.0','end-1c')) #e.g. df[df.itemcode>5]
        #print(df)
        displayPandasTable(df)
    #expTXT.delete('1.0', 'end-1c')
    def cbofieldsSelectedEvent(event):
        if len(expTXT.get('1.0', 'end-1c'))<=0:
            expTXT.insert(INSERT, 'df[(')
            #expTXT.delete('1.0', 'end-1c')
            expTXT.insert(INSERT, 'df.'+event.widget.get())
    cbofields.bind("<<ComboboxSelected>>", cbofieldsSelectedEvent)
    #expTXT.delete('1.0', 'end-1c')
    def cboopSelectedEvent(event):
        #expTXT.delete('1.0', 'end-1c')
        if event.widget.get()=='&' or event.widget.get()=='|':
            expTXT.insert(INSERT, ') '+event.widget.get()+' (')
        else:
            expTXT.insert(INSERT, event.widget.get())
    cboop.bind("<<ComboboxSelected>>", cboopSelectedEvent)
    '''
    #textbox change event
    def f1(*args):
        expTXT.insert(INSERT, valTXT.get("1.0", "end-1c"))
    valTXT.bind('<KeyRelease>', lambda *args: f1())
    '''
    r+=1
    Button(frame5, text='Filter Data', command=filterDataBtnClickEvent).grid(row=r, column=1, sticky='W')
    r+=1
    Label(frame5, text="").grid(row=r, column=1, sticky=W, padx=4, pady=2)
    #----------------------------------------
    #----------------------------------------
    #FRAME - pandasTable
    #----------------------------------------
    # w, h = rootDA.winfo_screenwidth()-20, rootDA.winfo_screenheight()-100
    framePandasTable = Frame(rootDA, height=300, width=rootDA.winfo_screenwidth()-50, bg='#ffcccc')
    framePandasTable.grid(row=1, column=0, sticky=W, padx=20, pady=20)
    #infinite loop
    rootDA.mainloop()

#dataAnalysis('mastertrans001')
