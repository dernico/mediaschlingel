mediaschlingel
==============

mediaschlingel is a music server that plays music from local networks, 8tracks, tunein and youtube (thanks to pafy). If everythink works you can just run "python schlingel.py" in your command line. After that you can connect to server with your mobile browser/desktop browser on port 8000 (example: http://192.168.0.12:8000 if 192.168.0.12 is the ip adress from the computer the server runs on)

because there is not much spare time available some thinks might not work.

==============
How to install
=============

if pip is not installed:
sudo apt-get install python-pip

sudo apt-get install python-gst0.10 gstreamer0.10-plugins-good \
    gstreamer0.10-plugins-ugly

Install tornado

cd libs/tornado-3.2
python setup.py build
sudo python setup.py install
(or)
install latest tornado somewhere

Install mutagen

cd libs/mutagen-1.22
sudo python setup.py install
(or)
download latest mutagen somewhere

Install Pafy
cd libs/pafy
sudo python setup.py install
(or)
download latest pafy from github: https://github.com/np1/pafy

#------------------#

New Version 

install Flask
sudo pip install Flask

install Flask-OAuth
git clone git://github.com/lepture/flask-oauthlib.git