from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import math


app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///registration_database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User_Registration(db.Model):

    id_no = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email_id = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    mobile_no = db.Column(db.String(12), unique=True, nullable=False)
    address = db.Column(db.String(150), nullable=False)

#db.create_all()


class Users(Resource):

    def get(self):

        page_no = request.args.get("page", 1, type=int)
        record_size = request.args.get("record_size", 5, type=int)
        database = User_Registration.query.filter_by().all()
        total_data = len(database)
        data = database[(page_no - 1) * record_size: ((page_no-1) * record_size)+record_size]
        user_list = []
        for data in data:
            user_data = {
                "id": data.id_no,
                "first_name": data.first_name,
                "last_name": data.last_name,
                "email_id": data.email_id,
                # "password": data.password,
                "mobile_no": data.mobile_no,
                "address": data.address
            }
            user_list.append(user_data)

        max_page_size = (len(user_list))
        if len(user_list) == 0:
            response = user_list
            return jsonify({
                "data": response,
                "is_success": False,
                "message": "Page not found",
                "current_page": page_no,
                "total_page": math.ceil(total_data / record_size)
            })

        if 1 <= page_no:
            response = user_list
            return jsonify({
                "data": response,
                "is_success": True,
                "message": "success",
                "current_page": page_no,
                "total_page": math.ceil(total_data/record_size)
            })



# http://127.0.0.1:5000/api/users
api.add_resource(Users, "/api/users")


if __name__ == '__main__':

    app.run(debug=True)






if __name__ == "__main__":
    app.run(debug=True)