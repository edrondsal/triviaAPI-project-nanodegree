import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def formatCategories(categories):
  categoriesDict= {}
  #set the database query in the format for the frontend
  for category in categories:
    categoriesDict[category.id] = category.type
  return categoriesDict

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  db = setup_db(app)
  
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  @app.route('/categories', methods=['GET'])
  def categories():
    """Retrieve the entire list of categories in the database
    Keyword arguments:
    """
    categories = Category.query.order_by(Category.id).all()
    data = {
      'success': True,
      'categories': formatCategories(categories)
    }
    return jsonify(data)

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def questions_by_categorie(category_id):
    """Retrieve all the questions for one category
    Keyword arguments:
    category_id -- the integer id of the category
    """    
    questions = Question.query.filter_by(category = category_id).all()
    if questions is None or len(questions)==0:
      abort(404)
    data = {
      'success': True,
      'questions': [question.format() for question in questions],
      'totalQuestions': len(questions),
      'currentCategory': category_id
    }
    return jsonify(data)
  
  @app.route('/questions', methods=['GET'])
  def questions():
    """Retrieve QUESTIONS_PER_PAGE for the page requested in the query
    Keyword arguments:
    """
    page = request.args.get('page', 1, type=int)

    questions = Question.query.order_by(Question.id).all()
    categories = Category.query.order_by(Category.id).all()

    offset = (page-1)*QUESTIONS_PER_PAGE
    limit = min(offset + QUESTIONS_PER_PAGE,len(questions)-1)

    if offset>len(questions):
      abort(404)
    data = {
      'success': True,
      'questions': [question.format() for question in questions][offset:limit],
      'totalQuestions': len(questions),
      'categories': formatCategories(categories),
      'currentCategory': questions[0].category
    }
    return jsonify(data) 

  @app.route('/questions', methods=['POST'])
  def search_or_post_questions():
    """Retrieve questions list for the question including the search term within their question if searchTerm is present in the body
    else check if the body of the POST request have the data necessary to create a new question and create it if possible
    Keyword arguments:
    """
    body = request.get_json()
    searchTerm = body.get('searchTerm',None)
    if searchTerm is None:
      question = body.get('question',None)
      answer = body.get('answer',None)
      difficulty = body.get('difficulty',None)
      category= body.get('category',None)
      if question is None or answer is None or difficulty is None or category is None:
        abort(422)     
      error = False
      try:
        question = Question(question=question,answer=answer,category=category,difficulty=difficulty)
        question.insert()
      except:
        db.session.rollback()
        error=True
      finally:
        db.session.close()    
      if error:
        abort(500)
      else:
        return jsonify({'success':True}),201
    else:
      search = f'%{searchTerm}%'
      questions = Question.query.filter(Question.question.ilike(search)).all()
      if len(questions) == 0:
        abort(404)
      data = {
        'success': True,
        'questions': [question.format() for question in questions],
        'totalQuestions': len(questions),
        'currentCategory': questions[0].category
      }
      return jsonify(data),200
  
  @app.route('/questions/<int:question_id>',methods=['DELETE'])
  def delete_question(question_id):
    """Delete the question
    Keyword arguments:
    question_id -- the integer id of the question to delete
    """
    question = Question.query.filter_by(id = question_id).first()
    if question is None:
      abort(422)
    else:
      error=False
      try:
        question.delete()
      except:
        db.session.rollback()
        error=True
        print(sys.exc_info())
      finally:
        db.session.close()
      if error:
        abort(500)
      else:  
        data = {
          'success':True,
          'question': question.format()
        }
        return jsonify(data)      

  @app.route('/quizzes',methods=['POST'])
  def next_question():
    """take category and previous question parameters and return next question within the given category, 
    if provided, and that is not one of the previous questions.
    Keyword arguments:
    """
    body = request.get_json()
    if body is None:
      abort(422)
    quizCategory = body.get('quiz_category',None)
    previousQuestions = body.get('previous_questions',None)

    if quizCategory is None or previousQuestions is None:
      abort(422)
    
    category = quizCategory.get('id',None)
    if(category is None):
      abort(422)
    category_id = int(category)
    question = Question.query.filter(Question.category == category_id).filter(Question.id.notin_(previousQuestions)).first()
    if question is None:
      return jsonify({'success':False})
    
    data={
      'success':True,
      'question': question.format()
    }
    return jsonify(data)


  #  Error Handlers
  #  ----------------------------------------------------------------
  @app.errorhandler(404)
  def not_found_error(error):
    data = {
      'success':False,
      'error': 404,
      'message': 'Not Found'
    }
    return jsonify(data), 404
  
  @app.errorhandler(422)
  def unprocessable_error(error):
    data = {
      'success':False,
      'error': 422,
      'message': 'unprocessable'
    }
    return jsonify(data), 422

  @app.errorhandler(500)
  def server_error(error):
    data = {
      'success':False,
      'error': 500,
      'message': 'Internal Server Error'
    }
    return jsonify(data), 500
  
  return app

    