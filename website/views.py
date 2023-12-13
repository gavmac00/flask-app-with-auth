"""Stores the standard routes for the website."""

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

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