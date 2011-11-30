from Tkinter import *
import tkMessageBox
import stock_timer as st
import time

__author__ = "Andrew Temlyakov"
__licence__ = "GPL"
__version__ = "3"
__maintainer__ = "Andrew Temlyakov"
__email__ = "temlyaka@email.sc.edu"

class App(Frame):

    def __init__(self, master=None):
	    Frame.__init__(self, master)
	    self.grid()
	    self.createWidgets()
	    self.timerlist = []

    def createWidgets(self):
        self.stopButton = Button(self, text="Stop", fg="red", 
                                 command=self.stopstock, state=DISABLED, 
                                 width=40)
        self.stopButton.grid(row=5,column=2)
        self.logStocks = Button(self, text="Begin Log", 
                                command=self.logstocks)
        self.logStocks.grid(row=4,column=1)

        #Set up the text
        Label(self, text="Stock Symbol:").grid(row=1, stick=W)
        Label(self, text="Log at Interval (seconds):").grid(row=2, stick=W)
        Label(self, text="Save to File:").grid(row=3, stick=W)

        #Set up the all entry fields
        self.symbolEntry = Entry(self)
        self.symbolEntry.grid(row=1, column=1)

        self.interval = Entry(self)
        self.interval.grid(row=2, column=1)

        self.filename = Entry(self)
        self.filename.grid(row=3, column=1)

        #Create Message container to show current time
        self.message = Message(self, text="StockLogger 4000", width=200)
        self.message.grid(row=5, columnspan=2)

        self.tableheading = Message(self, text="Symbol | Interval (Sec) | Filename | Status", width=300)
        self.tableheading.grid(row=0, column=2)

        self.listbox = Listbox(self, width=40, height=5, selectmode=SINGLE)
        self.listbox.grid(row=1,column=2, rowspan=4, sticky=(N,W,E,S))

        s = Scrollbar(self, orient=VERTICAL, command=self.listbox.yview)
        s.grid(row=1, column=3, rowspan=4, sticky=(N,S))

        self.listbox['yscrollcommand'] = s.set

    """ Stop all threads when user attempts to abruptly close the program """
    def callback(self):
	    if len(self.timerlist) > 0:
	    	if tkMessageBox.askokcancel("Quit", 
                                        "Do you really wish to quit?\
                                        \nLogging will stop."):
		    for timer in self.timerlist:
			    timer.stop()
		    root.destroy()
	    else:
		    root.destroy()
    
    """ Stop logging a stock when it's selected and stop button is pressed """
    def stopstock(self):
	    selection = self.listbox.curselection()
	    selection = int(selection[0])
	    self.timerlist[selection].stop()
	    self.timerlist.pop(selection)
	    self.listbox.delete(selection, last=None)
 	
	    #if no more stocks are being logged disable the stop button
	    if len(self.timerlist) == 0:
		    self.stopButton.config(state = DISABLED)

    """ Check all input and manage the threads """
    def logstocks(self): 
	    symbol = self.symbolEntry.get()
	    filename = self.filename.get()
	    interval = self.interval.get()

	    try:
		    if int(interval) < 3:
			    tkMessageBox.showerror("Invalid Interval", 
                                       "Interval must be at least 3 seconds")
		    elif filename == "":
			    tkMessageBox.showerror("No Filename", 
                                       "Y U NO GIVE FILENAME?!?!")
		    else: 
			    #create a new thread and start logging!
			    self.listbox.insert(END, symbol + " | " + interval + " | " + 
                                    filename + " | running...")
			    self.timerlist.append(st.Timer())
			    self.timerlist[-1].config(symbol, int(interval), filename)
			    self.timerlist[-1].start()
			    self.stopButton.config(state = NORMAL)
	    except ValueError:
		    tkMessageBox.showerror("Incorrect Input", 
                                   "Incorret input entered - please check.")

    """ Run a real-time clock """
    def tick(self):
        temptime = ""
        newtime = time.strftime("%H:%M:%S")
        if newtime != temptime:
            temptime = newtime
            self.message.config(text = temptime)

        self.message.after(200, self.tick)

root = Tk()
app = App()
root.protocol("WM_DELETE_WINDOW", app.callback)
root.resizable(0,0)
root.title("StockLogger 4000")
app.tick()
app.message.mainloop()
app.mainloop()
