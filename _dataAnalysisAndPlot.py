from _libraryAndDBConnection import * #includes database connection and cursor setting strings
#-----------------------------------------------------------------------------
# pandastable frame      r=1 c=0
# colcheckboxes frame    r=2 c=0
# insertDataInput frame  r=0 c=1
#-----------------------------------------------------------------------------
global tablesCBO
global pandasTableFRM
global colCheckboxesFRM
global plotFRM
global statisticalDetailsFRM
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
                print(msg)
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
                frameUpdateTable.configure(background='cyan')
                r = 0
                for colname in rowDataList.index:
                        #print(i,' -- ',rowDataList[colname])
                        Label(frameUpdateTable, text=colname, bg='cyan') \
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
def statisticalDetailsFRM(selectrootframe,table,df,r=1,c=1):
        global tablesCBO
        global plotFRM
        global statisticalDetailsFRM


        '''
        print(table, df)
        df = table2df(table)
        '''
        #sample data (head/tail)from dataframe
        w, h = selectrootframe.winfo_screenwidth(), selectrootframe.winfo_screenheight()
        h=h*20/100
        w=w*30/100
        #frame4 = Frame(selectrootframe, width=w*40/100, bg='black')   #!!!!!! selectrootframe and not any other frame
        frame4 = Frame(selectrootframe, width=w, height=h)#, bg='black')   #!!!!!! selectrootframe and not any other frame
        frame4.grid(row=1, column=1, sticky='NW')
        w, h = frame4.winfo_screenwidth(), frame4.winfo_screenheight()

        table = tablesCBO.get()
        #print(table)
        df = table2df(frame4,table)
        #print(df)

        #subframe41 = Frame(frame4, width=w*10/100, bg='red')   #!!!!!! selectrootframe and not any other frame
        subframe41 = Frame(frame4, width=w*2/100) #, bg='red')#!!!!!! selectrootframe and not any other frame
        subframe41.grid(row=0, column=0, sticky='NW')
        #subframe42 = Frame(frame4, width=w*40/100, bg='green')   #!!!!!! selectrootframe and not any other frame
        subframe42 = Frame(frame4, width=40)#, bg='green')   #!!!!!! selectrootframe and not any other frame
        subframe42.grid(row=0, column=1, sticky='NW')

        #Label(subframe42, text='TABLES:').grid(row=0, column=0, sticky='NW')
        d=df.describe().round(2)
        d.reset_index(level=0, inplace=True) #set index as a column in the dataframe for display in pt
        pt = Table(subframe42, dataframe=d, showstatusbar=False)  #width=w
        pt.show()
 

        #frameHeadingLBL = LabelFrame(frame4, text='frame4', font=('Times', 12), bd=5, relief=RIDGE, bg='red')
        #r4=0
        #Label(subframe41, text="SAMPLE DATAFRAME DATA").grid(row=r4, column=0, columnspan=2, sticky='NW')
        r4 = 0
        def sampleDataBTNClickEvent():
                
                if df.empty==False:
                        numofrows = numofrowstxt.get('1.0','end-1c')
                        if varHeadTail.get()=='head':
                                if len(numofrows)>0:
                                    d=df.head(int(numofrows))
                                else:
                                    d=df.head()
                        else:
                                if len(numofrows)>0:
                                    d=df.tail(int(numofrows))
                                else:
                                    d=df.tail()
                        #displayPandasTable(subframe42, d)
                        #pt = Table(subframe42, dataframe=d, width=50, showstatusbar=False)
                        pt = Table(subframe42, dataframe=d, showstatusbar=False)
                        pt.show()
                else:
                    tkmsgbox.showinfo("ATTENTION PLEASE!","The '"+cboTables.get().upper()+"' table is empty.",parent=frame4)
        varHeadTail = StringVar()
        values = {"Top Samples":"head","Bottom Samples":"tail"}
        #loop to create multiple Radiobuttons - don't create each button separately
        c=0
        for (text, value) in values.items():
                #rbt = Radiobutton(frame3, text=text, variable=var, value=value, command=sampleDataBtnClickEvent)
                rbt = Radiobutton(subframe41, text=text, variable=varHeadTail, value=value, tristatevalue=0)
                rbt.grid(row=r4, column=c, sticky='NW')
                #c+=1
                r4 += 1
        Label(subframe41, text="No. of rows").grid(row=r4, column=0, sticky=W)
        numofrowstxt = Text(subframe41, height=1, width=10)
        numofrowstxt.grid(row=r4, column=1, sticky='NW')
        r4 += 1
        sampleDataBTN = Button(subframe41, text='SAMPLE DATAFRAME DATA', command=sampleDataBTNClickEvent)
        sampleDataBTN.grid(row=r4, column=0, columnspan=2, sticky='NW')
        r4 += 1
        '''
        def displayPandasTable(df):
                #width=rootDA.winfo_screenwidth()-50
                global globalDF
                globalDF = df
                pt = Table(framePandasTable, dataframe=globalDF)    
                pt.show()
        '''

        def statDetailBTNClickEvent():
                table = tablesCBO.get()
                df = table2df(subframe41, table)
                #df=df.describe()
                d=df.describe().round(2)
                #df['index']=df.index
                d.reset_index(level=0, inplace=True) #set index as a column in the dataframe for display in pt
                #displayPandasTable(d)
                #w, h = subframe42.winfo_screenwidth()-120, subframe42.winfo_screenheight()-160
                #w = w*70/100
                #pt = Table(subframe42, dataframe=d, width=w, showstatusbar=False)
                pt = Table(subframe42, dataframe=d, showstatusbar=False)
                pt.show()
        statDetailBTN = Button(subframe41, text='STATISTICAL DETAILS OF DF DATA', command=statDetailBTNClickEvent)
        statDetailBTN.grid(row=r4, column=0, columnspan=2, sticky='NW')

        for widget in subframe41.winfo_children():
                widget.grid(padx=2, pady=2)
        for widget in subframe42.winfo_children():
                widget.grid(padx=2, pady=2)


          
        '''
        #fire tablescbo combobox click-event programmatically
        idx = lookupvals.index(table)
        tablesCBO.current(idx)
        #print(idx, tablesCBO.current(idx), lookupvals[idx])
        tablesCBO.event_generate('<<ComboboxSelected>>')
        '''
        #sampleDataBTN.event_generate('<<ComboboxSelected>>')
        #statDetailBTN.event_generate('<<ComboboxSelected>>')

#-----------------------------------------------------------------------------
def MatplotlibGUI(chartFRM, df, xcol, ycol, charttype):
        #for widget in chartFRM.winfo_children():
        #    widget.destroy()
        import matplotlib


        matplotlib.use('TkAgg')
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        plt.clf()
        fig = plt.figure(1)
        x = df[xcol].tolist()
        y = df[ycol].tolist()
        if charttype=='plot':
                plt.plot(x,y)
        elif charttype=='bar':
                plt.bar(x,y)
        #elif charttype=='plot':
        #        plt.hist(x,y)
        canvas = FigureCanvasTkAgg(fig, master=chartFRM)
        plot_widget = canvas.get_tk_widget()
        plot_widget.grid(row=0, column=0)

#-----------------------------------------------------------------------------


#---------------------------------------
def createChartFRM(root, df, xcol, ycol, charttype):
        global chartFRM
        w, h = root.winfo_screenwidth()-120, root.winfo_screenheight()-160
        w = w*70/100
        #h = h*5/100
        r = 0
        chartFRM = Frame(root, width=w, bg='red')#, height=h)
        chartFRM.grid(row=0, column=1, rowspan=2, sticky='NW')
        chartLBL = Table(chartFRM, text="xxxx")
        chartLBL.grid(row=r, column=0, sticky=W)
        MatplotlibGUI(chartFRM, df, xcol, ycol, charttype)

#=============================================================================
def plottry():
        x = [2012,2013,2014,2015,2016]
        y = [45,56,23,78,42]
        plt.bar(x,y)
        plt.xlabel('X-Axis')
        plt.ylabel('Y-Axis')
        plt.xticks(x)
        plt.yticks(np.arange(0,101,10))
        plt.show()

#--------------------------------------------------------------------------
def plottry1(plotparams):
        import matplotlib
        matplotlib.use('TkAgg')
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

        plotFRM = Toplevel()
        
        table = plotparams['table']
        df = table2df(plotFRM,table)
        x = df[plotparams['x']].tolist()
        y = df[plotparams['y']].tolist()
        title = plotparams['title']
        #xticks = plotdata['xticks']
        #yticks = plotdata['yticks']
        xlabel = plotparams['xlabel']
        ylabel = plotparams['ylabel']
        legend = plotparams['legend']
        grid = plotparams['grid']
        charttype = plotparams['charttype']

        figure = Figure(figsize=(6, 4), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, plotFRM)
        NavigationToolbar2Tk(figure_canvas, plotFRM)
        axes = figure.add_subplot()

        
        if charttype=='plot':
                axes.plot(x,y)
        elif charttype=='bar':
                axes.bar(x,y)
        elif charttype=='hist':
                mybin = plotparams['mybin']
                myrange =plotparams['myrange']
                axes.hist(data=x, bin=mybin, range=myrange) 

        axes.set_title(title)
        axes.set_xlabel(xlabel)
        axes.set_ylabel(ylabel)
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        '''
        plt.title = plotparams['title']
        #plt.xticks = plotdata['xticks']
        #plt.yticks = plotdata['yticks']
        plt.xlabel = plotparams['xlabel']
        plt.ylabel = plotparams['ylabel']
        plt.legend = plotparams['legend']
        plt.grid = plotparams['grid']
        plt.show()
        '''
        
#=============================================================================
def createPlotFRM(frame, plotparams):

        global plotFRM
                
        #import ctypes
        #ctypes.windll.shcore.SetProcessDpiAwareness(1)
        '''
        import win32con, win32gui, win32print
        def get_dpi():
                hDC = win32gui.GetDC(0)
                HORZRES = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
                VERTRES = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
                return HORZRES,VERTRES
        wp,hp = get_dpi()
        '''
        #global plotFRM
        plotFRM = Toplevel()
        plotFRM.title('My Plot')
        wp, hp = frame.winfo_screenwidth()-20, frame.winfo_screenheight()-100



        '''
        import win32con, win32gui, win32print
        def get_dpi():
                hDC = win32gui.GetDC(0)
                HORZRES = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
                VERTRES = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
                return HORZRES,VERTRES
        wp,hp = get_dpi()
        wp = wp*40/100
        hp = hp*40/100
        '''
                
        
        plotFRM.geometry("%dx%d+0+0" % (wp, hp))
        plotFRM.configure(background="#88cffa") #"light grey"
        #print(plotFRM.winfo_width(), plotFRM.winfo_height())
        #frame.tk.call('tk', 'scaling', 1.25)  #Zoom out 2 times

        
        
        ######## --------- PLOTTING ON DEFAULT MATPLOTLIB POPUP WINDOW
        table = plotparams['table']
        df = table2df(frame,table)
        x = df[plotparams['x']].tolist()
        y = df[plotparams['y']].tolist()
        title = plotparams['title']
        #xticks = plotdata['xticks']
        #yticks = plotdata['yticks']
        xlabel = plotparams['xlabel']
        ylabel = plotparams['ylabel']
        legend = plotparams['legend']
        grid = plotparams['grid']
        charttype = plotparams['charttype']
        
        if charttype=='plot':
                plt.plot(x,y)
        elif charttype=='bar':
                plt.bar(x,y)
        elif charttype=='hist':
                mybin = plotparams['mybin']
                myrange =plotparams['myrange']
                plt.hist(data=x, bin=mybin, range=myrange) 

        plt.title = plotparams['title']
        #plt.xticks = plotdata['xticks']
        #plt.yticks = plotdata['yticks']
        plt.xlabel = plotparams['xlabel']
        plt.ylabel = plotparams['ylabel']
        plt.legend = plotparams['legend']
        plt.grid = plotparams['grid']
        plt.show()
        

        '''
        ######## --------- PLOTTING ON A FRAME

        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import matplotlib
        from matplotlib.figure import Figure
        matplotlib.use("TkAgg")
        
        table = plotparams['table']
        df = table2df(frame,table)
        x = df[plotparams['x']].tolist()
        y = df[plotparams['y']].tolist()
        charttype = plotparams['charttype']
        plt.clf()
        fig = plt.figure(1)
        if charttype=='plot':
                plt.plot(x,y)
        elif charttype=='bar':
                plt.bar(x,y)
        #elif charttype=='hist':
        #        plt.hist(x,y)
        canvas = FigureCanvasTkAgg(fig, master=plotFRM)
        plot_widget = canvas.get_tk_widget()
        plot_widget.grid(row=0, column=0)      
        def onsize(event):
                print(plotFRM.winfo_width(), plotFRM.winfo_height())
        plotFRM.bind("<Configure>", onsize)

        '''
        
#=============================================================================
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
        #col+=1
        r+=1
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
        w = w*50/100
        h = h*40/100
        pandasTableFRM = Frame(frame, height=h, width=w)
        pandasTableFRM.grid(row=r, column=c, sticky='NW')
        #pt = Table(pandasTableFRM, dataframe=df, showtoolbar=True, width=w, showstatusbar=True)
        pt = Table(pandasTableFRM, dataframe=df, width=w, height=h, showstatusbar=True)  
        pt.cellbackgr = 'chartreuse1'
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
        #frame.tk.call('tk', 'scaling', 1.25)  #Zoom out 1.25 times which is equivalent of 125% default display on Windows10


        df = table2df(frame,table)
        dfColumns = descTable(frame,table)

        r=0
        Label(frame, text='TABLES:').grid(row=r, column=0, sticky='NW')
        tables = StringVar()
        tablesCBO = Combobox(frame, name='tablecbo', width=30)#, textvariable=tablesCBOvar) #,width=30)
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
            columnFindCBO['values'] = df.columns.tolist()

            xcolCBO['values'] = df.columns.tolist()
            ycolCBO['values'] = df.columns.tolist()
            
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
            createColumnCheckBoxesFRM(selectrootframe, table, df, 0, 2)
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
        frame1 = Frame(frame, bg="cadetblue1")
        frame1.grid(row=r, column=0, columnspan=2, sticky='NW')  #W-left, E-right, N-top, S-bottom
        # search / Find What
        r1=0
        Label(frame1, text='Find what:').grid(row=r1, column=0, sticky='NW')
        findWhatTXT = Entry(frame1, width=30)
        findWhatTXT.grid(row=r1, column=1, sticky='NW')
        r1 += 1
        Label(frame1, text='compare').grid(row=r1, column=0, sticky='NW')
        operatorfind = StringVar()
        operatorFindCBO = Combobox(frame1, name='operatorFindCBO', width=10, textvariable=operatorfind)
        operatorFindCBO['values'] = ['=','<>','>','<','>=','<=','between','like','in']
        operatorFindCBO.grid(row=r1, column=1, sticky='NW')
        operatorFindCBO.current(0)
        r1 += 1
        Label(frame1, text='in column').grid(row=r1, column=0, sticky='NW')
        columnfind = StringVar()
        columnFindCBO = Combobox(frame1, name='columnFindCBO', width=30, textvariable=columnfind)
        #columnFindCBO['values'] = lookupvals
        columnFindCBO.grid(row=r1, column=1, sticky='NW')
        r1 += 1
        def searchTableButtonClickEventStart():
            table = tablesCBO.get()
            column = columnFindCBO.get()
            value = findWhatTXT.get()
            df = searchTableButtonClickEvent(frame1,table,column,value)
            createPandasTableFRM(selectrootframe, df)

            '''    
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
           
        searchTableButton = Button(frame1, text='Search Table', width=20, command=searchTableButtonClickEventStart)
        searchTableButton.grid(row=r1, column=1, sticky='EW')



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
                createColumnCheckBoxesFRM(selectrootframe, table, df, 0, 2)
                '''
                #for queries other than SELECT
                sql = sqlQueryTXT.get("1.0",'end-1c') #for TEXT use -  textbox1.get("1.0",'end-1c') #For entry txt.get()
                sqlQueryExecution(frame, sql)
                '''
        sqlQueryExecutionButton = Button(frame2, text='SQL Query Execution', width=20, command=sqlQueryExecutionButtonClickEventStart)
        sqlQueryExecutionButton.grid(row=r, column=1, sticky='EW')

        r += 1
        #sub frame #3
        # Plot Settings
        frame3 = Frame(frame)
        frame3.grid(row=r, column=0, columnspan=2, sticky='NW')  #W-left, E-right, N-top, S-bottom
        r2 = 0
        Label(frame3, text='Plot Settings:').grid(row=r2, column=0, columnspan=2, sticky='NW')
        '''
        r2 += 1
        Label(frame3, text='Plot Settings:').grid(row=r2, column=0, columnspan=2, sticky='NW')
        sqlQueryTXT = Text(frame3, width=35, height=6)
        sqlQueryTXT.grid(row=r2, column=0, columnspan=2, sticky='NW')
        '''
        r2 += 1
        Label(frame3, text='X-Column').grid(row=r2, column=0, sticky='NW')
        xcol = StringVar()
        xcolCBO = Combobox(frame3, name='xcolcbo', width=30, textvariable=xcol)
        xcolCBO.grid(row=r2, column=1, sticky='NW')
        #xcolCBO.current(0)
        r2 += 1
        Label(frame3, text='Y-Column').grid(row=r2, column=0, sticky='NW')
        ycol = StringVar()
        ycolCBO = Combobox(frame3, name='ycolcbo', width=30, textvariable=ycol)
        ycolCBO.grid(row=r2, column=1, sticky='NW')
        #ycolCBO.current(0)
        r2 += 1
        Label(frame3, text='Title:').grid(row=r2, column=0, sticky='NW')
        titleTXT = Entry(frame3, width=30)
        titleTXT.grid(row=r2, column=1, sticky='NW')
        r2 += 1
        Label(frame3, text='X-Label:').grid(row=r2, column=0, sticky='NW')
        xlabelTXT = Entry(frame3, width=30)
        xlabelTXT.grid(row=r2, column=1, sticky='NW')
        r2 += 1
        Label(frame3, text='Y-Label:').grid(row=r2, column=0, sticky='NW')
        ylabelTXT = Entry(frame3, width=30)
        ylabelTXT.grid(row=r2, column=1, sticky='NW')
        r2 += 1
        Label(frame3, text='Legend:').grid(row=r2, column=0, sticky='NW')
        legendTXT = Entry(frame3, width=30)
        legendTXT.grid(row=r2, column=1, sticky='NW')
        r2 += 1
        Label(frame3, text='Chart Type:').grid(row=r2, column=0, sticky='NW')
        chartTypeVar = StringVar()
        chartTypeCBO = Combobox(frame3, name='charttype', width=30, textvariable=chartTypeVar)
        chartTypeCBO.grid(row=r2, column=1, sticky='NW')
        chartTypeCBO['values'] = ['plot','bar','hist']
        r2 += 1
        Label(frame3, text='Bin (for HIST):').grid(row=r2, column=0, sticky='NW')
        binTXT = Entry(frame3, width=30)
        binTXT.grid(row=r2, column=1, sticky='NW')
        r2 += 1
        Label(frame3, text='Range (for HIST):').grid(row=r2, column=0, sticky='NW')
        rangeTXT = Entry(frame3, width=30)
        rangeTXT.grid(row=r2, column=1, sticky='NW')
        r2 += 1
        Label(frame3, text='Grid').grid(row=r2, column=0, sticky='NW')
        gridvar = StringVar()
        gridCBO = Combobox(frame3, name='grid', width=30, textvariable=gridvar)
        gridCBO.grid(row=r2, column=1, sticky='NW')
        gridCBO['values'] = ['True','False']
        #gridCBO.current(0)
        r2 += 1
        def drawPlotEvent():
            #global tablesCBO
            table = tablesCBO.get()
            x = xcolCBO.get()
            y = ycolCBO.get()
            title = titleTXT.get()
            #xticks = plotdata['xticks']
            #yticks = plotdata['yticks']
            xlabel = xlabelTXT.get()
            ylabel = ylabelTXT.get()
            legend = legendTXT.get()
            grid = gridCBO.get()
            charttype = chartTypeCBO.get()
            mybin = legendTXT.get()
            myrange = legendTXT.get()

            #print(table)
            
            plotparams = {'table':table,'x':x,'y':y,'title':title,'xlabel':xlabel,'ylabel':ylabel,'legend':legend, 
                     'grid':grid,'charttype':charttype,'mybin':mybin,'myrange':myrange}
            #createPlotFRM(selectrootframe, plotparams)  #!!!!!!selectrootframe and frame
            #createPlotFRM(frame, plotparams)  #!!!!!!selectrootframe and frame
            plottry1(plotparams)
                    
        drawPlotBTN = Button(frame3, text='Draw Plot', width=20, command=drawPlotEvent)
        #drawPlotBTN = Button(frame3, text='Draw Plot', width=20, command=plottry1)            
        drawPlotBTN.grid(row=r2, column=1, sticky='EW')







        #----------------------------------------
        r += 1
        #sub frame #5
        frame5 = Frame(frame)
        frame5.grid(row=r, column=0, columnspan=2, sticky='NW')  #W-left, E-right, N-top, S-bottom
        r4 = 0
        def savecsvfile():
                #df=createDataFrame(cboTables.get())
                filetypes = [('CSV Files','*.csv')]
                saveatfilepath = asksaveasfile(mode='w', filetypes = filetypes, defaultextension=filetypes)
                df.to_csv(saveatfilepath)
        Button(frame5, text='Save DF as CSV file', command=lambda:savecsvfile()).grid(row=r, column=1, sticky='W')
        #----------------------------------------
        for widget in frame.winfo_children():
                widget.grid(padx=10, pady=2)        

        for widget in frame1.winfo_children():
                widget.grid(padx=10, pady=2)        

        for widget in frame2.winfo_children():
                widget.grid(padx=10, pady=2)        
        
        for widget in frame3.winfo_children():
                widget.grid(padx=10, pady=2)
        #----------------------------------------        
        #fire tablescbo combobox click-event programmatically
        idx = lookupvals.index(table)
        tablesCBO.current(idx)
        #print(idx, tablesCBO.current(idx), lookupvals[idx])
        tablesCBO.event_generate('<<ComboboxSelected>>')
        

#=============================================================================
# root frame
#=============================================================================
def createDataAnalysisRootFrame(rootframe, param):

        #decalre here before creating root frame as their existance is to be verified during startup
        global pandasTableFRM
        global colCheckboxesFRM
        global statisticalDetailsFRM
        global plotFRM

        pandasTableFRM = Frame()
        colCheckboxesFRM = Frame()

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
        r=0;c=2      
        createColumnCheckBoxesFRM(selectrootframe,table,df,r,c)
        r=1;c=1      
        statisticalDetailsFRM(selectrootframe,table,df,r,c)        

        '''
        r=1;c=1
        plotdata={}
        createPlotFRM(selectrootframe,plotdata)
        '''

#=============================================================================
# standalone start
#=============================================================================
param = {'table':['item'],'pk':['itemcode'],'cbo':['itemcategory.itemcategory']}
if __name__ == "__main__":
        rootframe = Tk()

        
        '''
        w,h = rootframe.winfo_screenwidth()-120, rootframe.winfo_screenheight()-160
        rootframe.geometry("%dx%d+0+0" % (w, h)) #root window size 'wxh' at left top coordinates 0,0
        rootframe.maxsize(w,h)
        rootframe.minsize(w,h)
        '''

        '''
        import win32con, win32gui, win32print
        def get_dpi():
                hDC = win32gui.GetDC(0)
                HORZRES = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
                VERTRES = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
                return HORZRES,VERTRES
        w,h = get_dpi()
        rootframe.geometry("%dx%d+0+0" % (w, h))
        '''
        
        createDataAnalysisRootFrame(rootframe, param)
#=============================================================================

