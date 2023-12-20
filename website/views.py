"""Stores the standard routes for the website."""

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from .models import Gallery
from . import db
import json
import os

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required # the user must be logged in to access this route
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short.', category='error')
        else:
            # add the note to the database
            new_note = Note(data=note, date=None, user_id=current_user.id) # note here represents the form in the html document
            db.session.add(new_note)
            db.session.commit()
            flash('Note added.', category='success') # user feedback after note is added
            
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    """Deletes a note."""
    note = json.loads(request.data) # loads() converts a string to a dictionary
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/art')
def art():
    """Displays the art gallery."""
    # code that checks the folder website/static/gallery for folders, each folder is for an art piece that contains a file main.jpg and metadata.json
    # the code should walk through the directory and save the path to the image and the metadata to the gallery database
    # the code should then display the images and metadata in the art.html template

    # get the path to the gallery folder
    gallery_path = os.path.join(os.getcwd(), 'website', 'static', 'gallery')
    # get the folders in the gallery folder
    folders = os.listdir(gallery_path)
    tuple_list = []
    # loop through the folders
    for folder in folders:
        # get the path to the folder
        folder_path = os.path.join(gallery_path, folder)
        # get the files in the folder
        files = os.listdir(folder_path)
        # loop through the files
        for file in files:
            # check if the file is the main image
            if file == 'main.jpg':
                # get the path to the main image
                main_image_path = os.path.join(folder_path, file)
                relative_main_image_path = os.path.join('static', 'gallery', folder, file) # the relative path is used to display the image in the html document
            # check if the file is the metadata
            elif file == 'metadata.json':
                # get the path to the metadata
                metadata_path = os.path.join(folder_path, file)
        # get the metadata from the metadata file
        with open(metadata_path) as metadata_file:
            # load the metadata
            metadata = json.load(metadata_file)
            # print(metadata)

        # Retrieve metadata values with error handling
        title = metadata.get('title', 'No title available')  # Default value if 'title' is missing
        # print(title)
        description = metadata.get('description', 'No description available')  # Default value if 'description' is missing

        main_image_dimensions_width = metadata['main_image_dimensions']['width']  # Get the dimensions of the main image
        main_image_dimensions_height = metadata['main_image_dimensions']['height']

        # adjust the dimensions of the main image to be a maximum of 500 pixels wide or 500 pixels tall and scale accordingly
        if main_image_dimensions_width > main_image_dimensions_height:
            main_image_dimensions_height = int(500 * (main_image_dimensions_height / main_image_dimensions_width))
            main_image_dimensions_width = 500
        else:
            main_image_dimensions_width = int(500 * (main_image_dimensions_width / main_image_dimensions_height))
            main_image_dimensions_height = 500

        # Check if 'price' exists and is an integer
        if 'price' in metadata and isinstance(metadata['price'], int):
            price = metadata['price']
        else:
            price = 0  # Default value if 'price' is missing or not an integer

        medium = metadata.get('medium', 'No medium given')  # Default value if 'medium' is missing
        size = metadata.get('size', 'No size given')  # Default value if 'size' is missing

        metadata = {
            "title": title,
            "description": description,
            "price": price,
            "main_image_path": relative_main_image_path,
            "main_image_dimensions_width": main_image_dimensions_width,
            "main_image_dimensions_height": main_image_dimensions_height,
            "medium": medium,
            "size": size
        }
        tuple_list.append(metadata)

        # add the art piece to the database
        # new_art_piece = Gallery(title=title, description=description, price=price, main_image_path=main_image_path, medium=medium, size=size)
        # db.session.add(new_art_piece)
        # db.session.commit()

    return render_template("art.html", user=current_user, gallery=tuple_list)