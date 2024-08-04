import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as ttk
import requests
from datetime import datetime, timezone, timedelta
import pytz
from datetime import datetime
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import locale
# Set locale to English
locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
def show_frame(frame):
    frame.tkraise()

root = ttk.Window(themename="morph")
root.title("Weather App")
root.geometry("1920x1080")
# root.configure(bg="black")

# Create the frames
frame1 = ttk.Frame(root, width=1920, height=1080, style="TFrame")
frame2 = ttk.Frame(root, width=1920, height=1080, style="TFrame")
def get_weather(city):
    # city = input("Enter the city name: ")
    api_key = "c3d72c6f3db342c4ab52b825f9e8df22"
    url1 = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url1)
    data = response.json()

    current_temp = data['main']['temp']
    feel_like = data['main']['feels_like']
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    sunrise = datetime.fromtimestamp(data['sys']['sunrise'], timezone.utc).strftime('%I:%M %p')
    sunset = datetime.fromtimestamp(data['sys']['sunset'], timezone.utc).strftime('%I:%M %p')
    current_date = datetime.fromtimestamp(data['dt'], timezone.utc).strftime('%A %d %B')
    current_time = datetime.fromtimestamp(data['dt'], timezone.utc).strftime('%I:%M %p')
    description = data["weather"][0]["description"]
    city_name = data["name"]
    country = data["sys"]["country"]
    
    icon_id = data["weather"][0]["icon"]
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    image = Image.open(requests.get(icon_url, stream=True).raw)
    resized_image = image.resize((250, 250), Image.LANCZOS)
    icon = ImageTk.PhotoImage(resized_image)
    icon_label.configure(image=icon)
    icon_label.image = icon
    
    date_label.configure(text=f"{current_date},{current_time}")
    temperature_label.configure(text=f"{current_temp}°")
    humidity_d.configure(text=f"{humidity}%")
    low_d.configure(text=f"{pressure}")
    high_d.configure(text=f"{feel_like}°cd ")
    wind_d.configure(text=f"{wind_speed}mph")
    sunrise_d.configure(text=f"{sunrise}")
    sunset_d.configure(text=f"{sunset}")
    description_label.configure(text=f"{description}")
    location_label.configure(text=f"{city_name},{country}")
    
    
# weather for next 5h
    url2 = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"
    response2 = requests.get(url2)
    data2 = response2.json()
    # print(data2)
# 5 hours
    h5={}  
    for i in range(8):
        hour = data2['list'][i]['dt_txt']
        hshoort=hour[:16]
        dateshort=hour[:10]
        date_obj = datetime.strptime(dateshort, '%Y-%m-%d')
        datef=date_obj.strftime('%A %d %B')
        timef=f"{datef},{hshoort[-5:]}"
        timef=timef[:3]+timef[6:]
        # print(timef)
        temperature = data2['list'][i]['main']['temp']-273.15
        humidity = data2['list'][i]['main']['humidity']
        wind_speed = data2['list'][i]['wind']['speed']
        
        icon_id= data2['list'][i]['weather'][0]["icon"]
        
        # print(icon_id)
        h={"hour":timef,"temp":temperature,"hum":humidity, "wind":wind_speed,"icon":icon_id}
        
        # print(h)
        h5[i]=h
    # print(h5)
    Y=150
    for j in range(8):
        
        h1=ttk.Label(frame2, text=f"{h5[j]['hour']}", foreground="black", font=("Helvetica", 16,"bold") )
        h1.place(x=1130,y=Y)
        X=1320
        icon_url1 = f"https://openweathermap.org/img/wn/{h5[j]["icon"]}@2x.png"
        image = Image.open(requests.get(icon_url1, stream=True).raw)
        resized_image = image.resize((70, 70), Image.LANCZOS)
        icon = ImageTk.PhotoImage(resized_image)
        icon_label1=ttk.Label(frame2,image=icon)
        icon_label1.place(x=X+100, y=Y)
        icon_label1.image = icon
        temp1=ttk.Label(frame2, text=f"{h5[j]['temp']:.2f}°", foreground="black", font=("Helvetica", 16) )
        temp1.place(x=X+(100*2), y=Y)
        temp2=ttk.Label(frame2,text="temperature", foreground="black")
        temp2.place(x=X+(100*2), y=Y+40)
        humidity1=ttk.Label(frame2, text=f"{h5[j]['hum']}%", foreground="black", font=("Helvetica", 16) )
        humidity1.place(x=X+(100*3)+40, y=Y)
        hum2=ttk.Label(frame2,text="Humidity", foreground="black")
        hum2.place(x=X+(100*3)+20, y=Y+40)        
        wind1=ttk.Label(frame2, text=f"{h5[j]['wind']}mph", foreground="black", font=("Helvetica", 16) )
        wind1.place(x=X+(100*4)+20, y=Y)
        wind2=ttk.Label(frame2,text="Wind", foreground="black")
        wind2.place(x=X+(100*4)+20, y=Y+40) 
        line0=ttk.Label(frame2,text="________________________________________________________________________________________________________________________", foreground="black")
        line0.place(x=1160,y=Y+70)
        Y+=100
# 5days
    
    api_key = "c3d72c6f3db342c4ab52b825f9e8df22"  
    url3 = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&exclude=daily&appid={api_key}'
    response3 = requests.get(url3)
    data3 = response3.json()

# # next 5 days
    Y=450
    for i in range(0, 40, 8):
        weather3 = data3['list'][i]['weather'][0]['description']
        temperature3 = data3['list'][i]['main']['temp']-273.15
        humidity3 = data3['list'][i]['main']['humidity']
        wind3 = data3['list'][i]['wind']['speed']
        date = datetime.fromtimestamp(data3['list'][i]['dt']).strftime('%Y-%m-%d')
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        datefv=date_obj.strftime('%A %d %B')
        icon_id= data3['list'][i]['weather'][0]["icon"]
        d={"Date": datefv, "Temperature": temperature3, "Humidity": humidity3, "WindSpeed": wind3,"icon":icon_id}
        line0=ttk.Label(frame2,text="________________________________________________________________________________________________________________________________________________________", foreground="black")
        line0.place(x=40,y=Y)
        date0=ttk.Label(frame2, text=f"{d['Date']}", foreground="black", font=("Helvetica", 12,"bold"))
        date0.place(x=30,y=Y+60)   
        icon_url1 = f"https://openweathermap.org/img/wn/{d["icon"]}@2x.png"
        image1 = Image.open(requests.get(icon_url1, stream=True).raw)
        resized_image1 = image1.resize((90, 90), Image.LANCZOS)
        icon1 = ImageTk.PhotoImage(resized_image1)
        icon_label1=ttk.Label(frame2,image=icon1 )
        icon_label1.place(x=300,y=Y+30)
        icon_label1.image = icon1       
        temp0_d=ttk.Label(frame2,text=f"{d['Temperature']:.2f}°", foreground="black", font=("Helvetica", 16) )
        temp0_d.place(x=500,y=Y+40)
        temp0=ttk.Label(frame2,text="Temperature", foreground="black" )
        temp0.place(x=500,y=Y+77)
        wind0_d=ttk.Label(frame2,text=f"{d['WindSpeed']}mph", foreground="black", font=("Helvetica", 16) )
        wind0_d.place(x=700,y=Y+40)
        wind0=ttk.Label(frame2, text="wind", foreground="black")
        wind0.place(x=700,y=Y+77)
        hum0_d=ttk.Label(frame2,text=f"{d['Humidity']}%", foreground="black", font=("Helvetica", 16) )
        hum0_d.place(x=900,y=Y+40)
        hum0=ttk.Label(frame2, text="humidity", foreground="black")
        hum0.place(x=900,y=Y+77)
        Y+=100       


    return current_temp,humidity,wind_speed,sunrise,sunset,current_date,h,current_time,city_name,description,country
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    current_temp,humidity,wind_speed,sunrise,h,sunset,current_date,current_time,city_name,description,country=result
    



for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky='nsew')

# First frame content
image_path = 'C:/Users/AdMin/OneDrive/Desktop/Nouveau dossier/cloudy_1.png'
image = Image.open(image_path)
resized_image = image.resize((300, 300), Image.LANCZOS)
photo1 = ImageTk.PhotoImage(resized_image)

image_label1 = ttk.Label(frame1, image=photo1, width="10")
image_label1.pack(side='top', pady=20, anchor="center")

label1 = ttk.Label(frame1, text="Climate is what we expect, weather is what we get.", font=("Helvetica", 15, "italic"), foreground="black")
label1.pack(pady=10, anchor="center")

label2 = ttk.Label(frame1, text="Discover the weather in your City", font=("Inconsolata", 40), foreground="black")
label2.pack(pady=50, anchor="center")

entry_frame = ttk.Frame(frame1, style="TFrame")
entry_frame.pack(pady=30, anchor="center")

city_entry = ttk.Entry(entry_frame, font="Helvetica, 18", style="TEntry")
city_entry.pack(padx=10, side="left")

search_button = ttk.Button(entry_frame, text="search", bootstyle="warning", command=lambda:(show_frame(frame2),search()))
search_button.pack(padx=10, side="right")

# Second frame content

location_label = ttk.Label(frame2,  font=("Helvetica", 25, "bold"), foreground="black")
location_label.place(x=49, y=0)


date_label = ttk.Label(frame2, font=("Helvetica", 15, "italic"), foreground="black")
date_label.place(x=49, y=60)

#

icon_label = ttk.Label(frame2, width="10")
icon_label.place(x=25, y=120)

temperature_label = ttk.Label(frame2, font=("Helvetica", 30), foreground="black")
temperature_label.place(x=250, y=180)

description_label = ttk.Label(frame2, font=("Helvetica", 15), foreground="black")
description_label.place(x=290, y=250)

high_d=ttk.Label(frame2,foreground="black", font=("Helvetica", 15))
high_d.place(x=600,y=160)
high=ttk.Label(frame2, text="feels like", foreground="black")
high.place(x=610,y=210)

wind_d=ttk.Label(frame2, foreground="black", font=("Helvetica", 15))
wind_d.place(x=750,y=160)
wind=ttk.Label(frame2, text="Wind", foreground="black")
wind.place(x=760,y=210)

sunrise_d=ttk.Label(frame2, foreground="black", font=("Helvetica", 15))
sunrise_d.place(x=950,y=160)
sunrise=ttk.Label(frame2, text="Sunrise", foreground="black")
sunrise.place(x=960,y=210)

low_d=ttk.Label(frame2, foreground="black", font=("Helvetica", 15))
low_d.place(x=600,y=260)
low=ttk.Label(frame2, text="pressure", foreground="black")
low.place(x=610,y=310)

humidity_d=ttk.Label(frame2, foreground="black", font=("Helvetica", 15))
humidity_d.place(x=750,y=260)
humidity=ttk.Label(frame2, text="Humidity", foreground="black")
humidity.place(x=760, y=310)

sunset_d=ttk.Label(frame2, foreground="black", font=("Helvetica", 15))
sunset_d.place(x=950, y=260)
sunset=ttk.Label(frame2, text="sunset", foreground="black")
sunset.place(x=960,y=310)

label=ttk.Label(frame2, text="Next 5 days " , foreground="black", font=("Helvetica", 20, "italic") )
label.place(x=77,y=400)

# ****************************************************************************************************************************
Y=100
for i in range(0,100):
    l=tk.Label(frame2,text="*",foreground="black",width=3)
    l.place(x=1100,y=Y)
    Y+=20

label=ttk.Label(frame2, text="Today\'s weather " , foreground="black", font=("Helvetica", 20, "italic") )
label.place(x=1240,y=50)
label=ttk.Label(frame2, text="next 8 hours " , foreground="gray", font=("Helvetica", 20, "italic") )
label.place(x=1550,y=50)


# Show the first frame
show_frame(frame1)

root.mainloop()