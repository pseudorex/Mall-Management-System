from _reportDataAnalysisPlotCustomFunctions import *

#-------------------------------------------------------------------------------
# Create DataFrame from MySQL database table & then convert df into data for pdf
#-------------------------------------------------------------------------------
def invoicePurchase(frame):
        sql = "select * from item"
        df = executeSelectQueryAndReturnDF(frame, sql)

        # convert dataframe into data for pdf
        dftemp = df.applymap(str)  # Convert all data inside dataframe into string type
        columns = [list(dftemp)]  # Get list of dataframe columns
        rows = dftemp.values.tolist()  # Get list of dataframe rows
        data = columns + rows  # Combine columns and rows in one list

        # additional data to be added to pdf
        sql = "select sum(itemgstrate) as 'total' from item"
        df = executeSelectQueryAndReturnDF(frame, sql)
        additionaldata = str(df.iloc[0,0])

        # Generate PDF File
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", "B", 16)

        pdf.image(name='bvmlogo.png', x=80, y=10, w=7, h=10, type='', link='')
        pdf.cell(w=0, h=10, txt="MY STORE", align='C', new_x="LMARGIN", new_y="NEXT") #w=0 means full page width
        pdf.line(x1=10, y1=20, x2=200, y2=20) # x-horizontal, y-vertical

        pdf.set_font("Times", "", 12)
        pdf.cell(w=30, h=10, txt="Date: ", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(w=30, h=10, txt="July 22, 2023", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(w=30, h=10, txt="Invoice No.: ", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(w=30, h=10, txt="1234 ", new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Times", size=10)

        greyscale = 200
        blue = (255, 255, 255)
        grey = (128, 128, 128)
        headings_style = FontFace(emphasis="ITALICS", color=blue, fill_color=grey)

        with pdf.table(headings_style=headings_style, cell_fill_color=greyscale, cell_fill_mode="ROWS") as table:
            for data_row in data:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)
        if additionaldata is not None:
            pdf.set_font("Times", "B", 14)
            pdf.cell(w=30, h=10, txt=additionaldata, new_x="LMARGIN", new_y="NEXT")
                
        pdf.output("purchase-invoice.pdf")
#-------------------------------------------------------------------------------

#===============================================================================
# standalone start for code testing - to run this file independently
#===============================================================================
param = {'table':['item'],'pk':['itemcode'],'cbo':['itemcategory.itemcategory']}
if __name__ == "__main__":
        rootframe = Tk()
        invoicePurchase(rootframe)         
#===============================================================================

