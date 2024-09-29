from _libraryAndDBConnection import * #includes database connection and cursor setting strings
#custom library files
'''
#Generic Files
#-------------
import _dataAnalysisAndPlot
import _database
import _dataExportImport
import _exportImport
import _libraryAndDBConnection
import _masterCRUD
import _report
import _transaction
import _about
import _
'''
#Custom Files
#------------
import _master                  #for new
import _edit                    #for edit
import _report                  #for report 
import _transaction             #for transaction
import _dataAnalysisAndPlot     #for data analysis & plot 
import _database                #for database management
import _about
import _reportCustom
import _dataExportImport
import _dataAnalysisAndPlotCustom
'''
import _dataImport              #for data import  
import _dataExport              #for data export
'''
'''
import update
import delete
import report
'''
#====================================================================================
def donothing():
        pass
#====================================================================================
def menu(rootframe):
        #In "param", cbo is a combo box to be filled with lookup values from column of another table
        #use different name for 'param' for each option, otherwise the last only option gets assigned

        menubar = Menu(rootframe)
        #====================================================================
        newmenu = Menu(menubar, tearoff=0)

        pnew1 = {'table':['showroomcategory'],'pk':['showroomcategory'],'cbo':['']} 
        newmenu.add_command(label="Showroom Category",
                            command=lambda: _master.createInsertRootFrame(rootframe, pnew1))
        pnew2 = {'table':['employeecategory'],'pk':['employeecategory'],'cbo':['']} 
        newmenu.add_command(label="Employee Category",
                            command=lambda: _master.createInsertRootFrame(rootframe, pnew2))
        pnew3 = {'table':['servicecategory'],'pk':['servicecategory'],'cbo':['']} 
        newmenu.add_command(label="Service Category",
                            command=lambda: _master.createInsertRootFrame(rootframe, pnew3))
        pnew8 = {'table':['expensecategory'],'pk':['expensecategory'],'cbo':['']} 
        newmenu.add_command(label="Expense Category",
                            command=lambda: _master.createInsertRootFrame(rootframe, pnew8))

        newmenu.add_separator()
                
        pnew4 = {'table':['showroom'],'pk':['showroomcode'],'cbo':['showroomcategory.showroomcategory']}  
        newmenu.add_command(label="Showroom",
                            command=lambda: _master.createInsertRootFrame(rootframe, pnew4)) #use lambda to pass arguments to the function        
        pnew5 = {'table':['employee'],'pk':['employeeid'],'cbo':['employeecategory.employeecategory']} 
        newmenu.add_command(label="Employee",
                            command=lambda: _master.createInsertRootFrame(rootframe, pnew5))
        pnew6 = {'table':['service'],'pk':['servicecode'],'cbo':['servicecategory.servicecategory']} 
        newmenu.add_command(label="Service",
                            command=lambda: _master.createInsertRootFrame(rootframe, pnew6))
        pnew7 = {'table':['expense'],'pk':['invoice'],'cbo':['expensecategory.expensecategory']} 
        newmenu.add_command(label="Expense",
                            command=lambda: _master.createInsertRootFrame(rootframe, pnew7))
        

        newmenu.add_separator()
        '''

        pnew7 = {'table':['unit'],'pk':['unit']} 
        newmenu.add_command(label="Unit of Measurement",
                            command=lambda: _master.createInsertRootFrame(rootframe, pnew7))
        '''
        menubar.add_cascade(label="NEW", menu=newmenu)
        #====================================================================
        editmenu = Menu(menubar, tearoff=0)
        eparam1 = {'table':['showroom'],'pk':['showroomcode'],'cbo':['showroomcategory.showroomcategory']}
        editmenu.add_command(label="Showroom",
                    command=lambda: _edit.createEditRootFrame(rootframe, eparam1))#use lambda to pass arguments to the function

        eparam2 = {'table':['employee'],'pk':['employeeid'],'cbo':['employeecategory.employeecategory']}
        editmenu.add_command(label="Employee",
                    command=lambda: _edit.createEditRootFrame(rootframe, eparam2))
        eparam3 = {'table':['service'],'pk':['servicecode'],'cbo':['servicecategory.servicecategory']}
        editmenu.add_command(label="Service",
                             command=lambda: _edit.createEditRootFrame(rootframe, eparam3))
        eparam7 = {'table':['expense'],'pk':['invoice'],'cbo':['expensecategory.expensecategory']} 
        editmenu.add_command(label="Expense",
                            command=lambda: _edit.createEditRootFrame(rootframe, eparam7))
        
        
        editmenu.add_separator()
        
        editbox = Menu(editmenu)
        eparam4 = {'table':['showroomcategory'],'pk':['showroomcategory'],'cbo':['']}
        editbox.add_command(label="Showroom Category",
                    command=lambda: _edit.createEditRootFrame(rootframe, eparam4))
        eparam5 = {'table':['employeecategory'],'pk':['employeecategory'],'cbo':['']}
        editbox.add_command(label="Employee Category",
                    command=lambda: _edit.createEditRootFrame(rootframe, eparam5))
        eparam6 = {'table':['servicecategory'],'pk':['sevicecategory'],'cbo':['']}
        editbox.add_command(label="Service Category",
                    command=lambda: _edit.createEditRootFrame(rootframe, eparam6))
        eparam8 = {'table':['expensecategory'],'pk':['expensecategory'],'cbo':['']} 
        editbox.add_command(label="Expense Category",
                            command=lambda: _edit.createEditRootFrame(rootframe, eparam8))
        editmenu.add_cascade(label = 'Categories', menu = editbox)
        menubar.add_cascade(label="EDIT", menu=editmenu)
        #====================================================================
        transmenu = Menu(menubar, tearoff=0)

        # !IMPORTANT: date column should be named something as 'transdate' not as 'date'
        # Do not change 'keys' of the following dictionaries
        # use column names only on right hand side of an expression
        # 'invisible' - is the simple assignment which is to be saved in trans table BUT NOT to be displayed on screen
        # in this inventory system, item table contains average item price updated after every purchase
        # masterCBO - a master combobox whose selection will change the drop-down list of its child combobox
        # mastercbo tbl.col#childcbo tbl.col
        # whereas masterLookupItems is a combobox whose selection will fill textfields with autofill values
        
        tparam1 = {

                'table'                 : ['transexpense'],

                'pk'                    : ['invoice'],

                'dateColumn'            : "pdate",  

                'masterCBO'             : ['expense.expensecategory#expense.expensename'],
                'masterLookupItems'     : ['expense.expensename'],
                'masterPrimaryKeys'     : ['expense.expensecode'],
                'masterAutofillValues'  : ['expense.expensegstrate','expense.expensecost'],

                'transItems'            : ['cost'],

                'condition'             : [],

                'expressions'           : [
                                           'gst = float(expensegstrate.get()) * float(cost.get()) / 100', 
                                           'netamount = float(cost.get()) + float(gst.get())', 
                                           ],

                'invisible'             : [
                                           'expensecategory = expensecategory.get()',  
                                           'expensename = expensename.get()',
                                           'expensecode = expensecode.get()',
                                           'expensegstrate = expensegstrate.get()',
                                           ],

                'masterUpdates'         : ['expense.expensecost = ( float(cost.get()) + \
                                                                   float(gst.get())  )'
                                          ],                                               

                }
        

        transmenu.add_command(label="Expense", command=lambda: _transaction.createTransRootFrame(rootframe, tparam1))
        transmenu.add_separator()
        tparam2 = {
                'table'                 : ['income'],
                
                'pk'                    : ['incomecd'],
                
                'dateColumn'            : 'sdate',
                
                'masterCBO'             : ['showroom.showroomcategory#showroom.showroomname'],
                'masterLookupItems'     : ['showroom.showroomname'],
                'masterPrimaryKeys'     : ['showroom.showroomcode'],
                'masterAutofillValues'  : ['showroom.rentgstrate','showroom.rentpermnth'],

                'transItems'            : ['month'],

                'condition'             : ['showroom.rentpermnth > 0 '],               

                'expressions'           : ['amount=float(rentpermnth.get())*float(month.get())', 
                                           'gst=float(rentgstrate.get())*float(amount.get())/100', 
                                           'netamount=float(amount.get())+float(gst.get())', 
                                           ],

                'invisible'             : [
                                           'rent = rentpermnth.get()',
                                           'showroomcode = showroomcode.get()', 
                                           'showroomname = showroomname.get()', 
                                           'rentgstrate = rentgstrate.get()', 
                                           ],

                
                'masterUpdates'         : [] #use column names only on right hand side 

                }
        
        transmenu.add_command(label="Income", command=lambda: _transaction.createTransRootFrame(rootframe, tparam2))
        menubar.add_cascade(label="TRANSACTIONS", menu=transmenu)
        #====================================================================
        reportmenu = Menu(menubar, tearoff=0)
        rptparam1 = {'table':['showroom'],'pk':['showroomcode'],'cbo':['']}
        reportmenu.add_command(label="Showroom", command=lambda: _report.createSelectRootFrame(rootframe, rptparam1)) #use lambda to pass arguments to the function        
        rptparam2 = {'table':['employee'],'pk':['employeeid'],'cbo':['']}
        reportmenu.add_command(label="Employee", command=lambda: _report.createSelectRootFrame(rootframe, rptparam2))
        rptparam3 = {'table':['service'],'pk':['servicecode'],'cbo':['']}
        reportmenu.add_command(label="Service", command=lambda: _report.createSelectRootFrame(rootframe, rptparam3))
        reportmenu.add_separator()
        #rptparam4 = {'table':['showroom'],'pk':['showroomcode'],'cbo':['']
        reportmenu.add_command(label="Showroom", command=lambda: _reportCustom.rptShowroomDetail(rootframe))
        reportmenu.add_command(label="TransExpense", command=lambda: _reportCustom.rptTransexpenseDetail(rootframe))
        reportmenu.add_command(label="Employee", command=lambda: _reportCustom.rptEmployeeDetail(rootframe))
        reportmenu.add_command(label="Showroom Name", command=lambda:_reportCustom.rptshowroomnamePickupList(rootframe))
        reportmenu.add_command(label="Income Code", command=lambda:_reportCustom.rptincomePickupList(rootframe))
        reportmenu.add_separator()
        reportmenu.add_command(label="MySQL Query", command=lambda:_reportCustom.rptItemDetailConditionalTextbox(rootframe))
        menubar.add_cascade(label="REPORT", menu=reportmenu)
        #====================================================================
        damenu = Menu(menubar, tearoff=0)
        daparam1 = {'table':['showroom'],'pk':['showroomcode'],'cbo':['showroom.showroom']}
        damenu.add_command(label="Data Analysis - Complete",
                    command=lambda: _dataAnalysisAndPlot.createDataAnalysisRootFrame(rootframe, daparam1))
        damenu.add_command(label="Showroom Name & Rent",
                    command=lambda: _dataAnalysisAndPlotCustom.plotshowroomnameandrent(rootframe))
        damenu.add_command(label="Expense Name & Cost",
                    command=lambda: _dataAnalysisAndPlotCustom.plotexpensecostandexpensename(rootframe))
        damenu.add_command(label="Service Name & Cost",
                    command=lambda: _dataAnalysisAndPlotCustom.plotservicenameandservicecost(rootframe))

        #damenu.add_command(label="Data Analysis - Filter (Boolean Indexing)", command=lambda: dataAnalysisFilterData.dataAnalysis(db))
        menubar.add_cascade(label="DATA ANALYSIS", menu=damenu)
        #====================================================================
        dbmenu = Menu(menubar, tearoff=0)
        dbmenu.add_command(label="Export-Import Data", command=lambda: _dataExportImport.index(rootframe))
        dbmenu.add_separator()
        #newdatabase = "d1234"
        #dbmenu.add_command(label="Create Database", command=lambda: _database.createNewDatabase(rootframe,newdatabase))
        dbmenu.add_command(label="Backup Database", command=lambda: _database.backupDatabase(rootframe))
        dbmenu.add_command(label="Create Table", command=lambda: _database.createTablesWithTestData(rootframe))
        dbmenu.add_command(label="Alter Table", command=lambda: _database.alterTable(rootframe))
        dbmenu.add_separator()
        dbmenu.add_command(label="Restore Database", command=lambda: _database.restoreDatabase(rootframe))
        dbmenu.add_command(label="Reset Database", command=lambda: _database.resetDatabase(rootframe))
        dbmenu.add_command(label="Drop Table", command=donothing)
        menubar.add_cascade(label="DATABASE", menu=dbmenu)
        #====================================================================
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command= _about.about)
        helpmenu.add_command(label="Manual & Guide", command=_about.manual)
        helpmenu.add_command(label="Help", command=_about.help)
        menubar.add_cascade(label="HELP", menu=helpmenu)
        #====================================================================
        def clearcursorandconnection():
                #if cursor.open:
                #        cursor.close()
                if conn.open:
                        conn.close() #it will close its dependent cursor on its own
        def exitapp():
                #rootframe.quit() #NOT RECOMMENDED
                clearcursorandconnection()
                rootframe.destroy()
        exitmenu = Menu(menubar, tearoff=0)
        exitmenu.add_command(label="Close Cursor & Connection", command=clearcursorandconnection)
        exitmenu.add_command(label="Exit Application", command=exitapp) #rootframe.destroy
        menubar.add_cascade(label="Exit", menu=exitmenu)
        #==========================================================================
        return menubar
#====================================================================================
