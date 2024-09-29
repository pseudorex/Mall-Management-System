from _libraryAndDBConnection import * #includes database connection and cursor setting strings
#-----------------------------------------------------------------------------
def table2df(frame, table, columns='*', condition='1=1'):
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
#=============================================================================
# child frame
#=============================================================================
def createTransChildFrames(root, param):
        
        
    frame = Frame(root)
    frame.grid(row=0, column=0, sticky='W', padx=10, pady=10)
    frame.configure(background='mistyrose1')
    
    r = 0
    Label(frame, text="Transaction Record Entry", bg = 'mistyrose1', font=('Algerian', 15)).grid(sticky=NW)
    # SET TRANSACTION TABLE
    table = param['table']    
    r += 1
    # SET DATE USING CALENDAR
    Label(frame, text='Date', bg = 'mistyrose1').grid(row=r, column=0, sticky=W)
    def getDate():
        dt = cal.get_date()
        sqlDate = dt.strftime("%Y%m%d") #20210418(For Database query) #displayDate = dt.strftime("%d-%B-%Y") # date string 18-April-2021
        globals()[param['dateColumn']].delete(0,END)
        globals()[param['dateColumn']].insert(INSERT,sqlDate)
    cal = DateEntry(frame, selectmode='day', width=25)
    cal.grid(row=r,column=1,sticky=W) #,padx=15)
    cal.set_date(date.today())
    setDateBTN = tk.Button(frame,text='Set Date',command=getDate)
    setDateBTN.grid(row=r,column=2,sticky=W,padx=10)
    globals()[param['dateColumn']] = Entry(frame)
    globals()[param['dateColumn']].grid(row=r,column=3,sticky=W)
    r += 1
    # SET PRIMARY KEY OF TRANSACTION TABLE e.g. invoice for sale or purchase
    for i in param['pk']:
            globals()[i+'LBL'] = Label(frame, text=i[i.find('.')+1:], bg = 'mistyrose1')
            globals()[i+'LBL'].grid(row=r, column=0, sticky=W)
            globals()[i] = Entry(frame, width=30)
            globals()[i].grid(row=r, column=1, sticky=W)
            r += 1
    # SET MASTER PICKUP DROP-DOWNS
    #'masterCBO' : ['item.itemcategory>item.itemname']  # masterCBO > childCBO ... select event of masterCBO changes lookup values in childCBO
    for mcbo in param['masterCBO']:
            #set masterCBO
            if len(param['masterCBO'])>0:
                    masterCBO = mcbo[:mcbo.find('#')]
                    childCBO = mcbo[mcbo.find('#')+1:]
                    masterCBOtbl = masterCBO[:masterCBO.find('.')]
                    masterCBOcol = masterCBO[masterCBO.find('.')+1:]
                    Label(frame, text=masterCBOcol, bg = 'mistyrose1').grid(row=r, column=0, sticky=W)
                    globals()[masterCBOtbl+'_'+masterCBOcol] = StringVar()
                    globals()[masterCBOcol] = Combobox(frame, name=masterCBOtbl+'_'+masterCBOcol) #use combobox name to get the table name 
                    globals()[masterCBOcol].grid(row=r, column=1, sticky=W)
                    cols = '*'
                    condition = '1=1'
                    #globals()[masterCBOtbl+'DF'] = table2df(root, masterCBOtbl, cols, cond)
                    sql = "select distinct "+masterCBOcol+" from "+masterCBOtbl+" where "+condition
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    globals()[masterCBOtbl+'DF'] = pd.DataFrame(data)
                    print(globals()[masterCBOtbl+'DF'])
                    lookupvals = globals()[masterCBOtbl+'DF'][masterCBOcol].tolist()
                    globals()[masterCBOcol]['values'] = lookupvals
                    # masterCBO event handling        
                    def funcMasterCBOSelectedEvent(event):
                            mpk = event.widget._name
                            mCBOtbl = mpk[:mpk.find('_')]
                            mCBOcol = mpk[mpk.find('_')+1:]
                            mCBOval = globals()[mCBOcol].get()
                            childCBOcol = childCBO[childCBO.find('.')+1:]
                            for conds in param['condition']:
                                    if mCBOtbl in conds:
                                            cond = conds[conds.find('.')+1:]
                            #globals()[mCBOtbl+'DF'] = table2df(root, mCBOtbl, cols, cond)
                            sql = "select * from "+mCBOtbl+" where "+mCBOcol+"='"+mCBOval+"'"
                            #print(sql)
                            cursor.execute(sql)
                            data = cursor.fetchall()
                            globals()[mCBOtbl+'DF'] = pd.DataFrame(data)                            
                            lookupvals = globals()[mCBOtbl+'DF'][childCBOcol].tolist()
                            print(lookupvals)
                            print(globals()[mCBOtbl+'DF'])
                            #childCBO = mcbo[mcbo.find('>')+1:]
                            #childCBOtbl = childCBO[:childCBO.find('.')]                            
                            globals()[childCBOcol]['values'] = lookupvals

                            
                    globals()[masterCBOcol].bind("<<ComboboxSelected>>", funcMasterCBOSelectedEvent)    
                    

    r += 1        
    for i in param['masterLookupItems']:  #DICT ITEM: 'masterLookupItems':['table1.pk1','table2.pk2',...]
            # Pick one master table along with its primary key, lookup and autofills at a time
            masterlookuptbl = i[:i.find('.')]
            masterlookupcol = i[i.find('.')+1:]
            #'condition' : ['item.itemstock > 0']
            #default condition='1=1'
            cols = '*'
            cond = '1=1'
            for conds in param['condition']:
                    if masterlookuptbl in conds:
                            cond = conds[conds.find('.')+1:]

            #print(masterlookuptbl, "  ", masterlookupcol, "  ",cond)                
            globals()[masterlookuptbl+'DF'] = table2df(root, masterlookuptbl, cols, cond)
            #print(globals()[masterlookuptbl+'DF'])

            lookupvals = globals()[masterlookuptbl+'DF'][masterlookupcol].tolist()
            #print(lookupvals)

            # set combobox or drop-down with master table lookup values    
            Label(frame, text=masterlookupcol, bg = 'mistyrose1').grid(row=r, column=0, sticky=W)
            globals()[masterlookuptbl+'_'+masterlookupcol] = StringVar()
            globals()[masterlookupcol] = Combobox(frame, name=masterlookuptbl+'_'+masterlookupcol) #use combobox name to get the table name 
            globals()[masterlookupcol].grid(row=r, column=1, sticky=W)
            globals()[masterlookupcol]['values'] = lookupvals
            # master lookup table PKs
            for mpk in param['masterPrimaryKeys']:
                    if masterlookuptbl in mpk:
                            masterlookuppkcol = mpk[mpk.find('.')+1:]
            Label(frame, text=masterlookuppkcol, bg = 'mistyrose1').grid(row=r, column=2, sticky=W)
            globals()[masterlookuppkcol] = Entry(frame, width=30)                
            globals()[masterlookuppkcol].grid(row=r, column=3, sticky=W)
            r += 1
            # master lookup table autofills
            for afv in param['masterAutofillValues']:
                    if masterlookuptbl in afv:
                            masterautofillcol = afv[afv.find('.')+1:]
                            Label(frame, text=masterautofillcol, bg = 'mistyrose1').grid(row=r, column=0, sticky=W)
                            globals()[masterautofillcol] = Entry(frame, width=30)
                            globals()[masterautofillcol].grid(row=r, column=1, sticky=W)
                            r += 1

                            #print(masterautofillcol)    
                            
            # master lookup event handling        
            def funcSelectedEvent(event):
                    #combobox name => mastertable+'_'+masterlookupcol
                    #Get label text
                    #print("label text:", event.widget.cget("text"))
                    mpk = event.widget._name
                    masterlookuptbl = mpk[:mpk.find('_')]
                    masterlookupcol = mpk[mpk.find('_')+1:]
                    masterlookupval = globals()[masterlookupcol].get()
                    mastertbleDF = globals()[masterlookuptbl+'DF']
                    #fill PK and autofill values from master pickup table
                    for c in mastertbleDF.columns:
                            if masterlookuptbl+'.'+c in param['masterPrimaryKeys']:
                                    #masterlookuppkval = mastertbleDF[mastertbleDF[masterlookupcol]==masterlookupval][c].tolist()[0]
                                    masterlookuppkval = mastertbleDF[mastertbleDF[masterlookupcol]==masterlookupval][c].tolist()[0]
                                    globals()[c].delete(0,END)    
                                    globals()[c].insert(INSERT,masterlookuppkval)
                            if masterlookuptbl+'.'+c in param['masterAutofillValues']:  
                                    autofillVal = mastertbleDF[mastertbleDF[masterlookupcol]==masterlookupval][c].tolist()[0]
                                    globals()[c].delete(0,END)
                                    globals()[c].insert(INSERT,round(autofillVal,2))

                                    #print(masterlookuptbl+'.'+c, '     ' ,autofillVal )
                                    
            globals()[masterlookupcol].bind("<<ComboboxSelected>>", funcSelectedEvent)
            r += 1

    for i in param['transItems']:
            globals()[i+'LBL'] = Label(frame, text=i[i.find('.')+1:], bg = 'mistyrose1')
            globals()[i+'LBL'].grid(row=r, column=0, sticky=W)
            globals()[i] = Entry(frame, width=30)
            globals()[i].grid(row=r, column=1, sticky=W)
            r += 1
    def expressionBTNClickEvent():
            for exp in param['expressions']:
                    expLeft = exp[:exp.find('=')].strip()
                    expRight = exp[exp.find('=')+1:]
                    globals()[expLeft].insert(INSERT, round(eval(expRight),2))
    expressionBTN = Button(frame, text="Calculate", command=expressionBTNClickEvent)
    expressionBTN.grid(row=r, column=1)

    r += 1
    for i in param['expressions']:
            i = i[:i.find('=')].strip()
            globals()[i+'LBL'] = Label(frame, text=i, bg = 'mistyrose1')
            globals()[i+'LBL'].grid(row=r, column=0, sticky=W)
            globals()[i] = Entry(frame, width=30)
            globals()[i].grid(row=r, column=1, sticky=W)
            r += 1


    #for inv in param['invisible']:
    #        globals()[inv].grid_remove()


    def submitButtonClickEvent():


            
            # columns to be sent to trans 'table' - dateColumn, pk, transItems, expressions
            # master values not to be sent to trans table unless assigned to the columnnames in expression
            # masterUpdates to be set in master tables only


            #!IMPORTANT: date column should be named something as 'transdate' not as 'date'
            #Do not change 'keys' of the following dictionaries
            ##use column names only on right hand side of an expression

            #'invisible' - is the simple assignment which is to be saved in trans table BUT NOT to be displayed on screen
            
            cols = []
            vals = []

            table = param['table']

            cols.append(param['dateColumn'])

            for p in param['pk']:
                    cols.append(p[p.find('.')+1:])

            '''
            for mcb in param['masterCBO']:
                    cols.append(mcb[mcb.find('.')+1:mcb.find('#')])    
            for mpi in param['masterLookupItems']:
                    cols.append(mpi[mpi.find('.')+1:])
            for mpk in param['masterPrimaryKeys']:
                    #cols.append(mpk[mpk.find('.')+1:])
                    #cols.append(globals()[mpk[:mpk.find('.')]+'PK'])        #equivalent of globals()[table+'PK']
                    #t = globals()[mpk[mpk.find('.')+1:]].get()
                    cols.append(mpk[mpk.find('.')+1:])
            '''
            
            for ti in param['transItems']:
                    cols.append(ti[ti.find('.')+1:])
                    
            for ex in param['expressions']:
                    #cols.append(ex[ex.find('.')+1:])
                    cols.append(ex[:ex.find('=')].strip())


            #print(cols)

            for c in cols:
                    #print(cols,"   ",c)
                    vals.append(globals()[c].get())

            #print(vals)


            for inv in param['invisible']:  #simple assignments, same as expressions
                    cols.append(inv[:inv.find('=')].strip())
                    vals.append(eval(inv[inv.find('=')+1:].strip()))

            print(cols)
            print(vals)

            sql = "INSERT INTO "+ table[0] +"("
            for c in cols:
                    sql += c+","
            sql = sql[:-1]
            sql += ") VALUES("
            for v in vals:
                    sql += "'"+v+"',"
            sql = sql[:-1]
            sql += ")" 
            print(sql)

            #'masterUpdates' : ['item.stock=float(item.stock)+float(quantity)']
            for t in param['masterUpdates']:

                    left = t[:t.find('=')]
                    table = left[:left.find('.')]
                    col = left[left.find('.')+1:]
                    exp = t[t.find('=')+1:] #right
                    pk=''
                    for pkc in param['masterPrimaryKeys']:
                            tbl = pkc[:pkc.find('.')]
                            if tbl==table:
                                    pkCol = pkc[pkc.find('.')+1:]
                    exp = str(round(eval(exp),2))
                    sql1 = "UPDATE "+ table +" SET "+ col +"="+ exp + \
                           " WHERE "+ pkCol +"="+ globals()[pkCol].get()
                    print(sql1)
                    
                    try:
                            #####cursor.execute(sql)
                            cursor.execute(sql1)
                            ####conn.commit()
                            ####msg = "SUCCESS: SQL query executed successfully."
                            ####tk.messagebox.showinfo("MESSAGE", msg, parent=frame)
                    except conn.Error as e:
                            msg = "ERROR: "+str(e.args[0])+e.args[1]
                            tk.messagebox.showinfo("MESSAGE", msg, parent=frame)        

            try:
                    cursor.execute(sql)
                    ###cursor.execute(sql1)
                    conn.commit()
                    msg = "SUCCESS: SQL query executed successfully."
                    tk.messagebox.showinfo("MESSAGE", msg, parent=frame)
            except conn.Error as e:
                    msg = "ERROR: "+str(e.args[0])+e.args[1]
                    tk.messagebox.showinfo("MESSAGE", msg, parent=frame)

        
    submitButton = Button(frame, text="Submit", command=submitButtonClickEvent)
    submitButton.grid(row=r, column=1)
    r += 1
    #-----------------------------------------
    for widget in frame.winfo_children():
        widget.grid(padx=0, pady=5)
#=============================================================================
# root frame
#=============================================================================
def createTransRootFrame(rootframe, p):
        print(p)
        
        w, h = rootframe.winfo_screenwidth()-50, rootframe.winfo_screenheight()-150
        transrootframe = Toplevel(rootframe)
        transrootframe.geometry("%dx%d+15+60" % (w, h)) 
        transrootframe.title("TRANSACTION ENTRY")
        transrootframe.configure(background = 'mistyrose1')
        table = p['table'][0]
        df = table2df(transrootframe,table)
        createTransChildFrames(transrootframe, p)
#=============================================================================
# standalone start
#=============================================================================
myparam = {
        'table'                 : ['transexpense'],
        'pk'                    : ['invoice'],
        'dateColumn'            : "pdate",
        'masterCBO'             : ['expense.expensecategory#expense.expensename'],
        'masterLookupItems'     : ['expense.expensename'],
        'masterPrimaryKeys'     : ['expense.expensecode'],
        'masterAutofillValues'  : ['expense.expensegstrate'],
        'condition'             : [],
        'expressions'           : ['gst=float(expensegstrate.get())*float(cost.get())/100', \
                                   'netamount=float(cost.get())+float(gst.get())'],
        'transItems'            : ['cost'],
        'masterUpdates'         : [] #use column names only on right hand side 
        }
myparam1 = {
        'table'                : ['income'],
        'pk'                    : ['incomecd'],
        'dateColumn'            : 'sdate',
        'masterCBO'             : ['showroom.showroomcategory#showroom.showroomname'],
        'masterLookupItems'     : ['showroom.showroomname'],
        'masterPrimaryKeys'     : ['showroom.showroomcode'],
        'masterAutofillValues'  : ['showroom.rentgstrate','showroom.rentpermnth'],
        'condition'             : ['showroom.rentpermnth > 0'],
        'transItems'            : ['month'],
        'expressions'           : ['amount=float(rent.get())*float(month.get())', \
                                           'gst=float(rentpermnth.get())*float(amount.get())/100', \
                                           'netamount=float(amount.get())+float(gst.get())'],      
        'masterUpdates'         : [] #use column names only on right hand side 
        }
#'condition': ['item.itemname = 'Item01'],
if __name__ == "__main__":
    rootframe = Tk() 
    createTransRootFrame(rootframe, myparam1)
#=============================================================================
