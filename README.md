HIVE Application (HTML Version)
1. Overview
HIVE is a robust, web-based productivity and communication platform developed using Flask, a lightweight Python web framework. Designed for individuals, teams, and communities, HIVE offers a centralized hub where users can register, log in, and access a feature-rich dashboard. The platform enables users to manage personal notes, upload and share files, engage in real-time chats with other users, and view received messages—all within a visually engaging, modern interface. HIVE leverages animated gradient text, dynamic video backgrounds, and a responsive design powered by Tailwind CSS and Bootstrap, ensuring an immersive user experience.

This repository contains the HTML-based version of HIVE, featuring a full web interface with HTML templates, Tailwind CSS, Bootstrap, and Socket.IO for real-time chat functionality.

2. Purpose
HIVE’s primary goal is to provide an all-in-one solution for productivity and collaboration. It integrates note-taking, file sharing, and real-time communication to help users organize tasks, share resources, and connect efficiently. Whether for personal use, remote teams, or community engagement, HIVE offers a user-friendly web interface to foster productivity and interaction.

3. Key Features
HIVE offers the following features in its HTML version:

a. User Authentication and Security

Users can register with a unique username and password, log in, and securely log out.
Authentication is managed using Flask-Login and Flask-WTF, with data stored in a SQLite database (users.db).
Passwords are stored in plain text (recommend hashing for production use).
b. Dashboard Experience

A central dashboard (dashboard.html) displays a welcome message, notes, files, chat, and messages with a visually striking design (animated gradients, video backgrounds).
Features real-time updates for messages using Socket.IO.
c. Notes Management

Users can create, edit, and delete personal notes directly from the dashboard.
Managed through dashboard.html, edit_note.html, and Flask routes.
d. File Sharing and Management

Users can upload, view, and delete files (stored in the uploads directory).
Accessible via forms and links in dashboard.html.
e. Real-Time Chat System

A chat interface (chat.html) allows users to send and receive messages in real time using Socket.IO.
Users select recipients from a dropdown and receive instant updates.
f. Messages Management

Users can view received messages in the dashboard or via view_messages.html, with sender details and timestamps.
Updated in real time via Socket.IO.
g. Visual and Interactive Design

Features a modern, dark-themed UI with Tailwind CSS for most templates and Bootstrap for edit_note.html, register.html, and view_messages.html.
Includes animated gradient text and video backgrounds for an engaging experience.
4. Installation and Running
4.1. Prerequisites
a. Python 3.x installed on your system.
b. Basic knowledge of Python, Flask, and web development.

4.2. Steps
a. Clone the Repository:

git clone https://github.com/srujan-zenshastra/Week1-Main-Project.git
cd Week1-Main-Project b. Install Dependencies:
Use pip to install the required packages: pip install flask flask-sqlalchemy flask-wtf flask-socketio werkzeug c. Set Up the Database:
Ensure users.db is in the instance folder (or run the app once to create it): python app.py d. Run the Application:
Execute app.py to start the Flask server: python app.py The app will run on http://0.0.0.0:8000 in debug mode. e. Access the App:
Open a web browser and navigate to http://0.0.0.0:8000 (or localhost:8000).
5. Usage
5.1. Getting Started
a. Register: Visit index.html or register.html to create an account with a username and password.
b. Log In: Use login.html to enter credentials and access the dashboard.
c. Explore the Dashboard: Use the dashboard to manage notes, upload files, chat with others, and view messages.

5.2. Using Features
a. Notes: Click the note form to add a new note, "Edit" to modify, or "Delete" to remove a note.
b. Files: Use the upload form to add files, click links to view, or use the "Delete" button to remove files.
c. Chat: Navigate to "Chat" to send messages to other users in real time, selecting recipients from the dropdown.
d. Messages: View received messages in the dashboard or view_messages.html for a detailed list.

6. Libraries and Modules Used
The HIVE application relies on several Python libraries and modules. Below is a detailed explanation of each:

a. Flask

Description: Flask is a micro web framework written in Python, designed to be lightweight and flexible, allowing developers to build web applications quickly with minimal dependencies.
Why Used: Flask is the core framework, providing routing, request handling, and session management for HTML templates and real-time features.
b. Flask-SQLAlchemy

Description: Flask-SQLAlchemy integrates SQLAlchemy, a powerful SQL toolkit and Object-Relational Mapping (ORM) library, for seamless database interaction.
Why Used: Manages the SQLite database (users.db) to store user data, notes, and messages, simplifying CRUD operations.
c. Flask-WTF

Description: Flask-WTF integrates WTForms for flexible forms validation and rendering, with CSRF protection.
Why Used: Creates and validates forms like RegisterForm, LoginForm, NoteForm, and UploadForm for user input in the web interface.
d. Flask-SocketIO

Description: Flask-SocketIO integrates Socket.IO for real-time, bidirectional communication between web clients and servers using WebSockets.
Why Used: Enables real-time chat functionality, handling message sending and receiving instantly via chat.html.
e. Werkzeug

Description: Werkzeug is a WSGI utility library for Python, providing tools for request/response handling, URL routing, and security features.
Why Used: Sanitizes filenames during file uploads with secure_filename to prevent security vulnerabilities.
f. Datetime

Description: datetime is a built-in Python module for handling dates and times, providing classes to manipulate and format date-time objects.
Why Used: Timestamps messages in the Message model, displaying when messages were sent in the UI.
g. Functools

Description: functools is a built-in Python module offering higher-order functions, such as decorators.
Why Used: Preserves function metadata in decorators like login_required (implied) for authentication logic.
h. Os

Description: os is a built-in Python module for interacting with the operating system, handling files, directories, and paths.
Why Used: Manages the uploads directory, lists files, and removes files safely for file operations.
i. Tailwind CSS

Description: Tailwind CSS is a utility-first CSS framework delivered via CDN, allowing developers to build custom designs quickly by applying low-level utility classes.
Why Used: Used in templates like index.html, login.html, dashboard.html, and chat.html to create a responsive, modern, and dark-themed UI.
j. Bootstrap

Description: Bootstrap is a popular CSS framework (delivered via CDN) that provides pre-designed components, grids, and responsive layouts for building web interfaces.
Why Used: Used in edit_note.html, register.html, and view_messages.html for clean, minimalistic, and responsive designs.
