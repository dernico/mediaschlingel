mediaschlingel
==============

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