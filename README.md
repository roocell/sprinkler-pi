# sprinkler-pi
raspberry pi controller garden sprinkler
I also use this project to control my fireplace with a simple relay.
But I've hooked up IFTTT to my raspi webserver so I can ask alexa to 
turn on my fireplace.


<img src="IMG_6853.jpg" width="200">
<img src="IMG_6857.jpg" width="200">
<img src="valve.jpg" width="200">
<img src="IMG_6854.jpg" width="200">

sudo apt-get install python3-pip<BR>
sudo pip3 install RPi.GPIO<BR>
sudo pip3 install flask<BR>
sudo pip3 install flask-socketio<BR>
sudo pip3 install eventlet<BR>

python3 app.py<BR>
http://<raspi ip>:5001<BR>


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

sudo systemctl daemon-reload<BR>
sudo systemctl enable sprinkler<BR>
sudo systemctl restart sprinkler<BR>
sudo systemctl status sprinkler.service<BR>

# alexa and pi
python3 -m pip install Flask-Ask<BR>
pip3 install --upgrade setuptools<BR>
pip3 install 'cryptography<2.2'<BR>
pip3 install werkzeug==0.16.0<BR>

# setup HTTPS
we need to run https in order for amazon's alexa skills to talk to the pi.
We will be portforwarding using our domain - so we can use real certs rather than self-signed ones.
Should be able to just copy the certs from our domain server and use them on the pizero.

but here is an article explaining how to generate self signed certs
https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https

#ngrok
An alternative is to use ngrok.  https://dashboard.ngrok.com/get-started/setup
Instantly create a public HTTPS url for a website running locally on your development machine.
ngrok offloads TLS so you don't have to worry about your configuration.

enable port forwarding on your router so the pi is accessible from outside

# Alexa skills
using alexa skills can theoretically work, but it's far too complicated and finicky
when dealing with your skill invocation phrase and what 'slots' you want to use for
your skill.  I found that you couldn't define a desirable invocation name nor slot (on/off)
in order to have it work nicely. On top of that, getting the skill to work in canada on
my alexa devices proved troublesome.

# IFTTT
using IFTTT is much, much simpler. no ngrok. no https (if you want that)
goto ifttt.com
create a new applet
choose alexa as the 'if' and pick whatever phrase you like ("fireplace")
choose webhooks as the 'then' and have it point to your raspberry pi
once this is set up, you can simply say "alexa, trigger fireplace"
