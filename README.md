# qolos

Implemented following [Flask's tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/).

## Setup

Activate the virtual environment:

```
source .venv/Scripts/activate
```

Deactivate it:

```
deactivate
```

Set Flask environment variables:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
```

Initialize the database:

```
flask init-db
```

Run the application:

```
flask run --host=0.0.0.0
```

Install the project in editable mode:

```
pip install -e .
```