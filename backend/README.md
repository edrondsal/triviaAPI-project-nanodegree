# Full Stack Trivia API Backend

Backend for the Trivia App, which allow to manage the questions and to play the game with a client frontend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql -d trivia -U udacity -f trivia.psql
```

### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

### Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql -d trivia_test -U udacity -f trivia.psql
python test_flaskr.py
```

## API Reference

The Trivia API is a RESTful JSON API. The sections below explain how to use the different API endpoints. 

The API is not deployed and can only be accessed through the localhost:

```
http://localhost:5000
```

### Open Endpoints

Open endpoints require no Authentication.

* [List Categories](#categories) : `GET /categories`
* [List Categories Questions](#categories-questions) : `GET /categories/<int:category_id>/questions`
* [List Questions](#questions) : `GET /questions?page=`
* [Search Questions](#question-search) : `POST /questions`
* [Create Question](#question-create) : `POST /questions`
* [Delete Question](#question-delete) : `DELETE /questions/<int:question_id>`
* [Play](#play) : `POST /quizzes`

### Endpoints that require Authentication

For this API there are not closed endpoints require a valid Token to be included in the header of the request.

### Status Codes

Trivia API returns the following status codes:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 404 | `NOT FOUND` |
| 422 | `UNPROCESSABLE` |
| 500 | `INTERNAL SERVER ERROR` |

### List Categories <a name="categories"></a>
Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding String of the category

**URL** : `/categories`

**Method** : `GET`

**Auth required** : NO

**Data constraints**: No data required in the body of the request

#### Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "success": true,
    "categories":{
        "1" : "Science",
        "2" : "Art",
        "3" : "Geography",
        "4" : "History",
        "5" : "Entertainment",
        "6" : "Sports"
    }
}
```

### List Questions by Category <a name="categories-questions"></a>

Retrieve all the questions for one category

**URL** : `/categories/<int:category_id>/questions`

**Method** : `GET`

**Auth required** : NO

**Data constraints**: No data required in the body of the request

#### Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "success": true,
    "questions": [ 
        {"id": int,
        "question": String,
        "answer": String,
        "category": int,
        "difficulty": int}, 
        ... ],
    "totalQuestions": 30,
    "currentCategory": 2
}
```

#### Error Response

**Condition** : If category does not exists or no question is found for the category

**Code** : `404 NOT FOUND`

**Content** :

```json
{
    "success": false,
    "error": 404,
    "message": "Not Found"
}
```

### List Questions <a name="questions"></a>

Retrieve a list of 10 questions for the page requested in the query

**URL** : `/questions?page=`

**Method** : `GET`

**Auth required** : NO

**Data constraints**: No data required in the body of the request

#### Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "success": true,
    "questions": [ 
        {"id": int,
        "question": String,
        "answer": String,
        "category": int,
        "difficulty": int}, 
        ... ],
    "categories": {
        "1" : "Science",
        "2" : "Art",
        "3" : "Geography",
        "4" : "History",
        "5" : "Entertainment",
        "6" : "Sports"
        },   
    "totalQuestions": 30,
    "currentCategory": 2
}
```

#### Error Response

**Condition** : If required page does not exist

**Code** : `404 NOT FOUND`

**Content** :

```json
{
    "success": false,
    "error": 404,
    "message": "Not Found"
}
```


### Search Questions <a name="question-search"></a>

Retrieve questions list for the question including the search term within their question if searchTerm is present in the body of the request.

**URL** : `/questions`

**Method** : `POST`

**Auth required** : NO

**Data constraints**: 

```json
{
    "searchTerm": String,
}
```

**Data example**

```json
{
    "searchTerm": "What is",
}
```

#### Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "success": true,
    "questions": [ 
        {"id": int,
        "question": String,
        "answer": String,
        "category": int,
        "difficulty": int}, 
        ... ],
    "totalQuestions": 30,
    "currentCategory": 2
}
```

#### Error Response

**Condition** : If question is found

**Code** : `404 NOT FOUND`

**Content** :

```json
{
    "success": false,
    "error": 404,
    "message": "Not Found"
}
```

### Create Question <a name="question-create"></a>

**URL** : `/questions`

**Method** : `POST`

**Auth required** : NO

**Data constraints**: 

```json
{
    "question": String,
    "answer": String,
    "category": int,
    "difficulty": int [1..5]
}
```

**Data example**

```json
{
    "question": "question",
    "answer": "answer of the question",
    "category": 2,
    "difficulty": 3
}
```

#### Success Response

**Code** : `201 OK`

**Content example**

```json
{
    "success": true
}
```

#### Error Response

##### Unprocessable
**Condition** : If body of request not well formated or data missing

**Code** : `422 UNPROCESSABLE`

**Content** :

```json
{
    "success":False,
    "error": 422,
    "message": "unprocessable"
}
```
##### Internal Server Error
**Condition** : If error when recording the new question in the database

**Code** : `500 INTERNAL SERVER ERROR`

**Content** :

```json
{
    "success": false,
    "error": 500,
    "message": "Internal Server Error"
}
```

### Delete Question <a name="question-delete"></a>

**URL** : `/questions/<int:question_id>`

**Method** : `DELETE`

**Auth required** : NO

**Data constraints**: No data required in the body of the request


#### Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "success": true,
    "question": {
        "id": int,
        "question": String,
        "answer": String,
        "category": int,
        "difficulty": int
    }
}
```

#### Error Response

##### Unprocessable

**Condition** : If question with `question_id` does not exist

**Code** : `422 UNPROCESSABLE`

**Content** :

```json
{
    "success":False,
    "error": 422,
    "message": "unprocessable"
}
```
##### Internal Server Error
**Condition** : If error when deleting the question from the database

**Code** : `500 INTERNAL SERVER ERROR`

**Content** :

```json
{
    "success": false,
    "error": 500,
    "message": "Internal Server Error"
}
```

### Play Trivia App <a name="play"></a>
take category and previous question parameters and return next question within the given category, if provided, and that is not one of the previous questions.

**URL** : `/quizzes`

**Method** : `POST`

**Auth required** : NO

**Data constraints**: 

```json
{
    "quiz_category": {
        "id": int,
        "type": String
    },
    "previous_questions": Array[int]
}
```

**Data example**

```json
{
    "quiz_category": {
        "id": 2,
        "type": "Art"
    },
    "previous_questions": [2, 3, 12, 43]
}
```

#### Success Response

If a next question is found:
**Code** : `200 OK`

**Content example**

```json
{
    "success": true,
    "question": {
        "id": int,
        "question": String,
        "answer": String,
        "category": int,
        "difficulty": int
    }
}
```

If no next question is found:
**Code** : `200 OK`

**Content example**

```json
{
    "success": false
}
``` 

#### Error Response

**Condition** : When body of the request does not comply with the Data Constraint define above

**Code** : `422 UNPROCESSABLE`

**Content** :

```json
{
    "success":False,
    "error": 422,
    "message": "unprocessable"
}
```



