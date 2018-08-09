# dastools

## Prerequisites (macOS)

http://docs.python-guide.org/en/latest/starting/install3/osx/

https://github.com/OpenXenManager/openxenmanager/issues/107

https://www.metachris.com/2015/11/create-standalone-mac-os-x-applications-with-python-and-py2app/


brew install python
brew install gtk
brew install pygtk

# Use virtualenv to create an isolated environment
$ virtualenv --system-site-packages venv
$ . venv/bin/activate
$ pip install -r requirements.txt

# Do I have a Python 2 problem?
$ python --version
Python 2.7.10 # Referencing OSX system install
$ which python
/usr/bin/python # Yup, homebrew's would be in /usr/local/bin

# Symlink /usr/local/bin/python to python3
$ ln -s /usr/local/bin/python3 /usr/local/bin/python

$ python --version
Python 3.6.4 # Success!
# If you still see 2.7 ensure in PATH /usr/local/bin/ takes pecedence over /usr/bin/



### Install py2app

pip install -U git+https://github.com/metachris/py2app.git@master

py2applet --make-setup dastools.py

pip install --user --ignore-installed py2app

http://pygobject.readthedocs.io/en/latest/getting_started.html
brew install pygobject3 --with-python3 gtk+3

sudo pip3 install bs4

sudo easy_install -U requests

## Build for develop and testing

python setup.py py2app -A

## Build for deployment

$ rm -rf build dist
$ python setup.py py2app

## Usage

dastools is currently in beta and API stability is not guaranteed. dastools is a set of multi-purpose tools which integrates the following tools :

## AugustusTool
augustusTool can be used to convert to-and-from Base64 for any string.

## JuliusTool
JuliusTool is a useful tool for generating placeholder assets of a certain dimension. Simply launch garfieldgui on the command line as follows :
./dastools.py
You should see the below GUI. 
Enter the dimensions you want the image to be and the enter the text you want on the image and click generate image.
An image with the filename image_generated_output.png will be generated.
 
## aureliusTool
The purpose of aureliusTool is to exercise all the APIs in our backend using the GUI

## Running

## Running on Ubuntu

==> ./dastools.py


## Running on macOS

==> ./dist/dastools.app/Contents/MacOS/dastools



