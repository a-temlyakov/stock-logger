import threading
from time import localtime, strftime
import stock
import signal

__author__ = "Andrew Temlyakov"
__licence__ = "GPL"
__version__ = "3"
__maintainer__ = "Andrew Temlyakov"
__email__ = "temlyaka@email.sc.edu"

class Timer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.symbol = "GOOG"
        self.interval = 5.0
        self.filename = "GOOG.txt"
        self.f = 0

    def config(self, symbol, interval, filename):
        self.symbol = symbol
        self.interval = interval
        self.filename = filename

    def run(self):
        self.f = open(self.filename, "w")
        while not self.event.is_set():
            #Try to get value 3 times, then give up
            for i in range(3):
                try:
                    stock_price = stock.get_price(self.symbol)
                    break
                except IOError:
                    stock_price = 0
                    self.event.wait(1)

            self.f.write(stock_price + "\n")
            self.f.flush()
            self.event.wait(self.interval)

    def stop(self):
    	self.event.set()
        self.f.close()
