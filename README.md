# flask-todo-api

My take on learning some Python and Flask.

## Prerequisites

* Python 3
* [Virtualenv](http://sourabhbajaj.com/mac-setup/Python/virtualenv.html)

## Installation

```sh
git clone git@github.com:vaaralav/flask-todo-api.git
cd flask-todo-api
virtualenv .venv # Create Virtualenv
source .venv/bin/activate # Use the virtualenv
pip install -r requirements.txt # Install the dependencies
```

## Running the thing

```sh
python app.py
```

## Lint

To get somewhat readable linter output run the command below.

```sh
pylint --rcfile=pylintrc --output-format=colorized *.py
```
