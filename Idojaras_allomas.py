# -*- coding: utf-8 -*-
from sense_hat import SenseHat
from time import sleep
from random import randint
import time
import datetime
import csv
import sys
"""tkinter importálasa Pyton verziótól függően"""
if (sys.version_info > (3, 0)):
     # Python 3 code in this block
    from tkinter import *
    from tkinter import messagebox
else:
     # Python 2 code in this block
     from Tkinter import *
     import tkMessageBox
"""deklaráció és kezdőértek adás"""
master = Tk()
master.title("Weather station")
master.geometry('800x415+0+35')
sense = SenseHat()
sense.clear()
check_frequency = 3000
text_speed = 0.09
red = (255,0,0)
green = (0,255,0)
font_size=44
message1 = StringVar()
message2 = StringVar()
message3 = StringVar()
message4 = StringVar()
message1.set("Temp: Loading...")
message2.set("Humidity: Loading...")
message3.set("Pressure: Loading...")
message4.set("Last refresh: None")
"""GUI elemek megjelenítése"""
felirat1 = Label( master, textvariable = message1)
felirat1.config(font=font_size)
felirat1.pack ()
felirat2 = Label( master, textvariable = message2)
felirat2.config(font=font_size)
felirat2.pack ()
felirat3 = Label( master, textvariable = message3)
felirat3.config(font=font_size)
felirat3.pack ()
felirat4 = Label( master, textvariable = message4)
felirat4.config(font=font_size)
felirat4.pack ()
photo = PhotoImage(file="/home/pi/Documents/images.gif")
logo = Label(master, image=photo)
logo.photo = photo
logo.pack()
master.update()
def apply_button_click():
    """Apply gomb megnyomásakor történik"""
    global check_frequency
    try:
        new_freq = int(get_freq.get())
        if int(new_freq) > 0 and int(new_freq)<86401:
            check_frequency = new_freq*1000
            messagebox.showinfo("Info", "Beallitva!")
            sense.show_message("OK!", scroll_speed=text_speed, text_colour=green)
        else:
            messagebox.showinfo("Hiba!", "1 es 86400 kozotti szamot adjon meg!")
            sense.show_message("Hiba", scroll_speed=text_speed, text_colour=red)
    except:
        messagebox.showinfo("Hiba!", "Ez nem szam!")
        sense.show_message("Hiba!", scroll_speed=text_speed, text_colour=red)

"""További GUI elemek megjelenítése, formázása"""   
apply_button = Button (master, text = "Apply", command = apply_button_click)
apply_button.pack (side = BOTTOM)
default_freq = StringVar(master)
default_freq.set("4")
get_freq = Spinbox (master, from_ =1, to = 1000, width=7, textvariable = default_freq)
get_freq.config(justify=CENTER, font=font_size)
get_freq.pack (side=BOTTOM)
felirat5 = Label( master, text = "Check frequency in second: ")
felirat5.config(font=font_size)
felirat5.pack (side=BOTTOM)
master.update()
def getsense_data():
    """A szkript fő, ismétlődő függvénye"""
    """A szenzor adatainak lekérése"""
    temp = None
    humidity = None
    pressure = None
    temp = sense.get_temperature()
    temp = round (temp,1)
    humidity = sense.get_humidity()
    humidity = round (humidity,1)
    pressure = sense.get_pressure()
    pressure = round(pressure,1)
    """Dátum lekérdezés és formátum beállítás"""
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    """Szenzor hiba ellenőrzés"""
    if not date or not temp or not pressure or not humidity:
        messagebox.showinfo("Hiba!", "Nem erkezett adat a szenzortol!")
        sense.show_message("Hiba!", scroll_speed=text_speed, text_colour=red)
        message1.set("Nem erkezett adat a szenzortol!")
        message2.set("Nem erkezett adat a szenzortol!")
        message3.set("Nem erkezett adat a szenzortol!")
        message4.set("Date: "+str(date))
    else:
        try:
            """adatok mentése csv fájlba, GUI-n megjelenő adatok frissítése"""
            with open('/home/pi/Documents/weather_station.csv', mode='a') as weather_station_file:
                data_writer = csv.writer(weather_station_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data_writer.writerow([date, temp, pressure, humidity])
                message1.set("Temp: "+str(temp)+" °C")
                message2.set("Humidity: "+str(humidity)+" %")
                message3.set("Pressure: "+str(pressure)+" hPa")
                message4.set("Last refresh: "+str(date))                
        except IOError:
            messagebox.showinfo("Hiba!", "Hiba a file irasakor!")
            sense.show_message("Hiba!", scroll_speed=text_speed, text_colour=red)
    master.after (check_frequency,getsense_data)
master.after(3000,getsense_data())
master.mainloop()
