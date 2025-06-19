from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from .models import db, User
import cv2
import face_recognition as Recognition
import numpy as np
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        image = request.files['face_image']
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Nom d’utilisateur déjà pris.')
            return redirect(url_for('main.register'))
        
        # Sauvegarder l'image faciale
        image_path = os.path.join('app/static/known_faces', f"{username}.jpg")
        image.save(image_path)
        
        # Créer l'utilisateur
        new_user = User(username=username, face_image_path=image_path)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Inscription réussie. Veuillez vous connecter.')
        return redirect(url_for('main.login'))
    
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('main.two_factor'))
        else:
            flash('Nom d’utilisateur ou mot de passe incorrect.')
    
    return render_template('login.html')

@bp.route('/2fa', methods=['GET', 'POST'])
def two_factor():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        if 'face_image' not in request.files or request.files['face_image'].filename == '':
            flash('Aucune image fournie. Veuillez capturer une image.')
            return render_template('2fa.html')
        
        image_file = request.files['face_image']
        temp_image_path = os.path.join('app/static/images', 'temp.jpg')
        image_file.save(temp_image_path)
        
        # Charger l'image de référence
        known_image = Recognition.load_image_file(user.face_image_path)
        known_encodings = Recognition.face_encodings(known_image)
        if not known_encodings:
            flash('Erreur : Aucun visage détecté dans l’image de référence.')
            os.remove(temp_image_path)
            return render_template('2fa.html')
        known_encoding = known_encodings[0]
        
        # Charger l'image capturée
        unknown_image = Recognition.load_image_file(temp_image_path)
        unknown_encodings = Recognition.face_encodings(unknown_image)
        
        if unknown_encodings:
            results = Recognition.compare_faces([known_encoding], unknown_encodings[0])
            if results[0]:
                flash('Authentification réussie !')
                return redirect(url_for('main.dashboard'))
            else:
                flash('Échec de la reconnaissance faciale.')
        else:
            flash('Aucun visage détecté dans l’image capturée.')
        
        os.remove(temp_image_path)
        return render_template('2fa.html')
    
    return render_template('2fa.html')

@bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', current_user=user)

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Vous êtes déconnecté.')
    return redirect(url_for('main.login'))