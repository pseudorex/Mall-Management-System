from _libraryAndDBConnection import * #includes database connection and cursor setting strings
#-----------------------------------------------------------------------------
#Create global widget for their easy access across the frames
global tablesCBO
global pandasTableFRM

#pandastable frame r=1 c=0
#colcheckboxes frame r=2 c=0
#insertDataInput frame r=0 c=1

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
def updateARow(rowDataList,param): #rowDataList is a series


        #if there are multiple comboboxes for a table
        cbocolslstupdate = []
        for i in range(len(param['cbo'])):
                v = param['cbo'][i]
                v = v[v.find('.')+1:]
                cbocolslstupdate.append(v)


        
        try:
                frameUpdateTable = Toplevel()  #create a pop-up window
                frameUpdateTable.title("Update Table")
                frameUpdateTable.geometry()
                frameUpdateTable.configure(background='aquamarine1')
                r = 0
                for colname in rowDataList.index:
                        pk = param['pk'][0]
                        #print(i,' -- ',rowDataList[colname])
                        Label(frameUpdateTable, text=colname, bg='blanchedalmond') \
                                                           .grid(row=r, column=1, padx=15, pady=5, sticky='E')
                        if colname==pk:
                                globals()[colname] = Label(frameUpdateTable,text=rowDataList[colname])                               
                        else:
                                globals()[colname] = Entry(frameUpdateTable)
                                globals()[colname].insert(INSERT, rowDataList[colname])
                        globals()[colname].grid(row=r, column=2, padx=15, pady=5)                        


                        #if control is a combobox dropdown pickup
                        #----------------------------------------
                        # cbotbl = cbo[:cbo.find('.')]
                        # cbocol = cbo[cbo.find('.')+1:]
                           
                        #if cbocol ==  colname:
                        if colname in cbocolslstupdate:
                                   i = cbocolslstupdate.index(colname)

                                   cboupdate = param['cbo'][i]
                                   cbotblupdate = cboupdate[:cboupdate.find('.')]
                                   cbocolupdate = cboupdate[cboupdate.find('.')+1:]
                                                                      
                                   colvalsupdate = []
                                   try:
                                           sql = "select "+cbocolupdate+" from "+cbotblupdate+" order by "+cbocolupdate
                                           cursor.execute(sql)
                                           data = cursor.fetchall()
                                           dfcboupdate = pd.DataFrame(data)
                                           #print(dfcbo)
                                           colvalsupdate = dfcboupdate.iloc[:,0].tolist()
                                   except conn.Error as e:
                                           msg = "ERROR: "+str(e.args[0])+e.args[1]
                                           tk.messagebox.showinfo("MESSAGE", msg, parent=frame)
                                   #globals()[colname+'CBO'] = Combobox(insertDataInputFRM)
                                   globals()[colname+'updateCBO'] = Combobox(frameUpdateTable, name=cbocolupdate)  # !important to name the combobox for accessing it later
                                   globals()[colname+'updateCBO'].grid(row=r, column=4, padx=15, pady=5)
                                   globals()[colname+'updateCBO']['values'] = colvalsupdate
                                   def funcSelectedEvent(event):
                                           '''
                                           #print(event.widget)     
                                           print(event.widget._name)  # use name assigned to the combobox
                                           '''
                                           #val = globals()[colname+'CBO'].get()
                                           
                                           val = globals()[event.widget._name+'updateCBO'].get()
                                           globals()[event.widget._name].delete(0, END)
                                           globals()[event.widget._name].insert(INSERT, val)
                                           
                                   globals()[colname+'updateCBO'].bind("<<ComboboxSelected>>", funcSelectedEvent)




                        r += 1
                def updateTableSubmitButtonClickEvent():
                        #pass
                        table = param['table'][0]
                        pk = param['pk'][0]
                        sql = "UPDATE "+table+" SET "
                        for colname in rowDataList.index:                        
                                if colname==pk:
                                        pkval = globals()[colname].cget("text")  #to read the text of a label
                                        condition = " where "+colname+"='"+pkval+"'"
                                else:
                                        sql += colname+"='"+globals()[colname].get()+"'," #to read the text of an entry
                        sql = sql[:-1]
                        sql += " "+condition
                        print(sql)
                        sqlQueryExecution(frameUpdateTable, sql) #execute update query

                        #refresh df and then pandastable to show updated values
                        df = table2df(frameUpdateTable, table)
                        #createPandasTableFRM(frameUpdateTable, df, param)
                        global pandasTableFRM
                        pt = Table(pandasTableFRM, dataframe=df)
                        pt.cellbackgr = 'darkolivegreen1'
                        pt.grid()
                        pt.show()
                        
                updateTableSubmitButton = Button(frameUpdateTable, text="Update", command=updateTableSubmitButtonClickEvent)
                updateTableSubmitButton.grid(row=r, column=2, padx=10, pady=10)




                def deleteRowSubmitButtonClickEvent():
                        #pass
                        table = param['table'][0]
                        pk = param['pk'][0]
                        sql = "DELETE FROM "+table
                        for colname in rowDataList.index:                        
                                if colname==pk:
                                        pkval = globals()[colname].cget("text")  #to read the text of a label
                                        condition = " where "+colname+"='"+pkval+"'"
                        sql += " "+condition
                        print(sql)
                        sqlQueryExecution(frameUpdateTable, sql) #execute update query

                        #refresh df and then pandastable to show updated values
                        df = table2df(frameUpdateTable, table)
                        #createPandasTableFRM(frameUpdateTable, df, param)
                        global pandasTableFRM
                        pt = Table(pandasTableFRM, dataframe=df)
                        pt.cellbackgr = 'darkolivegreen1'
                        pt.grid()
                        pt.show()
                        
                deleteRowSubmitButton = Button(frameUpdateTable, text="DELETE", command=deleteRowSubmitButtonClickEvent)
                deleteRowSubmitButton.grid(row=r, column=3, padx=10, pady=10)





        except conn.Error as e:
                msg = "ERROR: "+str(e.args[0])+e.args[1]
                tk.messagebox.showinfo("MESSAGE", msg, parent=frameUpdateTable)
        
#-----------------------------------------------------------------------------
def createColumnCheckBoxesFRM(insertframe, table, df, r=2, col=0):

    #pandastable frame r=1 c=0
    #colcheckboxes frame r=2 c=0
    #insertDataInput frame r=0 c=1

    global tablesCBO
    w, h = insertframe.winfo_screenwidth()-120, insertframe.winfo_screenheight()-160
    w = w*20/100
    numOfCols = len(df.columns.tolist())
    frame = Frame(insertframe, width=w)
    #frame.grid(row=r, column=0, columnspan=numOfCols, sticky='NW', padx=15, pady=15)  #NW-top left
    #frame.grid(row=r, column=0, sticky='NW', padx=15, pady=15)  #NW-top left

    # r=1 c=0 colspan=2    
    frame.grid(row=r, column=0, columnspan=2, sticky='NW', padx=15, pady=15)  #NW-top left

    r = 1
    col = 0
    for c in df.columns.tolist():    
        globals()[c+'VAR'] = IntVar()
        globals()[c+'VAR'].set(0)
        globals()[c+'CHK'] = ttk.Checkbutton(frame,variable=globals()[c+'VAR'],text=c, onvalue=1, offvalue=0)
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
            df = table2df(insertframe, table, cols) 
            createPandasTableFRM(insertframe, df)
    getCheckedBoxesButton = Button(frame, text='Submit List of Selected Columns', \
                                   command=lambda: getCheckedBoxesButtonClickEvent(df))
    getCheckedBoxesButton.grid(row=r, column=0, columnspan=numOfCols, sticky='EW')
    
    for widget in frame.winfo_children():
        widget.grid(padx=0, pady=3)

#=============================================================================
def createInsertDataInputFRM(insertframe, table, param={}, r=0, c=1):

        '''
        print(param)
        print(len(param))
        print(param['cbo'])
        print(len(param['cbo']))
        '''

        #if there are multiple comboboxes for a table
        cbocolslst = []
        for i in range(len(param['cbo'])):
                v = param['cbo'][i]
                v = v[v.find('.')+1:]
                cbocolslst.append(v)
                #print(v)        
        #print(cbocolslst)
        
        '''
        #if there are only single combobox for a table
        table = param['table'][0]
        pk = param['pk'][0]
        cbo = param['cbo'][0]
        cbo = param['cbo'][0]
        cbotbl = cbo[:cbo.find('.')]
        cbocol = cbo[cbo.find('.')+1:]
        '''
        mywidth1 = insertframe.winfo_screenwidth()-20
        myheigh1 = insertframe.winfo_screenheight()-100
        original_r = r
        original_c = c
        

        w, h = insertframe.winfo_screenwidth()-120, insertframe.winfo_screenheight()-160
        w = w*40/100
        insertDataInputFRM = Frame(insertframe, height=h, width=w)
        insertDataInputFRM.grid(row=r, column=c, rowspan=2, sticky=W)
        insertDataInputFRM.configure(background='cadetblue1')

        try:
                   df = descTable(insertDataInputFRM,table)
                   df = df['Field']
                   total_rows = df.shape[0]
                   r = 1
                   for i in range(total_rows):
                           '''
                           colname = df[i]
                           Label(insertDataInputFRM, text=colname, bg='yellow') \
                                                           .grid(row=r, column=1, padx=15, pady=5, sticky='E')
                           e = Entry(insertDataInputFRM)
                           e.grid(row=r, column=3, padx=15, pady=5)
                           e.insert(INSERT, '')
                           r += 1
                           '''
                           colname = df[i]
                           Label(insertDataInputFRM, text=colname, bg='cornsilk1') \
                                                           .grid(row=r, column=1, padx=15, pady=5, sticky='E')
                           globals()[colname+'TXT'] = Entry(insertDataInputFRM)
                           globals()[colname+'TXT'].grid(row=r, column=3, padx=15, pady=5)
                           globals()[colname+'TXT'].insert(INSERT, '')




                           #if control is a combobox dropdown pickup
                           #----------------------------------------
                           # cbotbl = cbo[:cbo.find('.')]
                           # cbocol = cbo[cbo.find('.')+1:]
                           
                           #if cbocol ==  colname:
                           if colname in cbocolslst:
                                   i = cbocolslst.index(colname)

                                   cbo = param['cbo'][i]
                                   cbotbl = cbo[:cbo.find('.')]
                                   cbocol = cbo[cbo.find('.')+1:]
                                                                      
                                   colvals = []
                                   try:
                                           sql = "select "+cbocol+" from "+cbotbl+" order by "+cbocol
                                           cursor.execute(sql)
                                           data = cursor.fetchall()
                                           dfcbo = pd.DataFrame(data)
                                           #print(dfcbo)
                                           colvals = dfcbo.iloc[:,0].tolist()
                                   except conn.Error as e:
                                           msg = "ERROR: "+str(e.args[0])+e.args[1]
                                           tk.messagebox.showinfo("MESSAGE", msg, parent=frame)
                                   #globals()[colname+'CBO'] = Combobox(insertDataInputFRM)
                                   globals()[colname+'CBO'] = Combobox(insertDataInputFRM, name=cbocol)  # !important to name the combobox for accessing it later
                                   globals()[colname+'CBO'].grid(row=r, column=4, padx=15, pady=5)
                                   globals()[colname+'CBO']['values'] = colvals
                                   def funcSelectedEvent(event):
                                           '''
                                           #print(event.widget)     
                                           print(event.widget._name)  # use name assigned to the combobox
                                           '''
                                           #val = globals()[colname+'CBO'].get()
                                           
                                           val = globals()[event.widget._name+'CBO'].get()
                                           globals()[event.widget._name+'TXT'].delete(0, END)
                                           globals()[event.widget._name+'TXT'].insert(INSERT, val)
                                           
                                   globals()[colname+'CBO'].bind("<<ComboboxSelected>>", funcSelectedEvent)
            


                           
                           r += 1
                   def insertIntoTableSubmitButtonClickEvent():
                           #pass
                           vals = ''
                           cols = ''
                           for i in range(total_rows):
                                   colname = df[i]
                                   cols += df[i]+","
                                   vals += "'"+globals()[colname+'TXT'].get()+"',"
                           cols = cols[:-1]
                           vals = vals[:-1]

                           sql = " INSERT INTO "+ table +"("+ cols +") VALUES("+ vals +")"
                           
                           '''     
                           print(sql)
                           cursor.execute(sql)
                           conn.commit()                           
                           print(vals)
                           msg = "New row inserted into the table: (" + vals + ")"
                           tk.messagebox.showinfo("MESSAGE", msg, parent=insertDataInputFRM)
                           '''
                           sqlQueryExecution(insertDataInputFRM, sql)

                           #refresh df and then pandastable to show updated values
                           dfpt = table2df(insertDataInputFRM, table)
                           #createPandasTableFRM(frameUpdateTable, df, param)
                           global pandasTableFRM
                           pt = Table(pandasTableFRM, dataframe=dfpt)
                           pt.cellbackgr = 'darkseagreen1'
                           pt.grid()
                           pt.show()


                           
                        
                   insertIntoTableSubmitButton = Button(insertDataInputFRM, text="Insert into table", command=insertIntoTableSubmitButtonClickEvent)
                   insertIntoTableSubmitButton.grid(row=r, column=3, padx=10, pady=10)

        except conn.Error as e:
                   print("ERROR in createInsertDataInputFRM")     
                   msg = "ERROR: "+str(e.args[0])+e.args[1]
                   tk.messagebox.showinfo("MESSAGE", msg, parent=insertDataInputFRM)

#=============================================================================
def createPandasTableFRM(insertframe, df, param={}, r=1, c=0):


        global pandasTableFRM
        original_r = r
        original_c = c
        w, h = insertframe.winfo_screenwidth()-120, insertframe.winfo_screenheight()-160
        w = w*50/100
        pandasTableFRM = Frame(insertframe, height=h, width=w)
        pandasTableFRM.grid(row=r, column=c, sticky='NW')
        pt = Table(pandasTableFRM, dataframe=df, showtoolbar=True, width=w, showstatusbar=True)  
        pt.cellbackgr = 'darkolivegreen1'
        pt.grid()
        pt.show()
        #for insert disable the following event handling; enable it for update only
        def leftButtonClickEvent(event): #left-button click event handling
                rowclicked = pt.get_row_clicked(event)
                rowDataList = pt.model.df.loc[rowclicked] #Series
                updateARow(rowDataList,param)
        pt.rowheader.bind('<Button-1>',leftButtonClickEvent)
#=============================================================================
# child frames
#=============================================================================
def createInsertChildFrames(insertrootframe, param):

        # print(param)
        
        table = param['table'][0]
        pk = param['pk'][0]
        cbo = param['cbo'][0]
        cbotbl = cbo[:cbo.find('.')]
        cbocol = cbo[cbo.find('.')+1:]
        
        
        #common frame r=0 c=0
        r=0
        col = 0
        frame = Frame(insertrootframe)
        frame.configure(bg= 'aquamarine1')
        frame.grid(row=r, column=col, sticky='W', padx=15, pady=15)  #W-left, E-right, N-top, S-bottom
        Label(frame, text='TABLE:', bg = 'aquamarine1').grid(row=0, column=0, sticky=W)
        Label(frame, text=table, bg = 'aquamarine1').grid(row=0, column=1, sticky=W)
        Label(frame, text='PRIMARY KEY:', bg = 'aquamarine1').grid(row=1, column=0, sticky=W)
        Label(frame, text=pk, bg = 'aquamarine1').grid(row=1, column=1, sticky=W)
        Label(frame, text='LOOKUP VALUES (CBO):', bg = 'aquamarine1').grid(row=2, column=0, sticky=W)
        Label(frame, text=cbo, bg = 'aquamarine1').grid(row=2, column=1, sticky=W)
        '''
        Label(frame, text='LOOKUP VALUES (table & column):').grid(row=3, column=0, sticky=W)
        Label(frame, text=cbotbl+" + "+cbocol).grid(row=3, column=1, sticky=W)
        '''

        df = table2df(frame,table)
        dfColumns = descTable(frame,table)
        
        #pandastable frame r=1 c=0
        r+=1
        createPandasTableFRM(insertrootframe, df, param, r, col)
        '''
        #colcheckboxes frame r=2 c=0
        r+=1
        createColumnCheckBoxesFRM(insertrootframe, table, df, r, col)
        '''
        #insertDataInput frame r=0 c=1
        r=0
        col = 1
        createInsertDataInputFRM(insertrootframe, table, param, r, col)

        #colcheckboxes frame r=2 c=0
        #r+=1
        r = 2
        col = 0
        colspan = 2
        createColumnCheckBoxesFRM(insertrootframe, table, df, r, col)


        for widget in frame.winfo_children():
                widget.grid(padx=0, pady=5)        
#=============================================================================
def extra():
    '''    
    if len(args)>0:
            print("Parameters #2: ",args," Total: ",len(args))
            print("Table #2: ",args[0][1])        
    '''
    def tablesCBOSelectedEvent(event):
            table = event.widget.get()
            df = table2df(root,table)
            columnFindCBO['values'] = df.columns.tolist()
            columnReplaceCBO['values'] = df.columns.tolist()
            dfColumns = descTable(root,table)
            #setPrimaryKey(dfColumns)
            setPrimaryKey(table)
            pandasTableFRM.destroy()
            createPandasTableFRM(root, df)
            createColumnCheckBoxesFRM(root, df)
    tablesCBO.bind("<<ComboboxSelected>>", tablesCBOSelectedEvent)


    #create two more frames within root frame
    createPandasTableFRM(root, df)
    createColumnCheckBoxesFRM(root, df)
    
    #-------------------------start a new frame here    
    #CRUD controls
    r = 0
    def insertIntoTableButtonClickEvent():

           print("START #1")
                 
           try:
                   table = tablesCBO.get()
                   df = descTable(root,table)
                   df = df['Field']
                   frameInsertIntoTable = Toplevel()
                   frameInsertIntoTable.title("Insert Row Into Table")
                   frameInsertIntoTable.geometry()
                   frameInsertIntoTable.configure(background='honeydew2')
                   total_rows = df.shape[0]
                   r = 0
                   for i in range(total_rows):
                           '''
                           colname = df[i]
                           Label(frameInsertIntoTable, text=colname, bg='yellow') \
                                                           .grid(row=r, column=1, padx=15, pady=5, sticky='E')
                           e = Entry(frameInsertIntoTable)
                           e.grid(row=r, column=3, padx=15, pady=5)
                           e.insert(INSERT, '')
                           '''
                           colname = df[i]
                           Label(frameInsertIntoTable, text=colname, bg='honeydew2') \
                                                           .grid(row=r, column=1, padx=15, pady=5, sticky='E')
                           globals()[colname+'TXT'] = Entry(frameInsertIntoTable)
                           globals()[colname+'TXT'].grid(row=r, column=3, padx=15, pady=5)
                           globals()[colname+'TXT'].insert(INSERT, '')
                           
                           r += 1
                   def insertIntoTableSubmitButtonClickEvent():

                           print("START #2")
                           
                           vals = ''
                           for i in range(total_rows):
                                   colname = df[i]
                                   vals += globals()[colname+'TXT'].get('1.0','end-1c')
                           msg = vals
                           tk.messagebox.showinfo("MESSAGE", msg, parent=frameInsertIntoTable)

                                   
                           '''
                           def parentCBOSelectedEvent(event):
                           #substring the combobox name to exclude the leading '.' to get its corresponding text field name
                           txt = str(event.widget)[1:]
                           globals()[txt+'TXT'].delete('1.0', END)
                           globals()[txt+'TXT'].insert(INSERT, event.widget.get())

                           vals.append(globals()[df.loc[i,'mysqlcolumnname'].strip()+'TXT'].get('1.0','end-1c'))
                           
                           cc1 = childdropdown.split('.')

                           sql = "SELECT "+cc1[i+1].strip()+" as v FROM "+cc1[i].strip()
                           sql += " WHERE "+txt+"='"+globals()[cc[i+1].strip()+'TXT'].get('1.0','end-1c')+"'"
                        
                           globals()[colname+'TXT'].delete('1.0', END)
                           globals()[colname+'TXT'].insert(INSERT, newid)

                           if ctrl=='dropdown':
                           cursor.execute("SELECT DISTINCT "+lookupcol+" FROM "+lookuptbl)
                           lookupvals=[]
                           for val in cursor.fetchall():
                                   lookupvals.append(val[lookupcol])
                                   n = tk.StringVar()
                                   globals()[colname+'CBO'] = ttk.Combobox(frameInsertData, name=colname, width=30, textvariable = n)
                                   globals()[colname+'CBO']['values'] = lookupvals
                                   globals()[colname+'CBO'].grid(row=r, column = 4)
                                   globals()[colname+'CBO'].name=colname
                           def cboSelectedEvent(event):
                                   txt = str(event.widget)[1:]
                                   globals()[txt+'TXT'].delete('1.0', END)
                                   globals()[txt+'TXT'].insert(INSERT, event.widget.get())
                                   #child columns, if any
                                   d = df[df['mysqlcolumnname']==txt]
                                   d.index=np.arange(0,d.iloc[:,0].count())
                                   childcols = str(d.loc[0,'childcolumn']).strip()
                                   lookuptbl = str(d.loc[0,'lookupmysqltable']).strip()
                                   lookupcol = str(d.loc[0,'lookupmysqlcolumn']).strip()
                                   lookupcolcond = str(d.loc[0,'lookupmysqlcolumncondition']).strip()
                           globals()[colname+'CBO'].bind("<<ComboboxSelected>>", cboSelectedEvent)
                           '''
                           pass
                        
                   insertIntoTableSubmitButton = Button(frameInsertIntoTable, text="Insert into table", bg='yellow', command=insertIntoTableSubmitButtonClickEvent)
                   insertIntoTableSubmitButton.grid(row=r, column=3, padx=10, pady=10)
           except conn.Error as e:
                   msg = "ERROR: "+str(e.args[0])+e.args[1]
                   tk.messagebox.showinfo("MESSAGE", msg, parent=frameInsertIntoTable)
    insertIntoTableButton = Button(frame, text='Insert', width=20, command=insertIntoTableButtonClickEvent)
    insertIntoTableButton.grid(row=r, column=5, padx=20, pady=5, sticky=E)

    r += 2
    def searchTableButtonClickEventStart():
            table = tablesCBO.get()
            column = columnFindCBO.get()
            value = findWhatTXT.get()
            df = searchTableButtonClickEvent(root,table,column,value)
            createPandasTableFRM(root, df)    
    searchTableButton = Button(frame, text='Search Table', width=20, command=searchTableButtonClickEventStart)
    searchTableButton.grid(row=r, column=5, padx=20, pady=5, sticky=E)
   
    def deleteRowsButtonClickEventStart():
            table = tablesCBO.get()
            column = columnFindCBO.get()
            value = findWhatTXT.get()
            df = searchTableButtonClickEvent(root,table,column,value)
            createPandasTableFRM(root, df)
    deleteRowsButton = Button(frame, text='Delete Rows', width=20, command=deleteRowsButtonClickEventStart)
    deleteRowsButton.grid(row=r, column=6, padx=20, pady=5, sticky=E)

    r += 1
    def updateMultipleRowsButtonClickEventStart():
            table = tablesCBO.get()
            column = columnFindCBO.get()
            find = findWhatTXT.get()
            replace = replaceWithTXT.get()
            opfind = operatorFindCBO.get()
            #sql = "UPDATE "+table+" SET "+columnreplace+"='"+replace+"' WHERE "+columnfind+"='"+find+"'"
            #['=','<>','>','<','>=','<=','between','like','in']
            #if opfind in ['=','<>','>','<','>=','<=']:
            #        sql = "UPDATE "+table+" SET "+columnreplace+"='"+replace+"' WHERE "+columnfind+"='"+find+"'"
            sql = "UPDATE "+table+" SET "+columnreplace+"='"+replace+"' WHERE "+columnfind+" "+opfind+" "+find
            sqlQueryExecution(root, sql)
            
    updateMultipleRowsButton = Button(frame, text='Update Multiple Rows', width=20, command=updateMultipleRowsButtonClickEventStart)
    updateMultipleRowsButton.grid(row=r, column=5, padx=20, pady=5, sticky=E)


    '''
    sqlupdate += " UPDATE "+cc[i].strip()+" SET "+cc[i+1].strip()+"="
                        sqlupdate += globals()[expupdateothertblcol+'TXT'].get('1.0','end-1c')
                        sqlupdate += " WHERE "+keyupdateothertblcol+"="+globals()[keyupdateothertblcol+'TXT'].get('1.0','end-1c')

                        #print(sqlupdate)

                        #cursor.execute(sql)
    '''


    r += 1
    # General SQL Query Execution
    Label(frame, text='SQL Query:').grid(row=r, column=0, sticky=W)
    sqlQueryTXT = Entry(frame)
    sqlQueryTXT.grid(row=r, column=1, columnspan=8, sticky=EW)
    r += 1    
    def sqlQueryExecutionButtonClickEventStart():
            sql = sqlQueryTXT.get()
            sqlQueryExecution(root, sql)
            
    sqlQueryExecutionButton = Button(frame, text='SQL Query Execution', width=20, command=sqlQueryExecutionButtonClickEventStart)
    sqlQueryExecutionButton.grid(row=r, column=8, padx=20, pady=5, sticky=E)


#=============================================================================
# root frame
#=============================================================================
def createInsertRootFrame(rootframe, param):
        w, h = rootframe.winfo_screenwidth()-40, rootframe.winfo_screenheight()-150
        #insertrootframe = Frame(rootframe)
        #insertrootframe.grid(row=0, column=0, sticky='W', padx=15, pady=15)  #W-left, E-right, N-top, S-bottom
        insertrootframe = Toplevel(rootframe)
        insertrootframe.geometry("%dx%d+15+60" % (w, h))
        insertrootframe.title("INSERT NEW DATA")
        insertrootframe.configure(bg = 'aquamarine1')
        table = param['table'][0]
        df = table2df(insertrootframe,table)
        createInsertChildFrames(insertrootframe, param)
        '''
        img1 = Image.open("ppp.png")
        resize1 = img1.resize((75, 100))
        bgimg1 = ImageTk.PhotoImage(resize1)
        label = Label(insertrootframe, image = bgimg1)
        label.grid(row = 0, column = 0, sticky = 'SW')
        '''
        #createPandasTableFRM(insertrootframe, df)
        #createColumnCheckBoxesFRM(insertrootframe, table, df)
        #insertrootframe.mainloop()
        '''mywidth = insertrootframe.winfo_screenwidth()-20
        myheight = insertrootframe.winfo_screenheight()-100
        img = Image.open("ppp.png") #read the image
        resizeimg = img.resize((mywidth, myheight)) #resize the image
        bgimg = ImageTk.PhotoImage(resizeimg) #set resized images as bg
        #bgimglbl = Label(rootframe, image=bgimg) #place bg image in the label instead of text as in Label(frame, text="text")
        bgimglbl = Label(insertrootframe, compound=tk.BOTTOM, text="welcometext", font='Algerian 30 bold', fg='Black', image=bgimg)
        bgimglbl.grid(row=0, column=0, sticky='SW') #place the label in the first row, first column of the main root window; centered by default
'''
        
#=============================================================================
# standalone start
#=============================================================================
param = {'table':['item'],'pk':['itemcode'],'cbo':['itemcategory.itemcategory']}
if __name__ == "__main__":
    rootframe = Tk() 
    createInsertRootFrame(rootframe,param)
#=============================================================================

