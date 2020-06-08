import os
from flask import Flask
from flask import Flask, render_template,Response,request ,make_response, session, flash, redirect
from werkzeug.utils import secure_filename
import numpy as np
import urllib.request
import face_recognition
import cv2
import time
from uuid import uuid4

UPLOAD_FOLDER ='C:/Users/user/Desktop/FRI/FRI/faces'
app = Flask(__name__,static_folder = "templates")
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
knownFaces = []
allKnownFaces = os.listdir('faces/')
for i in range(len(allKnownFaces)):
    image = face_recognition.load_image_file("faces/"+allKnownFaces[i])
    knownFaces.append(image)
print(allKnownFaces) 
known_face_encodings = []
for i in range(len(knownFaces)): 
    try:
        known_face_encodings.append(face_recognition.face_encodings(knownFaces[i])[0])    
    except IndexError:
        print(i)
        print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
        quit()

known_face_names = allKnownFaces 
for i in range(len(known_face_names)): 
    known_face_names[i] = known_face_names[i].split(".")[0] 


@app.errorhandler(404)
def error404(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error500(e):    
    return render_template('500.html'), 500

@app.errorhandler(403)
def error500(e):    
    return render_template('403.html'), 403

@app.errorhandler(410)
def error500(e):    
    return render_template('410.html'), 410

def make_unique(string):
    ident = uuid4().__str__()[:5]
    return f"{ident}-{string}"

    
def facerecognitionvideo(videoPath,videoTimeToProcess,fpsToProcess):
    start = time.time()  
    video_capture = cv2.VideoCapture(videoPath) 
    fps = video_capture.get(cv2.cv2.CAP_PROP_FPS)
    fps = np.round(fps) 
    codecformat = cv2.VideoWriter_fourcc(*'XVID')
    size = (
		int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
		int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
	)

    if fpsToProcess == "none":
        out = cv2.VideoWriter('templates/facerecognitionvideo.avi',codecformat, fps, size)
    else:
        out = cv2.VideoWriter('templates/facerecognitionvideo.avi',codecformat, 1, size)
    i = 0
    while 1:
        ret, frame = video_capture.read() 
        if ret == False:
            break		
        
        
        
        i += 1
        if fpsToProcess != "none": 
            if i%int(fps*int(fpsToProcess))!=0: 
                print(i)
                continue
            
        if videoTimeToProcess != "none":
            print("Processed", i ," frames out of ", fps*int(videoTimeToProcess)) 
            if i==int(videoTimeToProcess)*fps: 
                break

        
        rgb_frame = frame[:, :, ::-1] 
        face_locations = face_recognition.face_locations(rgb_frame) 
        

        
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings): 
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)  
            name = "Unknown"            
            
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)   
            best_match_index = np.argmin(face_distances) 
            
            if matches[best_match_index]: 
                name = known_face_names[best_match_index]

            
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1) 

            
            cv2.rectangle(frame, (left, bottom - 33), (right, bottom), (0, 0, 255), cv2.FILLED) 
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1, (255, 255, 255), 1) 
        out.write(frame)
                
    print("Time Taken:", time.time()-start) 
	
    return 0


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/copyright')
def copyright():
        return render_template('copyright.html')

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			orignal_filename = secure_filename(file.filename)
			unique_filename = make_unique(orignal_filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
			flash('File successfully uploaded')
			return redirect('/#section4')
		else:
			flash('Allowed file types are png, jpg, jpeg')
			return redirect(request.url)

@app.route('/facerecognition.html', methods = ['POST', 'GET'])
def facerecognition():
    if request.method == 'POST': 
        f = request.files['fileToUpload'] 
        result = request.form 
        videoTimeToProcess = result['videoTime'] 
        fpsToProcess = result['fps'] 
        filePath = f.filename 
        f.save(secure_filename(filePath))

         
        facerecognitionvideo(filePath,videoTimeToProcess,fpsToProcess)
        return render_template('/download.html')

    
    else:
        return render_template('/index.html')

if __name__ == "__main__":
    app.run()
    app.debug = True
    app.run()
