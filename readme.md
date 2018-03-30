# Flask Blog Engine

Flask-blog-engine is a blogging application based on the Flaskr application from the Tutorial section of the official Flask documentation. The latest version of the documentation can be found [here](http://flask.pocoo.org/docs/latest/).

The following instructions are for MacOS. See the Installation part of the Flask documentation to run the app on different operating systems.

## To set up the application:
1. Create a folder for this app or `git clone` this repository
2. If using Python 3, create a new virtual environment with `python3 -m venv venv`
3. Activate the virtual environment with `. venv/bin/activate` (Deactivate the virtual environment by entering `deactivate` in the terminal)
4. Install Flask with `pip3 install Flask`
5. Install the application by running the command `pip3 install --editable .` in the project's root directory
6. Enable testing by installing pytest with `pip3 install pytest`

## To run the application:
1. Activate the virtual environment with `. venv/bin/activate`
2. Tell the terminal the application to work with by exporting the FLASK_APP environment variable with `export FLASK_APP=flask_blog_engine`
3. Run the app with `flask run`
4. View the app in a web browser at http://localhost:5000

## Notes
1. Enable debug mode with `export FLASK_DEBUG=1` before running the server; this will display code changes in the browser immediately when changes to a file are saved without having to relaunch the Flask app
2. The Flask server can be made externally visible with `flask run --host=0.0.0.0`
