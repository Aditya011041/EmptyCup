# wsgi.py
from your_flask_app import create_app

app = create_app()

if __name__ == '__main__':
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=True)