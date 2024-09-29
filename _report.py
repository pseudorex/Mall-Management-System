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
    colCheckboxesFRM = Frame(selectrootframe, width=w)
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
        pt.cellbackgr = 'paleturquoise1'
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
        frame = Frame(selectrootframe, width=w)
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
        if len(lookupvals)>0:
            tablesCBO.current(0)
            df = table2df(frame,lookupvals[0])
            dfColumns = descTable(frame,lookupvals[0])
        def tablesCBOSelectedEvent(event):
            '''    
            r=0;c=0
            inputFrame(selectrootframe,param,r,c)        
            r=0;c=1
            createPandasTableFRM(selectrootframe,df,r,c)
            r=1;c=1
            createColumnCheckBoxesFRM(selectrootframe,table,df,r,c)
            '''
            # !Important - use "selectrootframe" frame and not this "frame"
            table = event.widget.get()
            df = table2df(selectrootframe,table)
            columnFindCBO['values'] = df.columns.tolist()
            dfColumns = descTable(selectrootframe,table)
            pandasTableFRM.destroy()
            createPandasTableFRM(selectrootframe, df, 0, 1)
            colCheckboxesFRM.destroy()
            createColumnCheckBoxesFRM(selectrootframe, table, df, 1, 1)
        tablesCBO.bind("<<ComboboxSelected>>", tablesCBOSelectedEvent)
        r += 1
        Label(frame, text='PRIMARY KEY:').grid(row=r, column=0, sticky='NW')
        Label(frame, text=pk).grid(row=r, column=1, sticky='NW')
        r += 1
        Label(frame, text='LOOKUP VALUES (CBO):').grid(row=r, column=0, sticky='NW')
        Label(frame, text=pk).grid(row=r, column=1, sticky='NW')


        r += 1
        #sub frame #1
        frame1 = Frame(frame, bg="pink1")
        frame1.grid(row=r, column=0, columnspan=2, sticky='NW')  #W-left, E-right, N-top, S-bottom
        # search / Find What
        r=0
        Label(frame1, text='Find what:').grid(row=r, column=0, sticky='NW')
        findWhatTXT = Entry(frame1, width=30)
        findWhatTXT.grid(row=r, column=1, sticky='NW')
        r += 1
        Label(frame1, text='compare').grid(row=r, column=0, sticky='NW')
        operatorfind = StringVar()
        operatorFindCBO = Combobox(frame1, name='operatorFindCBO', width=10, textvariable=operatorfind)
        operatorFindCBO['values'] = ['=','<>','>','<','>=','<=','between','like','in']
        operatorFindCBO.grid(row=r, column=1, sticky='NW')
        operatorFindCBO.current(0)
        r += 1
        Label(frame1, text='in column').grid(row=r, column=0, sticky='NW')
        columnfind = StringVar()
        columnFindCBO = Combobox(frame1, name='columnFindCBO', width=30, textvariable=columnfind)
        #columnFindCBO['values'] = lookupvals
        columnFindCBO.grid(row=r, column=1, sticky='NW')
        r += 1
        def searchTableButtonClickEventStart():
            table = tablesCBO.get()
            column = columnFindCBO.get()
            value = findWhatTXT.get()
            df = searchTableButtonClickEvent(frame1,table,column,value)
            createPandasTableFRM(selectrootframe, df)
        searchTableButton = Button(frame1, text='Search Table', width=20, command=searchTableButtonClickEventStart)
        searchTableButton.grid(row=r, column=1, sticky='EW')

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
                #for sql query use raw string
                sql = sqlQueryTXT.get("1.0",'end-1c') #for TEXT use -  textbox1.get("1.0",'end-1c')
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
                
        sqlQueryExecutionButton = Button(frame2, text='SQL Query Execution', width=20, command=sqlQueryExecutionButtonClickEventStart)
        sqlQueryExecutionButton.grid(row=r, column=1, sticky='EW')



        for widget in frame.winfo_children():
                widget.grid(padx=10, pady=10)        

        for widget in frame1.winfo_children():
                widget.grid(padx=10, pady=10)        

        for widget in frame2.winfo_children():
                widget.grid(padx=10, pady=10)        
        
#=============================================================================
# root frame
#=============================================================================
def createSelectRootFrame(rootframe, param):
        
        w, h = rootframe.winfo_screenwidth()-50, rootframe.winfo_screenheight()-150
        selectrootframe = Toplevel(rootframe)
        selectrootframe.geometry("%dx%d+15+60" % (w, h)) 
        selectrootframe.title("DATA REPORT")

        table = param['table'][0]  
        df = table2df(selectrootframe,table)
        r=0;c=0
        inputFrame(selectrootframe,param,r,c)        
        r=0;c=1
        createPandasTableFRM(selectrootframe,df,r,c)
        r=1;c=1      
        createColumnCheckBoxesFRM(selectrootframe,table,df,r,c)
        '''
        #fire tablescbo combobox click-event programmatically
        idx = lookupvals.index(table)
        tablesCBO.current(idx)
        tablesCBO.event_generate('<<ComboboxSelected>>')
        '''
#=============================================================================
# standalone start
#=============================================================================
param = {'table':['item'],'pk':['itemcode'],'cbo':['itemcategory.itemcategory']}
if __name__ == "__main__":
        rootframe = Tk()
        createSelectRootFrame(rootframe, param)
#=============================================================================

