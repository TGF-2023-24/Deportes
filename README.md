# 🏅 Sports Statistics Analysis Platform

## Project Description

This project is a comprehensive platform designed to manage and analyze sports statistics, with a specific focus on football. Using advanced algorithms and data visualization tools, the platform enables clubs to make strategic decisions, such as player evaluation and long-term squad planning. The platform also helps identify young talent through algorithmic analysis to discover future football stars.

## Key Features

- **Player Analysis**: In-depth evaluation of player characteristics and performance using adaptive algorithms.
- **Squad Builder**: Create, analyze, and optimize football squads by replacing underperforming players.
- **Transfer Recommendations**: Algorithm-driven suggestions for players that fit the club's strategic vision, focusing on both short-term success and long-term planning.
- **Advanced Statistics**: Provides detailed, data-driven insights to assist in team-building decisions and recruitment strategies.

## Technologies Used

- **Frontend**:
  - ![HTML5](https://img.shields.io/badge/-HTML5-E34F26?style=flat&logo=html5&logoColor=fff)
  - ![CSS3](https://img.shields.io/badge/-CSS3-1572B6?style=flat&logo=css3)
  - ![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=000)
  - ![Bootstrap](https://img.shields.io/badge/-Bootstrap-563D7C?style=flat&logo=bootstrap&logoColor=fff)

- **Backend**:
  - ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=fff)
  - ![Django](https://img.shields.io/badge/-Django-092E20?style=flat&logo=django&logoColor=fff)

## Project Structure

1. **Frontend**: User interface that allows clubs to interact with the platform's features like player analysis and squad building.
2. **Backend**: Business logic that supports data-driven decision-making processes.
3. **Database**: Relational database that stores player data, team configurations, and performance metrics.

## How to Run Locally

### Clone the Repository
Clone this repository to your local machine:

  ```bash
  git clone https://github.com/TGF-2023-24/Deportes.git 
```
### Python:

Ensure that Python is installed on your system. You can check the Python version by running the following command:

    ```bash
    py -m django --version

If Python is not installed, download and install it from the official Python website.

### Install Django:

Use pip to install Django. Run the following command:

```bash
py -m pip install Django
```

### Run the Server:

Navigate to the project directory where the manage.py file is located and run the following command to start the Django development server:

```bash
py manage.py runserver
```

### Open in Browser:

Once the server is running, open your web browser and navigate to http://127.0.0.1:8000/ by clicking or using Ctrl + click.

## Imports

To make an import, you need to install django extensions

```bash
pip install django-extensions
```

Then you have to run the command (inside the project directory)

```bash
py manage.py runscript smartscore.import
```

## When changings database

Always makemigration and migrate 

```bash
py manage.py makemigrations
py manage.py migrate
```

## For testing

```bash
pip install pytest
```

python -m pytest

## Collaborators
This project was developed by Iván Gallego Cuervo and Pablo Moreno Canduela.

