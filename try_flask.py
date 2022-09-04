import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from google.cloud import vision
from google.cloud.vision_v1 import types
import cv2 
import pandas as pd
from web import web_stuff
from loc import localize_objects,find_prop

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		#print(os.path.join('flask/static/uploads', filename)
		file.save(os.path.join('flask/static/uploads', filename))
		#print(os.path.join('flask/static/uploads', filename)
		#print('upload_image filename: ' + filename)
		path_photo = 'flask/static/uploads/' + filename

		l_label,df_web,my_confidence,annotations = web_stuff(path_photo)
		objects = localize_objects(path_photo)
		image,df_location = find_prop(path_photo,objects)
		os.chdir('flask/static/uploads/')
		Objects_Located_filename = "Objects_Located_"+ filename
		cv2.imwrite(Objects_Located_filename, image)

		if (my_confidence > 8): #WWW has images similar or exactly the same (best guess is reliable)
			print("Extremely confident in Best Guess")
			print("It is a {}".format(l_label[0]))
			return render_template('Result.html', filename=filename,Message = "It is a {}".format(l_label[0]),Objects_Located_filename=Objects_Located_filename)
			#further web scraping beautiful soop?
			
		elif (len(df_web) == 0 and len(df_location) == 0): #neither the web search nor the obj locater worked
			print("No good guesses from the web and object localizer")
			print("Reverting back to best guess: {}".format(l_label[0]))
			return render_template('Result.html', filename=filename,Message = "Reverting back to best guess: {}".format(l_label[0]),Objects_Located_filename=Objects_Located_filename)
		else:
			if (len(df_web) > 0 and (df_web.Score[0] >= 0.99)): #unlikely scenario, it knows its one source forsure but cant find other
				#sources to back it up
				print("Certain that its online-based")
				print("Likely its: {}".format(l_label[0]))
				return render_template('Result.html', filename=filename,Message = "Likely its: {}".format(l_label[0]),Objects_Located_filename=Objects_Located_filename)
				
			elif (len(df_location) > 0): #Can't find anything online. Revert t object locater + analysis
				print("Certain that its user-made")
				print("Topic includes:")
				for i in df_location.Label:
					print('\t{}'.format(i))
				return render_template('Result.html', filename=filename,Message = "Certain that its user-made",Objects_Located_filename=Objects_Located_filename)
			else:
				print("Could be user-made or online but I really have no good guesses")
				print("Using Object Localiser")
				return render_template('Result.html', filename=filename,Objects_Located_filename=Objects_Located_filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(port=8080)