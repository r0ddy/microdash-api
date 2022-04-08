from microdash.wsgi import application

# Google App Engine looks for main.py at root directory
# for a WSGI-compatible object called app.
# Can also configure entrypoint via app.yaml
# entrypoint: gunicorn -b :$PORT microdash.wsgi
app = application