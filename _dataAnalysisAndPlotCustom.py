from _reportDataAnalysisPlotCustomFunctions import *
#-----------------------------------------------------------------------------
# User Defined Plots and Data Analysis
#-----------------------------------------------------------------------------
# plot 1
#-----------------------------------------------------------------------------
def plotshowroomnameandrent(frame):
        sql = "select showroomname, rentpermnth from showroom"
        charttype = 'plot' #'plot','bar','hist'
        xcol = 'showroomname'
        ycol = 'rentpermnth'
        title = 'Showroom Name and Rent Per Month'
        xlabel = 'Name'
        ylabel = 'Rate'
        xticks = ''
        yticks = ''
        executeSelectQueryForPlotAndDA(frame, sql, charttype, title, xlabel, ylabel, xticks, yticks, xcol, ycol)
#-----------------------------------------------------------------------------
# plot 2
#-----------------------------------------------------------------------------

def plotexpensecostandexpensename(frame):
        sql = "select expensename, expensecost from expense"
        charttype = 'bar' #'plot','bar','hist'
        xcol = 'expensename'
        ycol = 'expensecost'
        title = 'Expense Name and Expense Cost'
        xlabel = 'Name'
        ylabel = 'Price'
        xticks = ''
        yticks = ''
        executeSelectQueryForPlotAndDA(frame, sql, charttype, title, xlabel, ylabel, xticks, yticks, xcol, ycol)
#-----------------------------------------------------------------------------
# plot 3
#-----------------------------------------------------------------------------

def plotservicenameandservicecost(frame):
        sql = "select servicename, servicecost from service"
        charttype = 'plot' #'plot','bar','hist'
        xcol = 'servicename'
        ycol = 'servicecost'
        title = 'Sercice Name and Service Cost'
        xlabel = 'Name'
        ylabel = 'Cost'
        xticks = ''
        yticks = ''
        executeSelectQueryForPlotAndDA(frame, sql, charttype, title, xlabel, ylabel, xticks, yticks, xcol, ycol)

#=============================================================================
# standalone start
#=============================================================================
param = {'table':['showroom'],'pk':['showroomcode'],'cbo':['showroomcategory.showroomcategory']}
if __name__ == "__main__":
        rootframe = Tk()
        plotshowroomnameandrent(rootframe)        
#=============================================================================

