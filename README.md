# Deportes

## Requirements and to run on local:
To run this project locally, follow the steps below:

### Clone repository:

Clone this repository to your local machine using the following command:

git clone <repository-url>

### Python:

Ensure that Python is installed on your system. You can check the Python version by running the following command:

py -m django --version

If Python is not installed, download and install it from the official Python website.

### Install Django:

Use pip to install Django. Run the following command:

py -m pip install Django

### Run the Server:

Navigate to the project directory where the manage.py file is located and run the following command to start the Django development server:

py manage.py runserver

### Open in Browser:

Once the server is running, open your web browser and navigate to http://127.0.0.1:8000/ by clicking or using Ctrl + click.

## Imports

To male an import, you need to install django extensions

pip install django-extensions

Then you have to run the command (inside the project directory)

py manage.py runscript smartscore.import

## When changings database

Always makemigration and migrate 

py manage.py makemigrations
py manage.py migrate

## For testing

pip install pytest

python -m pytest


