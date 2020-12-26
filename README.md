# sprinkler-pi
raspberry pi controller garden sprinkler


<img src="IMG_6853.jpg" width="200">
<img src="IMG_6857.jpg" width="200">
<img src="valve.jpg" width="200">
<img src="IMG_6854.jpg" width="200">

sudo apt-get install python3-pip<BR>
sudo pip3 install RPi.GPIO<BR>
sudo pip3 install flask<BR>
sudo pip3 install flask-socketio<BR>

python3 app.py<BR>
http://<raspi ip>:5000<BR>


START AS SERVICE<BR>
sudo vi /etc/systemd/system/sprinkler.service<BR>
[Unit]<BR>
Description=sprinkler<BR>
After=network-online.target<BR>
[Service]<BR>
ExecStart=/home/pi/sprinkler-pi/app.py<BR>
[Install]<BR>
WantedBy=multi-user.target<BR>

add shebang to app.py  (#!/usr/bin/python3)<BR>
chmod +x ~/sprinkler-pi/app.py<BR>
