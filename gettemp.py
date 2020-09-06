import RPi.GPIO as GPIO
import dht11
import time
import datetime
import sqlite3
import math
from bokeh.plotting import figure, output_file, show

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# read data using pin 14
instance = dht11.DHT11(pin=14)

# dbconnect
conn = sqlite3.connect('/home/pi/DHT11_Python/temp.db')
c = conn.cursor()
#c.execute('''CREATE TABLE temp(date text, temp real)''')
#conn.commit()
while True:
    result = instance.read()
    if result.is_valid():
        now_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
        c.execute(f"INSERT INTO temp VALUES ('{now_time}', {round(result.temperature, 1)})")
        conn.commit()
        GPIO.cleanup()
        break

c.execute('SELECT date FROM temp order by date desc limit 288')
x = [(x[0]) for x in c.fetchall()]
c.execute('SELECT temp FROM temp order by date asc')
y = [(y[0]) for y in c.fetchall()]
conn.close()
x.reverse()
output_file("/home/pi/DHT11_Python/index.html")
p = figure(title="Temp data", sizing_mode='stretch_both', plot_height=1500, x_axis_label='x', y_axis_label='y', x_range=x)
p.line(x, y, legend_label="Temp.", line_width=2)
p.xaxis.major_label_orientation = "vertical"
show(p)
