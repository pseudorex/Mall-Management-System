from _libraryAndDBConnection import * #includes database connection and cursor setting strings
#-----------------------------------------------------------------------------
# pandastable frame      r=1 c=0
# colcheckboxes frame    r=2 c=0
# insertDataInput frame  r=0 c=1
#-----------------------------------------------------------------------------
global tablesCBO
global pandasTableFRM
global colCheckboxesFRM
#-----------------------------------------------------------------------------
def sqlQueryExecution(frame, sql): #all SQL queries except SELECT & DESC
        #database name is globally accessible, so need not pass it on to this function
        try:
                cursor.execute(sql)
                conn.commit()
                msg = "SUCCESS: SQL query executed successfully."
                tk.messagebox.showinfo("MESSAGE", msg, parent=frame)        
                #return msg
        except conn.Error as e:
                msg = "ERROR: "+str(e.args[0])+e.args[1]
                #return msg              
                tk.messagebox.showinfo("MESSAGE", msg, parent=frame)        
#-----------------------------------------------------------------------------
def showTablesInADatabase(frame):
        #database name is globally accessible, so need not pass it on to this function
        try:
                cursor.execute("SHOW TABLES")
                result = cursor.fetchall() #result: list of dictionary
                tables=[]
                for i in result:
                        tables.append(*i.values()) #use * to explode the dictionary so as to enlist values only
                return tables
        except conn.Error as e:
                msg = "ERROR: "+str(e.args[0])+e.args[1]
                tk.messagebox.showinfo("MESSAGE", msg, parent=frame)
#-----------------------------------------------------------------------------
def descTable(frame, table):
        try:
                sql = "desc "+table
                #cursor = conn.cursor()
                cursor.execute(sql)
                data = cursor.fetchall() #list of dict with one common key 'Field'
                df = pd.DataFrame(data)
                return df
        except conn.Error as e:
                msg = "ERROR: "+str(e.args[0])+e.args[1]
                tk.messagebox.showinfo("MESSAGE", msg, parent=frame)
#-----------------------------------------------------------------------------
def getPrimaryKeyColumn(frame, table):
        #mydb = _libraryAndDBConnection.mydatabase
        mydb = mydatabase
        try:
                sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '" + mydb + \
                      "' AND TABLE_NAME = '" + table + "' AND COLUMN_KEY = 'PRI'"
                #print(mydb, '  ',table, '  ',sql)
                print("STARTED: ",mydb)
                cursor.execute(sql)
                result = cursor.fetchall() #result: list of dictionary                
                #print("result: ",result)
                col = []
                for d in result:
                        col.append(d['COLUMN_NAME'])
                #print(col)
                return col
        except conn.Error as e:
                msg = "ERROR: "+str(e.args[0])+e.args[1]
                tk.messagebox.showinfo("MESSAGE", msg, parent=frame)
#-----------------------------------------------------------------------------
def table2df(frame='', table='', columns='*', condition='1=1'):
        try:
                sql = "select "+columns+" from "+table+" where "+condition
                #cursor = conn.cursor()
                cursor.execute(sql)
                data = cursor.fetchall()
                df = pd.DataFrame(data)
                return df
        except conn.Error as e:
                msg = "ERROR: "+str(e.args[0])+e.args[1]
                tk.messagebox.showinfo("MESSAGE", msg, parent=frame)
#-----------------------------------------------------------------------------
def table2dfSQLQuery(frame='', sql=''):
        try:
                cursor.execute(sql)
                data = cursor.fetchall()
                df = pd.DataFrame(data)
                return df
        except conn.Error as e:
                msg = "ERROR: "+str(e.args[0])+e.args[1]
                tk.messagebox.showinfo("MESSAGE", msg, parent=frame)
#-----------------------------------------------------------------------------
def searchTableButtonClickEvent(frame,table,column,value):
        try:
                sql = "select * from "+table+" where "+column+"='"+value+"'"
                #cursor = conn.cursor()
                cursor.execute(sql)
                data = cursor.fetchall()
                df = pd.DataFrame(data)
                return df
        except conn.Error as e:
                msg = "ERROR: "+str(e.args[0])+e.args[1]
                tk.messagebox.showinfo("MESSAGE", msg, parent=frame)
#-----------------------------------------------------------------------------
def updateARow(rowDataList): #rowDataList is a series
        try:
                frameUpdateTable = Toplevel()  #create a pop-up window
                frameUpdateTable.title("Update Table")
                frameUpdateTable.geometry()
                frameUpdateTable.configure(background='aqua')
                r = 0
                for colname in rowDataList.index:
                        #print(i,' -- ',rowDataList[colname])
                        Label(frameUpdateTable, text=colname, bg='aqua') \
                                                           .grid(row=r, column=1, padx=15, pady=5, sticky='E')
                        e = Entry(frameUpdateTable)
                        e.grid(row=r, column=2, padx=15, pady=5)
                        e.insert(INSERT, rowDataList[colname])
                        r += 1
                def updateTableSubmitButtonClickEvent():
                        pass
                updateTableSubmitButton = Button(frameUpdateTable, text="Update", command=updateTableSubmitButtonClickEvent)
                updateTableSubmitButton.grid(row=r, column=2, padx=10, pady=10)
        except conn.Error as e:
                msg = "ERROR: "+str(e.args[0])+e.args[1]
                tk.messagebox.showinfo("MESSAGE", msg, parent=frameUpdateTable)
        
#-----------------------------------------------------------------------------
def createColumnCheckBoxesFRM(selectrootframe, table, df, r=1, col=1):

    global tablesCBO
    global colCheckboxesFRM
    
    w, h = selectrootframe.winfo_screenwidth()-120, selectrootframe.winfo_screenheight()-160
    w = w*20/100
    numOfCols = len(df.columns.tolist())
    colCheckboxesFRM = Frame(selectrootframe, width=w, bg = 'darkolivegreen1')
    #colCheckboxesFRM.grid(row=r, column=0, columnspan=numOfCols, sticky='NW', padx=15, pady=15)  #NW-top left
    colCheckboxesFRM.grid(row=r, column=col, sticky='NW', padx=15, pady=15)  #NW-top left
    r = 1
    col = 0
    for c in df.columns.tolist():    
        globals()[c+'VAR'] = IntVar()
        globals()[c+'VAR'].set(0)
        globals()[c+'CHK'] = ttk.Checkbutton(colCheckboxesFRM,variable=globals()[c+'VAR'],text=c, onvalue=1, offvalue=0)
        globals()[c+'CHK'].grid(column=col, row=r, sticky='W')
        col+=1
    r+=1
    def getCheckedBoxesButtonClickEvent(df):
            checkedColumnsLST = []
            for c in df.columns.tolist():
                    if globals()[c+'VAR'].get()==1:
                            checkedColumnsLST.append(c)
            cols=''
            for c in checkedColumnsLST:
                   cols += c + ","
            cols = cols[:-1]
            df = table2df(colCheckboxesFRM, table, cols) 
            createPandasTableFRM(selectrootframe, df)  #!IMPORTANT - use selectrootframe
    getCheckedBoxesButton = Button(colCheckboxesFRM, text='Submit List of Selected Columns', \
                                   command=lambda: getCheckedBoxesButtonClickEvent(df))
    getCheckedBoxesButton.grid(row=r, column=0, columnspan=numOfCols, sticky='EW')
    
    for widget in colCheckboxesFRM.winfo_children():
        widget.grid(padx=0, pady=3)

#=============================================================================
def createPandasTableFRM(frame, df, r=0, c=1):
        global pandasTableFRM
        w, h = frame.winfo_screenwidth()-120, frame.winfo_screenheight()-160
        w = w*60/100
        pandasTableFRM = Frame(frame, height=h, width=w)
        pandasTableFRM.grid(row=r, column=c, sticky='NW')
        pt = Table(pandasTableFRM, dataframe=df, showtoolbar=True, width=w, showstatusbar=True)  
        pt.cellbackgr = 'lightgoldenrod1'
        pt.grid()
        pt.show()
        #for insert disable the following event handling; enable it for update only
        def leftButtonClickEvent(event): #left-button click event handling
                rowclicked = pt.get_row_clicked(event)
                rowDataList = pt.model.df.loc[rowclicked] #Series
                updateARow(rowDataList)
        pt.rowheader.bind('<Button-1>',leftButtonClickEvent)
#=============================================================================
def inputFrame(selectrootframe, param, r=0, c=0):

        global tablesCBO
        global colCheckboxesFRM
        global pandasTableFRM

        
        table = param['table'][0]
        pk = param['pk'][0]
        cbo = param['cbo'][0]
        
        
        w, h = selectrootframe.winfo_screenwidth()-120, selectrootframe.winfo_screenheight()-160
        w = w*30/100
        #frame = Frame(selectrootframe, height=h, width=w)
        frame = Frame(selectrootframe, width=w, bg = 'darkolivegreen1')
        frame.grid(row=r, column=c, rowspan=2, sticky='NW')#W-left, E-right, N-top, S-bottom

        df = table2df(frame,table)
        dfColumns = descTable(frame,table)

        r=0
        Label(frame, text='TABLES:').grid(row=r, column=0, sticky='NW')
        tables = StringVar()
        tablesCBO = Combobox(frame, name='tablecbo', width=27)#, textvariable=tablesCBOvar) #,width=30)
        lookupvals = showTablesInADatabase(frame)
        tablesCBO['values'] = lookupvals
        tablesCBO.grid(row=r, column=1, sticky='NW')
        
        idx = lookupvals.index(table)
        tablesCBO.current(idx)
        
        df = table2df(frame,lookupvals[0])
        dfColumns = descTable(frame,lookupvals[0])
        '''
        if len(lookupvals)>0:
            tablesCBO.current(0)
            df = table2df(frame,lookupvals[0])
            dfColumns = descTable(frame,lookupvals[0])
        '''
        def tablesCBOSelectedEvent(event):
            # !Important - use "selectrootframe" frame and not this "frame" #pass row and col for child frames
            table = event.widget.get()
            pk = getPrimaryKeyColumn(frame, table)
            #print(table, event.widget._name)
            df = table2df(frame,table)
            updateColCBO['values'] = df.columns.tolist()
            whereColCBO['values'] = df.columns.tolist()
            
            dfColumns = descTable(selectrootframe,table)
            if pkTXT.winfo_exists()== 1:
                    #pkTXT.delete('1.0', END)
                    #pkTXT.delete()
                    pkTXT.delete(0, END)
            pkTXT.insert(INSERT,"")
            pkTXT.insert(INSERT,pk)        
            if pandasTableFRM.winfo_exists()== 1:    
                    pandasTableFRM.destroy()
            createPandasTableFRM(selectrootframe, df, 0, 1)
            if colCheckboxesFRM.winfo_exists()== 1:    
                    colCheckboxesFRM.destroy()
            createColumnCheckBoxesFRM(selectrootframe, table, df, 1, 1)
        tablesCBO.bind("<<ComboboxSelected>>", tablesCBOSelectedEvent)

        r += 1
        Label(frame, text='PRIMARY KEY:').grid(row=r, column=0, sticky='NW')
        pkTXT = Entry(frame, width=30)
        pkTXT.grid(row=r, column=1, sticky='NW')
        #pkTXT.delete('1.0', END)
        pkTXT.delete(0,END) #for Entry (0,END)
        pkTXT.insert(INSERT,pk)        
        '''        
        Label(frame, text=pk).grid(row=r, column=1, sticky='NW')
        r += 1
        Label(frame, text='LOOKUP VALUES (CBO):').grid(row=r, column=0, sticky='NW')
        Label(frame, text=pk).grid(row=r, column=1, sticky='NW')
        '''

        r += 1
        #sub frame #1
        frame1 = Frame(frame, bg="mediumorchid1")
        frame1.grid(row=r, column=0, columnspan=2, sticky='NW')  #W-left, E-right, N-top, S-bottom
        # Update what & with what
        r=0
        Label(frame1, text='Update column').grid(row=r, column=0, sticky='NW')
        updateColvar = StringVar()
        updateColCBO = Combobox(frame1, name='updateColCBO', width=30, textvariable=updateColvar)
        updateColCBO.grid(row=r, column=1, sticky='NW')
        table = tablesCBO.get()
        df = table2df(frame1,table)
        updateColCBO['values'] = df.columns.tolist()
        updateColCBO.current(0)

        r += 1
        Label(frame1, text='With (New data value):').grid(row=r, column=0, sticky='NW')
        updateValTXT = Entry(frame1, width=30)
        updateValTXT.grid(row=r, column=1, sticky='NW')
        r += 1
        # Update Condition
        Label(frame1, text='Where (Condition):').grid(row=r, column=0, sticky='NW')
        whereCol = StringVar()
        whereColCBO = Combobox(frame1, name='whereColCBO', width=30, textvariable=whereCol)
        whereColCBO.grid(row=r, column=1, sticky='NW')
        df = table2df(frame1,table)
        whereColCBO['values'] = df.columns.tolist()
        
        r += 1
        Label(frame1, text='compare').grid(row=r, column=0, sticky='NW')
        whereOp = StringVar()
        whereOpCBO = Combobox(frame1, name='whereOpCBO', width=10, textvariable=whereOp)
        whereOpCBO['values'] = ['=','<>','>','<','>=','<=','between','like','in']
        whereOpCBO.grid(row=r, column=1, sticky='NW')
        whereOpCBO.current(0)
        r += 1
        whereValTXT = Entry(frame1, width=30)
        whereValTXT.grid(row=r, column=1, sticky='NW')
        r += 1
        def createUpdateQueryBTNEvent():
            table = tablesCBO.get()
            column = updateColCBO.get()
            value = updateValTXT.get()
            condition = whereColCBO.get()+whereOpCBO.get()+"'"+whereValTXT.get()+"'"

            sql = "UPDATE "+table+" SET "+column+"='"+value+"' WHERE "+condition
            print(sql)
            sqlQueryTXT.delete('1.0', END) #for Text ('1.0', END)
            sqlQueryTXT.insert(INSERT, sql)
            
            #df = searchTableButtonClickEvent(frame1,table,column,value)
            #createPandasTableFRM(selectrootframe, df)
            
        createUpdateQueryBTN = Button(frame1, text='Create Update SQL Query (execute the following query)', \
                           width=20, command=createUpdateQueryBTNEvent)
        createUpdateQueryBTN.grid(row=r, column=0, columnspan=2, sticky='EW')

        r += 1
        #sub frame #2
        # General SQL Query Execution
        frame2 = Frame(frame)
        frame2.grid(row=r, column=0, columnspan=2, sticky='NW')  #W-left, E-right, N-top, S-bottom

        Label(frame2, text='Raw SQL Query (Select only):').grid(row=r, column=0, columnspan=2, sticky='NW')
        r += 1
        sqlQueryTXT = Text(frame2, width=35, height=6)
        sqlQueryTXT.grid(row=r, column=0, columnspan=2, sticky='NW')
        r += 1
        def sqlQueryExecutionButtonClickEventStart():
                '''
                #####For SELECT query
                #for sql query use raw string
                sql = sqlQueryTXT.get("1.0",'end-1c') #for TEXT use -  textbox1.get("1.0",'end-1c') #For entry txt.get()
                #sqlQueryExecution(frame2, sql)
                #print("SQL: ",sql)
                #TO GET THE TABLE NAME FROM A SQL QUERY!!!!!!!!!!!!!!!
                #sql="select * from   item    where a=1";
                idx1 = sql.find("from");
                idx2 = sql[idx1+4:].strip().find(" ");
                idx3 = sql.find(" ",idx1+4+idx2-1);
                idx4=sql[idx1+4+idx2-1:].strip().find(" ");
                table = sql[idx1+4+idx2-1:idx3]
                #print(table)
                df = table2dfSQLQuery(frame2, sql)
                pandasTableFRM.destroy()
                colCheckboxesFRM.destroy()           
                createPandasTableFRM(selectrootframe, df, 0, 1)
                createColumnCheckBoxesFRM(selectrootframe, table, df, 1, 1)
                df = table2dfSQLQuery(frame2, sql)
                pandasTableFRM.destroy()
                colCheckboxesFRM.destroy()           
                createPandasTableFRM(selectrootframe, df, 0, 1)
                createColumnCheckBoxesFRM(selectrootframe, table, df, 1, 1)
                '''
                sql = sqlQueryTXT.get("1.0",'end-1c') #for TEXT use -  textbox1.get("1.0",'end-1c') #For entry txt.get()
                sqlQueryExecution(frame, sql)


                #refresh df and then pandastable to show updated values
                table = tablesCBO.get()
                df = table2df(frame, table)
                #createPandasTableFRM(frameUpdateTable, df, param)
                global pandasTableFRM
                pt = Table(pandasTableFRM, dataframe=df)
                pt.cellbackgr = 'aqua'
                pt.grid()
                pt.show()

                
        sqlQueryExecutionButton = Button(frame2, text='SQL Query Execution', width=20, command=sqlQueryExecutionButtonClickEventStart)
        sqlQueryExecutionButton.grid(row=r, column=1, sticky='EW')


        for widget in frame.winfo_children():
                widget.grid(padx=10, pady=10)        

        for widget in frame1.winfo_children():
                widget.grid(padx=10, pady=10)        

        for widget in frame2.winfo_children():
                widget.grid(padx=10, pady=10)        
        
        '''
        #fire tablescbo combobox click-event programmatically
        idx = lookupvals.index(table)
        tablesCBO.current(idx)
        #print(idx, tablesCBO.current(idx), lookupvals[idx])
        tablesCBO.event_generate('<<ComboboxSelected>>')
        '''

#=============================================================================
# root frame
#=============================================================================
def createEditRootFrame(rootframe, param):

        #decalre here before creating root frame as their existance is to be verified during startup
        global pandasTableFRM
        global colCheckboxesFRM
        pandasTableFRM = Frame()
        colCheckboxesFRM = Frame()

        w, h = rootframe.winfo_screenwidth()-50, rootframe.winfo_screenheight()-150
        selectrootframe = Toplevel(rootframe)
        selectrootframe.geometry("%dx%d+15+60" % (w, h)) 
        selectrootframe.title("DATA REPORT")
        selectrootframe.configure(bg = 'darkolivegreen1')

        table = param['table'][0]  
        df = table2df(selectrootframe,table)
        r=0;c=0
        inputFrame(selectrootframe,param,r,c)        
        r=0;c=1
        createPandasTableFRM(selectrootframe,df,r,c)
        r=1;c=1      
        createColumnCheckBoxesFRM(selectrootframe,table,df,r,c)

#=============================================================================
# standalone start
#=============================================================================
param = {'table':['item'],'pk':['itemcode'],'cbo':['itemcategory.itemcategory']}
if __name__ == "__main__":
        rootframe = Tk()
        createEditRootFrame(rootframe, param)
#=============================================================================

