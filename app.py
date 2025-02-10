from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, join_room

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FileField, SubmitField
from wtforms.validators import InputRequired, Length
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, send
from datetime import datetime
from functools import wraps

import os

app = Flask(__name__)
app.secret_key = "9cb1377d46fd86303c64cfdb1cc546d"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["UPLOAD_FOLDER"] = "uploads"

db = SQLAlchemy(app)
socketio = SocketIO(app)

# Decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Please log in to access this page", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
            return redirect(url_for("dashboard"))
    return decorated_function

# Ensure the upload folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])

    def __repr__(self):
        return f"<Message from {self.sender.username} to {self.receiver.username}>"

# Notes model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

# Registration form
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=100)])
    submit = SubmitField("Register")

# Login form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

# Note form
class NoteForm(FlaskForm):
    content = TextAreaField("New Note", validators=[InputRequired()])
    submit = SubmitField("Save Note")

# File upload form
class UploadForm(FlaskForm):
    file = FileField("Upload File", validators=[InputRequired()])
    submit = SubmitField("Upload")

@app.route("/", methods=["GET", "POST"])
def home():
    form = RegisterForm()

    if form.validate_on_submit():
        # Check if username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already exists", "danger")
        else:
            # Register the new user
            user = User(username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))  # Redirect to login page after successful registration

    return render_template("index.html", form=form)






@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
        if user:
            session["user"] = user.username
             
            return redirect(url_for("dashboard"))
        flash("Invalid username or password", "danger")
    return render_template("login.html", form=form)




@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    user = User.query.filter_by(username=session["user"]).first()
    notes = Note.query.filter_by(user_id=user.id).all()

    # Fetch all messages received by the user
    received_messages = Message.query.filter_by(receiver_id=user.id).order_by(Message.timestamp.desc()).all()

    note_form = NoteForm()
    if note_form.validate_on_submit():
        new_note = Note(user_id=user.id, content=note_form.content.data)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for("dashboard"))

    upload_form = UploadForm()
    uploaded_files = os.listdir(app.config["UPLOAD_FOLDER"])

    return render_template("dashboard.html", username=session["user"], notes=notes, note_form=note_form, 
                           upload_form=upload_form, files=uploaded_files, received_messages=received_messages)


@app.route("/delete_note/<int:note_id>")
@login_required
@handle_errors
def delete_note(note_id):
    if "user" not in session:
        return redirect(url_for("login"))

    note = Note.query.get(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/upload", methods=["POST"])
@login_required
@handle_errors
def upload():
    if "user" not in session:
        return redirect(url_for("login"))

    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        flash("File uploaded successfully!", "success")
    return redirect(url_for("dashboard"))

@app.route("/uploads/<filename>")
@login_required
@handle_errors
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/delete_file/<filename>", methods=["POST"])
@login_required
@handle_errors
def delete_file(filename):
    if "user" not in session:
        return redirect(url_for("login"))

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    
    if os.path.exists(file_path):
        os.remove(file_path)
        flash("File deleted successfully!", "success")
    else:
        flash("File not found!", "danger")

    return redirect(url_for("dashboard"))


@app.route("/edit_note/<int:note_id>", methods=["GET", "POST"])
@login_required
@handle_errors
def edit_note(note_id):
    if "user" not in session:
        return redirect(url_for("login"))

    user = User.query.filter_by(username=session["user"]).first()
    note = Note.query.get(note_id)

    # Check if the note belongs to the logged-in user
    if note.user_id != user.id:
        flash("You are not authorized to edit this note", "danger")
        return redirect(url_for("dashboard"))

    form = NoteForm()
    if form.validate_on_submit():
        note.content = form.content.data
        db.session.commit()
        flash("Note updated successfully!", "success")
        return redirect(url_for("dashboard"))

    # Pre-fill form with existing note content
    form.content.data = note.content
    return render_template("edit_note.html", form=form, note=note)

@app.route("/chat")
@login_required
@handle_errors
def chat():
    if "user" not in session:
        return redirect(url_for("login"))

    user = User.query.filter_by(username=session["user"]).first()
    users = User.query.all()  # Get all users for the chat system

    return render_template("chat.html", users=users, user=user)

@app.route("/send_message", methods=["POST"])
@login_required
@handle_errors
def send_message():
    if "user" not in session:
        return redirect(url_for("login"))

    sender = User.query.filter_by(username=session["user"]).first()
    receiver_username = request.form.get("receiver")
    receiver = User.query.filter_by(username=receiver_username).first()

    message_content = request.form.get("message")

    if receiver:
        new_message = Message(sender_id=sender.id, receiver_id=receiver.id, content=message_content)
        db.session.add(new_message)
        db.session.commit()
        flash("Message sent successfully!", "success")
    else:
        flash("User not found", "danger")

    return redirect(url_for("chat"))

@app.route("/view_messages")
@login_required
@handle_errors
def view_messages():
    if "user" not in session:
        return redirect(url_for("login"))

    user = User.query.filter_by(username=session["user"]).first()
    # Retrieve messages where the logged-in user is the receiver
    messages = Message.query.filter_by(receiver_id=user.id).all()

    return render_template("view_messages.html", messages=messages)

@socketio.on("send_message")
def handle_send_message(data):
    if "user" not in session:
        return

    sender = User.query.filter_by(username=session["user"]).first()
    receiver = User.query.filter_by(username=data["receiver"]).first()

    if sender and receiver:
        # Store message in database
        new_message = Message(sender_id=sender.id, receiver_id=receiver.id, content=data["content"])
        db.session.add(new_message)
        db.session.commit()

        # Emit only to the receiver's room
        socketio.emit("receive_message", {
            "sender": sender.username,
            "content": data["content"],
            "timestamp": new_message.timestamp.strftime("%H:%M:%S")
        }, room=data["receiver"])


@socketio.on("connect")
def handle_connect():
    if "user" in session:
        join_room(session["user"])  # Join room with username as room ID



@app.route("/logout")
@login_required
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)