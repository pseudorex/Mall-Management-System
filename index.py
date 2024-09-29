from _libraryAndDBConnection import * #includes database connection and cursor setting strings
import _menu

#====================================================================================
# rootframe (parent window) to be Tk ()
# rest others (child windows) to be Toplevel() or Frame()
#====================================================================================
#ROOT OR MAIN OR PARENT FRAME
rootframe = Tk() 
rootframe.title('Mall Management System') 
welcometext = ""
#maximize root window with title
w, h = rootframe.winfo_screenwidth()-20, rootframe.winfo_screenheight()-100
rootframe.geometry("%dx%d+0+0" % (w, h)) #root window size 'wxh' at left top coordinates 0,0
rootframe.configure(background="black")
#add background image to main root window using label after resizing the image to fit well within it
mywidth = rootframe.winfo_screenwidth()-20
myheight = rootframe.winfo_screenheight()-100
#BACKGROUND IMAGE
img = Image.open("AKMALL.png") #read the image
resizeimg = img.resize((mywidth, myheight)) #resize the image
bgimg = ImageTk.PhotoImage(resizeimg) #set resized images as bg
#bgimglbl = Label(rootframe, image=bgimg) #place bg image in the label instead of text as in Label(frame, text="text")
bgimglbl = Label(rootframe, compound=tk.BOTTOM, text=welcometext, font='Algerian 30 bold', fg='Black', image=bgimg)
bgimglbl.grid(row=0, column=0, sticky='SW') #place the label in the first row, first column of the main root window; centered by default
#place text field over the bg image at the top centered horizontally
'''
welcometext1 = "Bottom Full Width"
welcomelbl1 = Label(rootframe, height=2, text=welcometext1, font='Helvetica 15 bold', bg= "grey")
welcomelbl1.grid(row=0, column=0, sticky='SEW') #place it in first row, first column of the main root window; centered by default
#place text field over the bg image at the bottom centered horizontally
welcometext2 = "Top Full Width"
welcomelbl2 = Label(rootframe, height=2, text=welcometext2, font='Helvetica 15 bold', bg= "grey")
welcomelbl2.grid(row=0, column=0, sticky='NEW') #place it in first row, first column of the main root window; centered by default
'''
#---------------------------------------------
#GUI - App Menu
menubar = _menu.menu(rootframe)
#---------------------------------------------
#GUI - infinite main root loop
rootframe.config(menu=menubar)
rootframe.mainloop()
