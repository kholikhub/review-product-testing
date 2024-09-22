from flask import Blueprint, request, jsonify
from connectors.mysql_connector import connection
from models.review import Review

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required

from decorators.role_checker import role_required

review_routes = Blueprint("review_routes", __name__)

@review_routes.route("/review", methods=['GET'])
@role_required("admin")
def review_home():

    Session = sessionmaker(connection)
    s = Session()
    # with Session() as s:

    try:
        # Logic Apps
        review_query = select(Review)

        search_keyword = request.args.get('query')
        if search_keyword != None:
            review_query = review_query.where(Review.email.like(f"%{search_keyword}%"))

        result = s.execute(review_query)
        reviews = []

        for row in result.scalars():
            reviews.append({
                'id': row.id,
                'email': row.email,
                'description': row.description,
                'rating': row.rating,
            })

        return {
            'reviews': reviews,
            'message' : "Hello, " + current_user.name
        }

        # for row in review.scalars():
        #     print(f'ID: {row.id}, Name: {row.name}')

        # Commit
    except Exception as e:
        # Rollback
        print(e)
        # Kirim Error Message
        return { 'message': 'Unexpected Error' }, 500
    finally : s.close()

    return { 'message': 'Success fetch review data'}, 200


@review_routes.route('/review', methods=['POST'])
@role_required("admin")
def review_insert():
    Session = sessionmaker(connection)
    s = Session()
    s.begin()
    try:
        NewReview = Review(
            email=request.form['email'],
            description=request.form['description'],
            rating=request.form['rating']
        )

        s.add(NewReview)
        s.commit()
    except Exception as e:
        s.rollback()
        return { "message": "Fail to Insert" }, 500
    finally : s.close()

    return { 'message': 'Success insert review data'}, 200


@review_routes.route('/review/<id>', methods=['DELETE'])
@role_required("admin")
def review_delete(id):
    Session = sessionmaker(connection)
    s = Session()
    s.begin()
    try:
        review = s.query(Review).filter(Review.id == id).first()
        s.delete(review)
        s.commit()
    except Exception as e:
        print(e)
        s.rollback()
        return { "message": "Fail to Delete" }, 500
    finally : s.close()
    return { 'message': 'Success delete review data'}, 200

@review_routes.route('/review/<id>', methods=['PUT'])
@role_required("admin")
def review_update(id):
    Session = sessionmaker(connection)
    s = Session()
    s.begin()
    try:
        review = s.query(Review).filter(Review.id == id).first()

        review.email = request.form['email']
        review.description = request.form['description']
        review.rating = request.form['rating']
        

        s.commit()
    except Exception as e:
        s.rollback()
        return { "message": "Fail to Update" }, 500
    finally : s.close()
    return { 'message': 'Success update review data'}, 200