
from _libraryAndDBConnection import * #includes database connection and cursor setting strings

#drop database mastertrans2022

#-----------------------------------------------------------------------------
'''
Use options here to:
    - fetch database information
    - to create tables
    - to alter table structures
in the specified database.
'''
#-----------------------------------------------------------------------------
#=============================================================================
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
#=============================================================================
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
#=============================================================================
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
#=============================================================================
def backupDatabase(frame):
    try:
        dbuser = myuser
        dbpassword = mypassword
        dbname = mydatabase
        dbhost = myhost
        #backuppath = 'd:\\' #by default create backup in the app folder
        datetime = time.strftime('%d-%m-%Y_%H-%M-%S') #space and symbols in filename does not work! So, use '_' or '-'
        filename = dbname+datetime+".sql" #space in filename does not work! So, use '_'
        f = "C:\\xampp\\mysql\\bin\\mysqldump  -h "+dbhost+" -u "+dbuser+" -p "+dbpassword+" "+dbname+" > "+dbname+datetime+".sql"
        os.system(f)
        tkmsgbox.showinfo("IMPORTANT!", "MySQL Database "+dbname+" backed up successfully as "+filename+".", parent=frame)
    except Exception as e:
        #tkmsgbox.showinfo("Oops!","Error: %s" % e, parent=databaserootframe)
        tkmsgbox.showinfo("Oops!","Error: %s" % e, parent=frame)
#=============================================================================
def restoreDatabase(frame):
    #Restoring from a mysql database backup file
    #mysql -u yourusername -h yourusername.mysql.pythonanywhere-services.com 'yourusername$dbname'  < db-backup.sql
    try:
        db = mydatabase+'_restored'
        dbhost = myhost
        dbuser = myuser
        dbpassword = mypassword
        dbname = mydatabase
        
        dbRestoreFRM = Toplevel(bg='red')
        dbRestoreFRM.title('Restore MySQL Database')
        dbRestoreFRM.configure(background="#00ff22")
        #dbRestoreFRM.transient()
        w, h = dbRestoreFRM.winfo_screenwidth()-20, 200
        dbRestoreFRM.geometry("%dx%d+0+0" % (w, h))
        
        labl = Label(dbRestoreFRM, text="MySQL Database Backup SQL File")
        labl.grid(row=1, column=1)
        dbbackupsqlfiletxt = Text(dbRestoreFRM, height=3, width=100)
        Label(dbRestoreFRM, text="").grid(row=0, column=0)    #empty label for padding
        Label(dbRestoreFRM, text="").grid(row=2, column=0)    #empty label for padding
        Label(dbRestoreFRM, text="").grid(row=4, column=0)    #empty label for padding
        dbbackupsqlfiletxt.grid(row=1, column=2, columnspan=2)
        def selectsqlfilebtnevent():
            filetypes = (('sql files','*.sql'),('All files','*.*'))
            filename = filedialog.askopenfilename(parent=dbRestoreFRM, title='Select sql file',initialdir='/',filetypes=filetypes)
            #tkmsgbox.showinfo(title='Selected File',message=filename)
            dbbackupsqlfiletxt.delete('1.0', END)
            dbbackupsqlfiletxt.insert(INSERT, filename)
        selectsqlfilebtn = Button(dbRestoreFRM,text='Select sql File',command=selectsqlfilebtnevent)
        selectsqlfilebtn.grid(row=3, column=2)
        paddinglbl = Label(dbRestoreFRM, text="").grid(row=0, column=0)    
        def dbRestorebtnevent():
            #labl.configure(text="...restoring mysql database")
            dbbackupsqlfile = dbbackupsqlfiletxt.get('1.0','end-1c')            
            #tkmsgbox.showinfo(title='SQL File to be restored ',message=dbbackupsqlfile)
            #f = "C:\\xampp\\mysql\\bin\\mysql -h "+dbhost+" -u "+dbuser+" -p "+dbpassword+" "+dbname+" < "+dbbackupsqlfile
            #f = "C:\\xampp\\mysql\\bin\\mysql -u root -p -h localhost 'root$dbname'  < "+dbbackupsqlfile
            f = 'C:\\xampp\\mysql\\bin\\mysql -h localhost -u root -p '+dbname+' < "'+dbbackupsqlfile+'"'
            #IMPORTANT! - use " " and not ' ' to enclose sql filename as ' ' does not work on CMD
            os.system(f)
            #print("MySQL Database Backup file created as "+filename+".")
            tkmsgbox.showinfo("IMPORTANT!", "MySQL Database "+db+" restored.", parent=frame)
        dbRestorebtn = Button(dbRestoreFRM, text ="Restore MySQL Database", command=dbRestorebtnevent)
        dbRestorebtn.grid(row=5, column=2)
    except Exception as e:
        #tkmsgbox.showinfo("Oops!","Error: %s" % e, parent=rootmain)
        tkmsgbox.showinfo("Oops!","Error: %s" % e, parent=frame)
#=============================================================================
def createNewDatabase(frame,db):
        try:
                #create mysql database, if does not exist
                #tkmsgbox.showinfo("IMPORTANT!", "Setting up MySQL Database.", parent=rootmain)

                #tkmsgbox.showinfo("IMPORTANT!", "Setting up MySQL Database.")
                #conn = pymysql.connect(host='localhost', user='root', password='')
                #cursor = conn.cursor()
                #create mysql database
                cursor.execute("CREATE DATABASE IF NOT EXISTS "+db)
                #open mysql database
                conn = pymysql.connect( host="localhost",user="root",password="",database= db,cursorclass=pymysql.cursors.DictCursor)
                cursor = conn.cursor()
                msg = "SUCCESS: Database "+ db +" created successfully."
                tk.messagebox.showinfo("MESSAGE", msg, parent=frame)
        except conn.Error as e:
                msg = "ERROR: "+str(e.args[0])+e.args[1]
                tk.messagebox.showinfo("MESSAGE", msg, parent=frame)
#=============================================================================
def resetDatabase(frame,db):
    try:
        #open mysql database, if exists
        #conn = pymysql.connect( host='localhost',user='root',port='',password='',db=db,cursorclass=pymysql.cursors.DictCursor)
        #cursor=conn.cursor()
        #tkmsgbox.showinfo("MESSAGE", "Database "+mydb+" is all set and open.")
        #-------------
        #drop database - disable after testing
       
        cursor.execute("drop database if exists " +db)
        conn.commit()
        createNewDatabase(frame, db)
        tkmsgbox.showinfo("Oops!","Error: %s" % e, parent=frame)
    except Exception as e:
        #tkmsgbox.showinfo("Oops!","Error: %s" % e, parent=rootmain)
        tkmsgbox.showinfo("Oops!","Error: %s" % e, parent=frame)
#=============================================================================

def createTablesWithTestData(frame):
    cursor = conn.cursor()    
    #Creating Tables with Test Data:
    #---- item      ()
    #---- supplier  ()
    #---- customer  ()
    #---- purchase  ()
    #---- sales     ()
    try:
        tkmsgbox.showinfo("MESSAGE!", "Creating tables with test data...", parent=frame)
        #conn = mysql.connector.connect(host="localhost",user="root",password="",database=db)
        #cursor = conn.cursor(dictionary=True)
        
        #================================================================
        #!IMPORTANT: date column should be named something as 'transdate', 'pdate', 'sdate', 'doj' etc. BUT NOT AS 'date'
        #================================================================
        tbl=""
        try:
                sql = """DROP TABLE showroom"""
                cursor.execute(sql)
                conn.commit()
        except conn.Error as e:
                pass
        tbl = "create showroom"
        sql = """CREATE TABLE IF NOT EXISTS showroom(
                    showroomcode VARCHAR(30) PRIMARY KEY,
                    showroomname VARCHAR(30),
                    rentpermnth DECIMAL(8,2),
                    showroomcategory VARCHAR(30),
                    floornum int(10),
                    rentgstrate DECIMAL(5,2)
                    )"""
        cursor.execute(sql)
        conn.commit()
        cursor.execute("DELETE FROM showroom")
        conn.commit()
        tbl = "insert showroom"        
        sql = """INSERT INTO showroom VALUES
                    ('akag01','H&M',200000,'CLOTHING',1,12),
                    ('akag02','BIG BASKET',150000,'GROCERY',2,12),
                    ('akag03','JASPO',90000,'SPORTS',2,11),
                    ('akag04','TITAN',120000,'WATCHES',1,13),
                    ('akag05','TANISHQ',100000,'JWELLERY',3, 100)
                    """
        cursor.execute(sql)
        conn.commit()
        
        try:
                sql = """DROP TABLE showroomcategory"""
                cursor.execute(sql)
                conn.commit()
        except conn.Error as e:
                pass

        tbl = "create showroomcategory"
        sql = """CREATE TABLE IF NOT EXISTS showroomcategory(
                    showroomcategory VARCHAR(30) PRIMARY KEY
                    )"""
        cursor.execute(sql)
        conn.commit()
        cursor.execute("DELETE FROM showroomcategory")
        tbl = "insert showroomcategory"
        sql = """INSERT INTO showroomcategory VALUES
                    ('CLOTHING'),
                    ('SPORTS'),
                    ('GROCERY'),
                    ('WATCHES')
                    
                    """
        cursor.execute(sql)
        conn.commit()


        try:
                sql = """DROP TABLE employee"""
                cursor.execute(sql)
                conn.commit()
        except conn.Error as e:
                pass
        
        tbl = "create employee"
        sql = """CREATE TABLE IF NOT EXISTS employee(
                    emp_id INT PRIMARY KEY,
                    emp_name VARCHAR(30),
                    emp_mobile VARCHAR(10),
                    emp_category VARCHAR(30)
                    )"""
        cursor.execute(sql)
        conn.commit()
        cursor.execute("DELETE FROM employee")
        conn.commit()

        tbl = "insert employee"
        sql = """INSERT INTO employee VALUES
                    (1,'emp01','9411107750','Salesman'),
                    (2,'emp02','9817612569','Manager'),
                    (3,'emp03','7891235490','Security'),
                    (4,'emp04','9412189011','Cleaning'),
                    (5,'emp05','9413189022','Salesman')
                    """
        cursor.execute(sql)
        conn.commit()

        try:
                sql = """DROP TABLE employeecategory"""
                cursor.execute(sql)
                conn.commit()
        except conn.Error as e:
                pass
        tbl = "create employeecategory"
        sql = """CREATE TABLE IF NOT EXISTS employeecategory(
                    employeecategory VARCHAR(30) PRIMARY KEY
                    )"""
        cursor.execute(sql)
        conn.commit()
        cursor.execute("DELETE FROM employeecategory")
        tbl = "insert employeecategory"
        sql = """INSERT INTO employeecategory VALUES
                    ('Salesman'),
                    ('Manager'),
                    ('Security')
                    """
        cursor.execute(sql)
        conn.commit()
        
        try:
                sql = """DROP TABLE service"""
                cursor.execute(sql)
                conn.commit()
        except conn.Error as e:
                pass
        
        tbl = "create service"
        sql = """CREATE TABLE IF NOT EXISTS service(
                    servicecode INT PRIMARY KEY,
                    servicename VARCHAR(30),
                    servicecost DECIMAL(8,2),
                    servicecategory VARCHAR(30)
                    )"""
        cursor.execute(sql)
        conn.commit()
        cursor.execute("DELETE FROM service")
        conn.commit()
        tbl = "insert service"
        sql = """INSERT INTO service VALUES
                    (1,'Cabinet',150,'STORAGE'),
                    (2,'Parking',300,'VEHICAL')
                    """
        cursor.execute(sql)
        conn.commit()

        try:
                sql = """DROP TABLE servicecategory"""
                cursor.execute(sql)
                conn.commit()
        except conn.Error as e:
                pass
        
        tbl = "create servicecategory"
        sql = """CREATE TABLE IF NOT EXISTS servicecategory(
                    servicecategory VARCHAR(30) PRIMARY KEY
                    )"""
        cursor.execute(sql)
        conn.commit()
        cursor.execute("DELETE FROM servicecategory")
        tbl = "insert servicecategory"
        sql = """INSERT INTO servicecategory VALUES
                    ('STORAGE'),
                    ('VEHICAL')
                    """
        cursor.execute(sql)
        conn.commit()

        try:
                sql = """DROP TABLE expensecategory"""
                cursor.execute(sql)
                conn.commit()
        except conn.Error as e:
                pass
        
        tbl = "create expensecategory"
        sql = """CREATE TABLE IF NOT EXISTS expensecategory(
                 expensecategory VARCHAR(30) PRIMARY KEY
                 )"""
        cursor.execute(sql)
        conn.commit()
        cursor.execute("DELETE FROM expensecategory")
        tbl = "insert expensecategory"
        sql = """INSERT INTO expensecategory VALUES
                    ('Maintainance')
                    """
        cursor.execute(sql)
        conn.commit()
        try:
                sql = """DROP TABLE expense"""
                cursor.execute(sql)
                conn.commit()
        except conn.Error as e:
                pass
        tbl = "create expense"
        sql = """CREATE TABLE IF NOT EXISTS expense(
                    expensecode VARCHAR(30) PRIMARY KEY,
                    expensecategory VARCHAR(30),
                    expensename VARCHAR(30),
                    expensecost DECIMAL(10,2),
                    expensegstrate DECIMAL(5,2)
                    )"""
        cursor.execute(sql)
        conn.commit()
        cursor.execute("DELETE FROM expense")
        conn.commit()
        tbl = "insert expense"
        sql = """INSERT INTO expense VALUES
                    ('1452', 'Maintainance', 'Electricity', 50000,12),
                    ('1145', 'Maintainance', 'Cleaning', 60000, 6)
                    """
        cursor.execute(sql)
        conn.commit()

        try:
                sql = """DROP TABLE transexpense"""
                cursor.execute(sql)
                conn.commit()
        except conn.Error as e:
                pass
        tbl = "create transexpense"
        sql = """CREATE TABLE IF NOT EXISTS transexpense(
                    pdate DATE,
                    invoice VARCHAR(30),
                    expensecode INT,
                    expensename VARCHAR(30),
                    expensecategory VARCHAR(30),
                    expensegstrate DECIMAL(5,2),
                    cost DECIMAL(10,2),
                    gst DECIMAL(10,2),
                    netamount DECIMAL(10,2)
                    )"""
        cursor.execute(sql)
        conn.commit()

        try:
                sql = """DROP TABLE income"""
                cursor.execute(sql)
                conn.commit()
        except conn.Error as e:
                pass
        tbl = "create income"
        sql = """CREATE TABLE IF NOT EXISTS income(
                    sdate DATE,
                    incomecd VARCHAR(30) PRIMARY KEY,
                    showroomcode VARCHAR(30),
                    showroomname VARCHAR(30),
                    showroomcategory VARCHAR(30),
                    rentgstrate DECIMAL(5,2),
                    rent DECIMAL(10,2),
                    month INT,
                    amount DECIMAL(10,2),
                    gst DECIMAL(10,2),
                    netamount DECIMAL(10,2)
                    )"""
        cursor.execute(sql)
        conn.commit()
        
       
        tkmsgbox.showinfo("SUCCESS MESSAGE!","New tables created successfully with dummy values.", parent=frame)
    #except Exception as e:
    #    tkmsgbox.showinfo("Oops!","Error: %s" % e, parent=frame)
    except conn.Error as e:
                msg = "ERROR: "+str(e.args[0])+e.args[1]
                tk.messagebox.showinfo("MESSAGE",tbl+" "+msg, parent=frame)

#=============================================================================
def descTable(frame,table):
        try:
                sql = "desc "+table
                cursor.execute(sql)
                data = cursor.fetchall() #list of dict with one common key 'Field'
                df = pd.DataFrame(data)
                return df
        except conn.Error as e:
                msg = "ERROR: "+str(e.args[0])+e.args[1]
                tk.messagebox.showinfo("MESSAGE", msg, parent=frame)
#=============================================================================
def displayPandasTable(frame,df,r=0,c=0,w=400,h=400,bkcolor='orange'):
        #global pandasTableFRM
        pandasTableFRM = Frame(frame, width=w, height=h)
        pandasTableFRM.grid(row=r, column=c, sticky='NW')
        #pt = Table(pandasTableFRM1, dataframe=df, showtoolbar=True, width=w, height=h, showstatusbar=True)
        pt = Table(pandasTableFRM, dataframe=df, width=w, height=h)  
        pt.cellbackgr = bkcolor
        pt.grid()
        pt.show()
        #for insert disable the following event handling; enable it for update only
        def leftButtonClickEvent(event): #left-button click event handling
                rowclicked = pt.get_row_clicked(event)
                rowDataList = pt.model.df.loc[rowclicked] #Series
                updateARow(rowDataList)
        pt.rowheader.bind('<Button-1>',leftButtonClickEvent)
#=============================================================================
# child frames
#=============================================================================
def createDatabaseChildFrames(databaserootframe):
        
        frame = Frame(databaserootframe)
        frame.grid(row=0, column=0, rowspan=2, sticky='NW', padx=15, pady=15) #W-left, E-right, N-top, S-bottom

        r=0
        Label(frame, text='Database:').grid(row=r, column=0, sticky='NW')
        databaseTXT = Entry(frame, width=35)
        databaseTXT.grid(row=r, column=1, sticky='NW')
        #databaseTXT.delete('1.0', END)
        databaseTXT.insert(INSERT, mydatabase)
        
        r += 1
        Label(frame, text='TABLES:').grid(row=r, column=0, sticky='NW')
        tablesVar = StringVar()
        lookupvals = showTablesInADatabase(frame)
        tablesCBO = Combobox(frame, name='tablecbo', width=35, textvariable=tablesVar) #,width=30)
        tablesCBO['values'] = lookupvals
        tablesCBO.grid(row=r, column=1, sticky='NW')
        def tablesCBOSelectedEvent(event):
                table = event.widget.get()
                w, h = databaserootframe.winfo_screenwidth()-50, databaserootframe.winfo_screenheight()-150
                w = w*60/100
                h = h*40/100
                r=0; c=1; color='orange'
                df = table2df(databaserootframe,table)
                displayPandasTable(databaserootframe,df,r,c,w,h,color)
                r=1; c=1; color='blue'
                df = descTable(databaserootframe,table)
                displayPandasTable(databaserootframe,df,r,c,w,h,color)
        tablesCBO.bind("<<ComboboxSelected>>", tablesCBOSelectedEvent)

        r += 1
        Label(frame, text='Execute Raw SQL Query (Only DDL):').grid(row=r, column=0, columnspan=2, sticky='NW')
        r += 1
        # Raw SQL Query Execution
        rawDDLSQLQueryTXT = Text(frame, width=50, height=15)
        rawDDLSQLQueryTXT.grid(row=r, column=0, columnspan=2, sticky='NW')
        def rawDDLSQLQueryBTNEvent():
                sql = rawDDLSQLQueryTXT.get("1.0",'end-1c')   #for TEXT widget use parameters
                sqlQueryExecution(frame, sql)
                #fire tablescbo combobox click-event programmatically
                #tablesCBO.invoke()
                idx = lookupvals.index(table)
                tablesCBO.current(idx)
                tablesCBO.event_generate('<<ComboboxSelected>>')
        r += 1
        rawDDLSQLQueryBTN = Button(frame, text='Execute Raw SQL Query (Only DDL)', command=rawDDLSQLQueryBTNEvent)
        rawDDLSQLQueryBTN.grid(row=r, column=0, columnspan=2, padx=20, pady=5, sticky='NE')
    
        r += 1
        Label(frame, text='CREATE NEW DATABASE').grid(row=r, column=0, columnspan=2, sticky='NW')
        r += 1
        Label(frame, text='New Database: ').grid(row=r, column=0, sticky='NW')
        createNewDatabaseTXT = Entry(frame, width=35)
        createNewDatabaseTXT.grid(row=r, column=1, sticky='NW')
        #createNewDatabaseTXT.delete('1.0', END)
        createNewDatabaseTXT.insert(INSERT, mydatabase) 
        r += 1
        def createNewDatabaseBTNEvent():
                db = createNewDatabaseTXT.get()
                createNewDatabase(db)
        createNewDatabaseBTN = Button(frame, text='Create Database', command=createNewDatabaseBTNEvent)
        createNewDatabaseBTN.grid(row=r, column=0, columnspan=2, padx=20, pady=5, sticky='NE')

        r += 1
        Label(frame, text='Create Tables With Test Data: ').grid(row=r, column=0, columnspan=2, sticky='NW')
        r += 1
        Label(frame, text='(As per the detail in createTablesWithTestData() function.').grid(row=r, column=0, \
                        columnspan=2, sticky='NW')
        r += 1
        def createTablesWithTestDataBTNEvent():
                db = databaseTXT.get()
                createTablesWithTestData(db)
        createTablesWithTestDataBTN = Button(frame, text='Create Tables with Test Data', command=createTablesWithTestDataBTNEvent)
        createTablesWithTestDataBTN.grid(row=r, column=0, columnspan=2, padx=20, pady=5, sticky='NE')

        r += 1
        def backupDatabaseBTNEvent():
                backupDatabase()
        backupDatabaseBTN = Button(frame, text='Backup Database', command=backupDatabaseBTNEvent)
        backupDatabaseBTN.grid(row=r, column=0, columnspan=2, padx=20, pady=5, sticky='NW')

        r += 1
        def restoreDatabaseBTNEvent():
                restoreDatabase()
        restoreDatabaseBTN = Button(frame, text='Restore Database', command=restoreDatabaseBTNEvent)
        restoreDatabaseBTN.grid(row=r, column=0, columnspan=2, padx=20, pady=5, sticky='NW')

        '''
        r += 1
        Label(frame, text='Reset Database').grid(row=r, column=0, columnspan=2, sticky='NW')
        r += 1
        def resetDatabaseBTNEvent():
                db = databaseTXT.get()
                resetDatabase(db)
        resetDatabaseBTN = Button(frame, text='Reset Database', command=resetDatabaseBTNEvent)
        resetDatabaseBTN.grid(row=r, column=0, columnspan=2, padx=20, pady=5, sticky='NW')
        '''
        
        for widget in frame.winfo_children():
                widget.grid(padx=0, pady=5)        

#=============================================================================
# root frame
#=============================================================================
def createDatabaseFrame(rootframe):
        w, h = rootframe.winfo_screenwidth()-50, rootframe.winfo_screenheight()-150
        databaserootframe = Toplevel(rootframe)
        databaserootframe.geometry("%dx%d+15+60" % (w,h)) 
        databaserootframe.title("MANAGE DATABASE")
        createDatabaseChildFrames(databaserootframe)
        #createDatabase()
        #createTablesWithTestData()
#=============================================================================
# standalone start
#=============================================================================
if __name__ == "__main__":
    rootframe = Tk() 
    createDatabaseFrame(rootframe)
#=============================================================================
