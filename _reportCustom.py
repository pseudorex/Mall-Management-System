from _reportDataAnalysisPlotCustomFunctions import *
from _libraryAndDBConnection import *

#-----------------------------------------------------------------------------
# User Defined Reports
#-----------------------------------------------------------------------------
# report 1
#-----------------------------------------------------------------------------
def rptShowroomDetail(frame):
        sql = "select * from showroom"
        executeSelectQuery(frame, sql)
#-----------------------------------------------------------------------------
# report 3
#-----------------------------------------------------------------------------
def rptTransexpenseDetail(frame):
        sql = "select * from transexpense"
        executeSelectQuery(frame, sql)
#-----------------------------------------------------------------------------
# report 4
#-----------------------------------------------------------------------------
def rptEmployeeDetail(frame):
        sql = "select * from employee"
        executeSelectQuery(frame, sql)
#-----------------------------------------------------------------------------
# report 2
#-----------------------------------------------------------------------------
def rptshowroomnamePickupList(frame1):

        frame = Toplevel()
        frame.configure(background='rosybrown1')
        sql = "select showroomname from showroom"
        df = executeSelectQueryAndReturnDF(frame, sql)
        # GUI 
        # drop-down/pick-up list
        frame.title('Mall Management System')
        Label(frame, text=" ").grid(row=1, column=1, sticky='NE')
        namevar = StringVar()
        namelookupvalues = df['showroomname'].tolist()
        Label(frame, text="Showroom Name").grid(row=2, column=1, sticky='NE')
        nameCBO = Combobox(frame, name='namecbo', width=30, textvariable=namevar)
        nameCBO.grid(row=2, column=2)
        nameCBO['values'] = namelookupvalues
        nameCBO.current(0)
        def nameCBOSelectedEvent(event):
                name = event.widget.get()
                sql = "SELECT * FROM showroom where showroomname='"+name+"'"
                executeSelectQuery(frame, sql)        
        nameCBO.bind("<<ComboboxSelected>>", nameCBOSelectedEvent)
        Label(frame, bg="pink1", text=" ").grid(row=3, column=3, sticky='NE')
#-----------------------------------------------------------------------------
# report 3
#-----------------------------------------------------------------------------
def rptincomePickupList(frame1):

        frame = Toplevel()
        frame.configure(background='rosybrown1')
        sql = "select incomecd from income"
        df = executeSelectQueryAndReturnDF(frame, sql)
        # GUI 
        # drop-down/pick-up list
        frame.title('Mall Management System')
        Label(frame, text=" ").grid(row=1, column=1, sticky='NE')
        namevar = StringVar()
        namelookupvalues = df['incomecd'].tolist()
        Label(frame, text="Income Code").grid(row=2, column=1, sticky='NE')
        nameCBO = Combobox(frame, name='namecbo', width=30, textvariable=namevar)
        nameCBO.grid(row=2, column=2)
        nameCBO['values'] = namelookupvalues
        nameCBO.current(0)
        def nameCBOSelectedEvent(event):
                name = event.widget.get()
                sql = "SELECT * FROM income where incomecd='"+name+"'"
                executeSelectQuery(frame, sql)        
        nameCBO.bind("<<ComboboxSelected>>", nameCBOSelectedEvent)
        Label(frame, bg="pink1", text=" ").grid(row=3, column=3, sticky='NE')
#-----------------------------------------------------------------------------
# report 5
#-----------------------------------------------------------------------------
        
def rptItemDetailConditionalTextbox(rootframe):
        frame = Toplevel()
        frame.configure(background='thistle1')
        Label(frame, text=" ").grid(row=1, column=1, sticky='NE')
        Label(frame, text="SQL Query").grid(row=2, column=1, sticky='NE')
        sqlTXT = Entry(frame, width=30)
        sqlTXT.grid(row=2, column=2, sticky='NW')
        def clickButtonEvent():
                sql = sqlTXT.get()
                executeSelectQuery(frame, sql)        
        Button(frame, text="Submit", command=clickButtonEvent).grid(row=3, column=2, sticky='NW')
        Label(frame, text=" ").grid(row=4, column=3, sticky='NE')
        

#=============================================================================
# standalone start for code testing - to run this file independently
#=============================================================================
param = {'table':['item'],'pk':['itemcode'],'cbo':['itemcategory.itemcategory']}
if __name__ == "__main__":
        rootframe = Tk()
        #createSelectRootFrame(rootframe, param)
        #rptItemDetail(rootframe)                        # report 1
        #rptItemDetailConditionalPickupList(rootframe)       # report 2
        #rptItemDetailConditionalPickupList(rootframe)          # report 3
        
#=============================================================================

