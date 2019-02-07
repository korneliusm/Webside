import usocket as socket
from machine import Pin, I2C
import time
import BME280
i2c = I2C(scl=Pin(22),sda=Pin(21), freq=10000)
bme = BME280.BME280(i2c=i2c)
CSS= """
 <style>
               
                h1 { background-color: #400085;
                 }
                 body { background-image: url("https://cdn.allwallpaper.in/wallpapers/1920x1080/11440/winter-forest-hills-skies-1920x1080-wallpaper.jpg");
                background-repeat: no-repeat;
                background-attachment: fixed;
                background-position: center;
                }
                body {
                 padding: 20px;
                 margin: auto;
                 width: 80%;
                 text-align: center;
                 style="font-family:courier;"
                }
                .progress { }
                .progress.vertical {
                 position: relative;
                 width: 10%;
                 height: 50%;
                 display: inline-block;
                 margin: 20px;
                }
                .progress.vertical > .progress-bar {
                 width: 100% !important;
                 position: absolute;bottom: 0;
                }
                .progress-bar { background: linear-gradient(to top, brown 0%, blue 100%); }
                .progress-bar-pres { background: linear-gradient(to top, pink 0%, crimson 100%); }
                .progress-bar-hum { background: linear-gradient(to top, #B95200 0%, #7B80EE 100%); }
                .progress-bar-temp { background: linear-gradient(to top, #3EC2D4 0%, #FF0000 100%); }
                p {
                 position: absolute;
                 font-size: 1.5rem;
                 top: 50%;
                 left: 50%;
                 transform: translate(-50%, -50%);
                 z-index: 5;
                }
            </style>
"""
def index(temperature, humidity, pressure):
    header = 'HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    html = """
        <html>
            <head>
             """ + CSS + """
             <meta http-equiv="refresh" content="15">
             <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>
            <body>
             <button onclick=location=URL>Refresh</button>
             <h1>BME280 Målinger </h1>
             <div class="progress vertical">
              <p>"""+str(temperature)+"""C<p>
              <div role="progressbar" style="height: """+str(temperature)+"""%;" class="progress-bar progress-bar-temp"></div>
             </div>
              <div class="progress vertical">
              <p>"""+str(humidity)+"""% Fukt</p>
              <div role="progressbar" style="height: """+str(humidity)+"""%;" class="progress-bar progress-bar-hum"></div>
             </div>
              <div class="progress vertical">
              <p>"""+str(pressure)+"""kPa<p>
              <div role="progressbar" style="height: """+str(float(pressure)/100)+"""%;" class="progress-bar progress-bar-pres"></div>
             </div>  
            </body>
         </html>
"""
    return header + html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  temp = bme.temperature[0:-1] 
  pres = bme.pressure[0:-4]
  hum = bme.humidity[0:-1]
  #temp_percentage = (temp+6)/(40+6)*(100)

  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)

  response = index(temp, hum, pres)
  conn.send(response)
  conn.close()