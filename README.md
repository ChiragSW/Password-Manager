# Password Manager

A secure and user-friendly web application designed to manage your passwords efficiently. The Password Manager ensures your sensitive information is safe, organized, and easily accessible.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/password-manager.git
   cd password-manager
   ```

2. Run the application:
   ```bash
   flask run
   ```

3. Open your browser and visit:
   ```
   http://127.0.0.1:5000/
   ```

## Folder Structure

```
password-manager/
├── static/       # CSS, JavaScript, and image files
├── templates/    # HTML files
├── app.py        # Main Flask application
├── requirements.txt  # List of dependencies
├── README.md     # Project documentation
└── database.db   # SQLite database (auto-generated)
```

(Features)

        - **Secure Storage**: Your passwords are stored securely in an SQLite database.
        - **Master Password Protection**: Access your passwords with a single master password.
        - **Add, View, and Delete Passwords**: Easily manage your passwords through a user-friendly interface.
        - **Responsive Design**: The application is responsive and works well on various devices.

(Tech Used)

        - Web Framework: Flask
        - Database Management: SQLite
        - Frontend: HTML, CSS, Bootstrap
        - Backend: Python (3.7)
        - Interactive UI: JavaScript
