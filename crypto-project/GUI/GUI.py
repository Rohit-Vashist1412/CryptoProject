import pandas as pd
from pycoingecko import CoinGeckoAPI
import datetime
import time
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk

root= tk.Tk()
root.title('Crypto currency viewer')
root.geometry('1280x720')

today = date.today() 
startDate = datetime.date(2010,8,16)
cg = CoinGeckoAPI()
coins = cg.get_coins()
coinList = [sublist["id"] for sublist in coins]
formattedCoinList = [a.capitalize().replace("-"," ") for a in coinList]
currencyList = cg.get_supported_vs_currencies()
formattedCurrencyList = [a.upper() for a in currencyList]

figure = plt.Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(figure, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
toolbar = NavigationToolbar2Tk(canvas, root)

def getGraph():
    coinInput = str(clicked1.get())
    currencyInput = str(clicked2.get())
    coinInput = coinInput.lower().replace(" ","-")
    currencyInput = currencyInput.lower()
    coinData = cg.get_coin_market_chart_range_by_id(
    id= coinInput, vs_currency= currencyInput, from_timestamp=time.mktime(startDate.timetuple()), to_timestamp=time.mktime(today.timetuple()))
    priceData = coinData["prices"]
    priceData = pd.DataFrame(priceData, columns = ["Date", "Price"])
    priceData["Date"] = pd.to_datetime(priceData["Date"], unit ="ms")
    
    figure.clear()
    ax = figure.add_subplot(111)
    df = priceData[['Date','Price']].groupby('Date').sum()
    df.plot(kind='line', legend=True, ax=ax, color='r',marker= None, fontsize=10)
    ax.set_title(f'Price of {coinInput.capitalize()} in {currencyInput.upper()}')
    canvas.draw_idle()

clicked1= tk.StringVar()
clicked1.set("Bitcoin")
coinSelect = tk.OptionMenu(root, clicked1, *formattedCoinList)
coinSelect.pack()

clicked2= tk.StringVar()
clicked2.set("USD")
currencySelect = tk.OptionMenu(root, clicked2, *formattedCurrencyList)
currencySelect.pack()

clicked3 = tk.Button(root, text = "Get Graphs", command =lambda: getGraph())
clicked3.pack()



root.mainloop()
