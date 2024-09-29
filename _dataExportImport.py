from _libraryAndDBConnection import * #includes database connection and cursor setting strings
#------------------------------------------------------------------------------------------------
global globaldf #for reference from within many functions
#------------------------------------------------------------------------------------------------
def savedisplayedDFtoMySQLTableSQLEngine(rootframe, globaldf, cbotableselected):
    '''
    #PREPARING DATAFRAME
    #===================
    dftemp = pd.read_csv("meet_logs_1627694691222 31July2021.csv")
    df.rename(columns=mymapper, inplace=True)
    df.loc[:,'Date'] = df['Date'].str[:12]
    df.loc[:,'Duration']=df['Duration'].fillna(0)
    df.loc[:,'Duration'] = round(df['Duration']/60)
    df.Duration.astype(int)
    '''
    '''
    #dataframe to SQL
    #================
    sqlEngine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root",pw="",db=mydatabase))
    connection = sqlEngine.connect()
    try:
        frame = globaldf.to_sql(cbotableselected, connection, index=False)  #if_exists='replace', if_exists='append'
    except pymysql.Error as e:
        print("ERROR: %d: %s" %(e.args[0], e.args[1]))
    else:
        print("Table %s created successfully."%cbotableselected)  
    finally:
        connection.close()
    '''
#------------------------------------------------------------------------------------------------
def savedisplayedDFtoMySQLTableInsert(rootframe, globaldf, cbotableselected):
    # INSERT
    try:
            cols = ''
            for c in globaldf.columns:
                cols += c + ','
            cols = cols[:-1]
            #for i in globaldf.iterrows:
            for i in range(len(globaldf.index)):
                #for i in range(len(globaldf.columns)):
                row = globaldf.loc[i].tolist()
                vals = ''
                for v in row:
                    vals += "'"+str(v)+"'"+','
                vals = vals[:-1]
                sql = "INSERT INTO " + cbotableselected + "(" + cols + ") VALUES(" + vals + ")" 
                cursor.execute(sql)
                conn.commit()
            msg = "Records inserted into MySQL table "+cbotableselected
            tk.messagebox.showinfo("MESSAGE", msg, parent=rootframe)        
    except conn.Error as e:
            msg = "ERROR: "+str(e.args[0])+e.args[1]
            tk.messagebox.showinfo("MESSAGE", msg, parent=rootframe)        
#------------------------------------------------------------------------------------------------
def savedisplayedDFtoMySQLTableUpdate(rootframe, globaldf, cbotableselected):
    # UPDATE
    try:
            #sql = "SHOW INDEX FROM "+mydatabase+"."+cbotableselected+" WHERE Key_name = 'PRIMARY'"
            sql = '''SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
                     WHERE TABLE_SCHEMA = "'''+mydatabase+'''" 
                     AND TABLE_NAME = "'''+cbotableselected+'''" AND COLUMN_KEY = "PRI"'''
            cursor.execute(sql)
            pk = cursor.fetchone()
            #print("Table: ",cbotableselected," PK: ",pk,"    ",pk['COLUMN_NAME'])  #outputs a dictionary e.g. {'COLUMN_NAME': 'customercode'}
            #print("PK Value: ",globaldf.iloc[0][pk['COLUMN_NAME']])
            colnames = globaldf.columns
            #for i in globaldf.iterrows:
            for i in range(len(globaldf.index)):
                rowdata = globaldf.loc[i].tolist()
                sql = "UPDATE " + cbotableselected + " SET " 
                for j in range(len(globaldf.columns)):
                    if colnames[j]==pk['COLUMN_NAME']:
                        pass
                    else:
                        sql += colnames[j] + "='" + str(rowdata[j]) + "',"
                sql = sql[:-1]
                sql += " WHERE "+pk['COLUMN_NAME']+" = "+str(globaldf.iloc[i][pk['COLUMN_NAME']])
                #print(sql)
                cursor.execute(sql)
            conn.commit()
            msg = "Records updated in MySQL table "+cbotableselected
            tk.messagebox.showinfo("MESSAGE", msg, parent=rootframe)        
    except conn.Error as e:
            msg = "ERROR: "+str(e.args[0])+e.args[1]
            tk.messagebox.showinfo("MESSAGE", msg, parent=rootframe)        
#------------------------------------------------------------------------------------------------
def savedisplayedDFasCSVFile(df):
    filetypes = [('CSV Files','*.csv')]
    saveatfilepath = asksaveasfile(mode='w', filetypes = filetypes, defaultextension=filetypes)
    df.to_csv(saveatfilepath, index=False,  line_terminator='\n')
    # header=False
    #use lineterminator to avoid blank lines in csv file
#------------------------------------------------------------------------------------------------
def getNumOfRowsOfMySQLTable(mysqltable):
    cursor.execute("select count(*) as numofrows from "+mysqltable)
    numofrows = cursor.fetchone()['numofrows']
    return numofrows
#------------------------------------------------------------------------------------------------
def getDataFrameFromCSVFile():
    filetypes = [('CSV Files','*.csv')]
    csvfilepath = askopenfilename(filetypes = filetypes, defaultextension = filetypes) 
    #dfcsv=pd.read_csv(file_path,usecols=['Name','Email','Gender'])
    df = pd.read_csv(csvfilepath)
    return df
#------------------------------------------------------------------------------------------------
def getDataFrameFromSQLQuery(sql):
    cursor.execute(sql)
    data = cursor.fetchall()
    df=pd.DataFrame(data)
    return df
#------------------------------------------------------------------------------------------------
def getDataFrameFromMySQLTable(mysqltable):
    cursor.execute("select * from "+mysqltable)
    data = cursor.fetchall()
    df=pd.DataFrame(data)
    return df
#------------------------------------------------------------------------------------------------
def getTablenamesOfMySQLDatabase(dbname):
    sql = '''SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
             WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA="'''+dbname+'''"'''
    cursor.execute(sql) 
    tablesdict = cursor.fetchall()
    tables=[]
    for i in range(len(tablesdict)):
        tables.append(tablesdict[i]['TABLE_NAME'])
    return tables
#------------------------------------------------------------------------------------------------
def getColumnNamesOfMySQLTable(mysqltable):
    cursor.execute("DESC "+mysqltable) 
    colsdict = cursor.fetchall()
    cols=[]
    for i in range(len(colsdict)):
        cols.append(colsdict[i]['Field']) #show column names of the specified table
    return cols
#------------------------------------------------------------------------------------------------
def displayPandasTable(frame,r,df):
    pandasTableFRM = Frame(frame)
    pandasTableFRM.grid(row=r, column=1, sticky='NW')
    #pt = Table(pandasTableFRM, dataframe=df, showtoolbar=True, width=w, showstatusbar=True)
    pt = Table(pandasTableFRM, dataframe=df, showtoolbar=True, showstatusbar=True)
    pt.cellbackgr = 'orange'
    pt.grid()
    pt.show()
    global globaldf
    globaldf = df #for reference from within other functions
#------------------------------------------------------------------------------------------------
def index(rootframe):
    topframe = Toplevel()
    '''
    '''
    r=0
    #display tablenames of the given mysql database in combo box
    tables = getTablenamesOfMySQLDatabase(mydatabase)
    Label(topframe, text="Select Table").grid(row=r, column=0, sticky='W')
    cboTables = ttk.Combobox(topframe, values=tables)
    cboTables.current(0)
    cboTables.grid(row=r, column=1, sticky='W')
    def cboTablesSelectedEvent(event):#display columns of the selected table
        cols = getColumnNamesOfMySQLTable(cboTables.get())
        cboColumns['values'] = cols
        cboColumns.current(0)
        #df=createDataFrame(cboTables.get())
        numofrows = getNumOfRowsOfMySQLTable(cboTables.get())
        numofrowstxt.delete(0,END)    
        numofrowstxt.insert(INSERT, numofrows)
        #numofrowstxt.get('1.0', 'end-1c'))
        df = getDataFrameFromMySQLTable(cboTables.get())
        displayPandasTable(topframe, r+1, df)
    cboTables.bind("<<ComboboxSelected>>", cboTablesSelectedEvent)
    #display No. of rows in the selected table
    r+=1
    Label(topframe, text="No. of rows in table").grid(row=r, column=0, sticky=W)
    numofrowstxt = Entry(topframe, width=30)
    numofrowstxt.grid(row=r, column=1, sticky='W')

    r+=1
    #display column names of the given mysql table in combo box
    r+=1
    Label(topframe, text="Columns in the selected table").grid(row=r, column=0, sticky='E')
    cboColumns=ttk.Combobox(topframe, values=tables)
    cboColumns.grid(row=r, column=1, sticky='W')
    r+=1
    Label(topframe, text="SQL Query").grid(row=r, column=0, sticky='W')
    #sqlTXT.delete('1.0', END)
    #sqlTXT.insert(INSERT, txt)
    sqlTXT = Text(topframe, height=3, width=80)
    sqlTXT.grid(row=r, column=1, sticky='W')
    def sqlQuerySubmitBTNClickEvent():
        sql = sqlTXT.get()
        df = getDataFrameFromSQLQuery(sql)
        displayPandasTable(topframe, r+1, df)        
    r+=1
    Button(topframe, text="Submit SQL Query", command=sqlQuerySubmitBTNClickEvent).grid(row=r, column=1, sticky='E')    
    r+=1          
    def openCSVFileBtnClickEvent():
        df = getDataFrameFromCSVFile()
        displayPandasTable(topframe, r+1, df)
    Button(topframe, text='Open CSV file', command=openCSVFileBtnClickEvent).grid(row=r, column=1, sticky='W')
    r+=1   
    def saveDFasCSVFileBtnClickEvent():
        global globaldf
        savedisplayedDFasCSVFile(globaldf)
        msg = "CSV File saved."
        tk.messagebox.showinfo("MESSAGE", msg, parent=topframe)  
    Button(topframe, text='Save DF as CSV file', command=saveDFasCSVFileBtnClickEvent).grid(row=r, column=1, sticky='W')
    r+=1 
    def saveDFtoMySQLTableSQLEngineBtnClickEvent():
        global globaldf
        savedisplayedDFtoMySQLTableSQLEngine(topframe, globaldf, cboTables.get())
        msg = "Data saved in selected MySQL table."
        tk.messagebox.showinfo("MESSAGE", msg, parent=topframe)  
    Button(topframe, text='Save displayed DF to selected MySQL Table using SQLEngine', command=saveDFtoMySQLTableSQLEngineBtnClickEvent).grid(row=r, column=1, sticky='W')

    r+=1 
    def saveDFtoMySQLTableInsertBtnClickEvent():
        global globaldf
        savedisplayedDFtoMySQLTableInsert(topframe, globaldf, cboTables.get())
        msg = "Data saved in selected MySQL table."
        tk.messagebox.showinfo("MESSAGE", msg, parent=topframe)  
    Button(topframe, text='INSERT displayed DF to selected MySQL Table', command=saveDFtoMySQLTableInsertBtnClickEvent).grid(row=r, column=1, sticky='W')
    r+=1 
    def saveDFtoMySQLTableUpdateBtnClickEvent():
        global globaldf
        savedisplayedDFtoMySQLTableUpdate(topframe, globaldf, cboTables.get())
        msg = "Data saved in selected MySQL table."
        tk.messagebox.showinfo("MESSAGE", msg, parent=topframe)  
    Button(topframe, text='UPDATE displayed DF to selected MySQL Table', command=saveDFtoMySQLTableUpdateBtnClickEvent).grid(row=r, column=1, sticky='W')

#------------------------------------------------------------------------------------------------
#=============================================================================
# standalone start for code testing - to run this file independently
#=============================================================================
if __name__ == "__main__":
        rootframe = Tk()
        index(rootframe)        
#=============================================================================

