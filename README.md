# F.R.I
### Facial Recogniton and Identification


A Flask based project to identifying faces in a video after uploading a face photo of the person.
This uses [face_recognition](https://github.com/ageitgey/face_recognition "face_recognition") API to detect faces.

# Installation
##### To install it in Windows:
One need to install visual studio 2017 for installing dlib. otherwise, it will not work.

##### Installing on Mac or Linux
First, make sure you have dlib already installed with Python bindings:

[How to install dlib from source on macOS or Ubuntu](https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf "How to install dlib from source on macOS or Ubuntu")
Then, install this module from pypi using pip3 (or pip2 for Python 2):

`pip3 install face_recognition`

## Install the requirements
`pip3 install -r requirements.txt`

**Note: One need to set your own face upload directory through final.py**
