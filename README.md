# flask-todo-api

My take on learning some Python and Flask.

<!-- TOC depthFrom:2 depthTo:3 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the thing](#running-the-thing)
- [Lint](#lint)
- [API](#api)
	- [`GET /todo/api/tasks`](#get-todoapitasks)
	- [`POST /todo/api/tasks`](#post-todoapitasks)
	- [`GET /todo/api/tasks/:task_id`](#get-todoapitaskstaskid)
	- [`PUT /todo/api/tasks/:task_id`](#put-todoapitaskstaskid)
	- [`DELETE /todo/api/tasks/:task_id`](#delete-todoapitaskstaskid)
	- [`GET /todo/api/health`](#get-todoapihealth)

<!-- /TOC -->

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

## API

### `GET /todo/api/tasks`

Lists tasks. By default doesn't filter tasks.

#### Filters

Tasks can be filtered using query string and the following Filters

* `done` _0 or 1_: Get only done (1) or undone (0) tasks.

#### Example

##### Request

```http
GET /todo/api/tasks?done=0 HTTP/1.1
Host: localhost:5000
Content-Type: application/json
Authorization: Basic <your_basic_authentication_token_here>
```

##### Response: 200 OK

```json
[
  {
    "description": "Flask especially",
    "done": false,
    "id": 2,
    "title": "Learn Python",
    "uri": "http://localhost:5000/todo/api/tasks/2"
  },
  {
    "description": "Such wow",
    "done": false,
    "id": 3,
    "title": "Learn Python",
    "uri": "http://localhost:5000/todo/api/tasks/3"
  },
  {
    "description": "",
    "done": false,
    "id": 4,
    "title": "Buy stuff",
    "uri": "http://localhost:5000/todo/api/tasks/4"
  },
  {
    "description": "",
    "done": false,
    "id": 5,
    "title": "Buy stuff",
    "uri": "http://localhost:5000/todo/api/tasks/5"
  }
]
```

### `POST /todo/api/tasks`

Create new task.

#### Example

##### Request

```http
POST /todo/api/tasks HTTP/1.1
Host: localhost:5000
Content-Type: application/json
Authorization: Basic <your_basic_authentication_token_here>
Cache-Control: no-cache
Postman-Token: ef8b66ff-9ff1-4e11-a4e2-bda067aaa39e

{
    "title": "Be awesome",
    "description": ""
}
```

##### Response: 201 Created

```json
{
  "description": "",
  "done": false,
  "id": 8,
  "title": "Be awesome",
  "uri": "http://localhost:5000/todo/api/tasks/8"
}
```

### `GET /todo/api/tasks/:task_id`

Get single task.

#### Example

##### Request

```http
GET /todo/api/tasks/7 HTTP/1.1
Host: localhost:5000
Content-Type: application/json
Authorization: Basic <your_basic_authentication_token_here>
```

#### Response: 200 OK

```json
{
  "description": "😇",
  "done": true,
  "id": 7,
  "title": "Foobar",
  "uri": "http://localhost:5000/todo/api/tasks/7"
}
```

### `PUT /todo/api/tasks/:task_id`

Update a task.

#### Example

##### Request

```http
PUT /todo/api/tasks/7 HTTP/1.1
Host: localhost:5000
Content-Type: application/json
Authorization: Basic <your_basic_authentication_token_here>
Cache-Control: no-cache
Postman-Token: ab6d272a-95d1-4ffe-ba22-2f4b820a6a5d

{
    "done": false
}
```

##### Response: 200 OK

```json
{
  "description": "😇",
  "done": false,
  "id": 7,
  "title": "Foobar",
  "uri": "http://localhost:5000/todo/api/tasks/7"
}
```

### `DELETE /todo/api/tasks/:task_id`

Remove a task.

#### Example

##### Request

```http
DELETE /todo/api/tasks/7 HTTP/1.1
Host: localhost:5000
Content-Type: application/json
Authorization: Basic <your_basic_authentication_token_here>

{
    "done": false
}
```

##### Response: 200 OK

```json
{
  "result": true
}
```

### `GET /todo/api/health`

Health check.

#### Example Response

200 OK

```json
{
  "health": "ok!"
}
```
