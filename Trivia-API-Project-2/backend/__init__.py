from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import os
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def pagination(page_num,all_questions):
  global QUESTIONS_PER_PAGE
  # calculate the start and end indexes of the question array
  start = (page_num-1)* QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  print(start,end)
  # if there is a little element remain
  size = len(all_questions)
  if end > size:
    end = size -1 

  return all_questions[start:end]

def create_app(test_config=None):
  global QUESTIONS_PER_PAGE
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  

  CORS(app)

  @app.after_request
  def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

  @app.route('/categories' , methods = ["GET"])
  def get_categories():
    all_categories = Category.query.all()

    return jsonify ( {
      "success" : True,
      "categories" : {category.id : category.type for category in all_categories},
      "total_categories" : len(all_categories)
    })

  @app.route('/questions', methods = ["GET"])
  def get_questions():
    try:
      questions = Question.query.all()
      all_categories = Category.query.all()
      page_num = request.args.get("page",1,type=int)
      questions = pagination(page_num, questions)

      all_categories= Category.query.all()
      
      return jsonify ({
        "questions" : [question.format() for question in questions],
        "totalQuestions" : len(questions),
        "currentCategory" : None,
        "categories" : {category.id : category.type for category in all_categories},
        "success" : True
      })
    except:
      abort(422)

  @app.route('/questions/<int:id>', methods = ["DELETE"])
  def delete_questions(id):
      deleted_question = Question.query.get(id)
      if deleted_question is None:
        abort(400)

      deleted_question.delete()
      # questions = Question.query.all()
      # questions = pagination(request, questions)
      return jsonify ({
              # "questions" : [question.format() for question in questions],
              # "totalQuestions" : len(questions),
              "success" : True,
              'deleted': id
            })

  @app.route("/questions",methods=["POST"])
  def add_question():
    try:

      data = request.get_json()
      print(data)

      if 'searchTerm' in data:
        searched_questions = Question.query.filter(Question.question.ilike("%{}%".format(data['searchTerm']))).all()
        print("ray2",searched_questions)
        return jsonify ({
            "questions": [question.format() for question in searched_questions],
            "totalQuestions": len(searched_questions),
            "currentCategory" : None,
            "success" : True
        })

      else:
        question = data ['question']
        answer = data ['answer']
        difficulty = data ['difficulty']
        category= data ['category']

        new_question = Question(question,answer,category,difficulty)
        new_question.insert()

        return jsonify ({
          "success" : True,
          "id" : new_question.id # for testing
        })
    except:
      # bad request
        abort(400)

  @app.route('/categories/<int:category_id>/questions', methods = ['GET'])
  def get_category_questions(category_id):

    category = Category.query.get(category_id)
    # invalid category
    if category is None:
      abort(404)

    # questions = Question.query.filter(Question.category == category_id).all()
    questions = category.questions

    return jsonify({
      "questions" : [question.format() for question in questions],
      "totalQuestions" : len(questions),
      "currentCategory" : None ,
      "success" : True
    })

  @app.route( '/quizzes', methods=['POST'])
  def get_next_question_quiz():
    try:
      data = request.get_json()
      print(data)
      previous_questions_ids = data['previous_questions']
      quiz_category_id = data['quiz_category']['id']

      # get all questions in that category
      questions = Question.query.filter(Question.category == quiz_category_id).all()
      # create a list of ids of that questions
      questions_ids = [question.id for question in questions]

      print(questions_ids)

      # remove the previous question id to select randomly another question
      for previous_questions_id in previous_questions_ids:
        questions_ids.remove(previous_questions_id)


      print(questions_ids)
      # if it is the last question
      if len(questions_ids) == 0:
        return jsonify ({ "question" : None }) 

      random_index = random.randrange( len(questions_ids) )     
      random_id = questions_ids[random_index]
      random_question = Question.query.get(random_id)

      return jsonify ({
        "question" : random_question.format(),
        "success" : True
      })

    except:
      # bad request (missing json in the request)
      abort(400)

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success" : False,
      "error" : 400,
      "message" : "Error Bad Request, you may forgot to send the json"
    }) , 400
    
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success" : False,
      "error" : 404,
      "message" : "Error Not Found"
    }) , 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success" : False,
      "error" : 422,
      "message" : "Error Un Proccessable"
    }) , 422
    

  return app

    

    
app = create_app()

if __name__ == '__main__':
  # print( Question.query.all()[0].category_name )
  # print( Category.query.all()[1].questions )
  app.run()

