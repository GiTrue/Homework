from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from db import Session, Advertisement, User
from errors import HttpError
from schema import CreateAdv, UpdateAdv, CreateUser, validate

app = Flask("app")
bcrypt = Bcrypt(app)

@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    return jsonify({"error": error.message}), error.status_code

def get_auth_user(session):
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        raise HttpError(401, "Authentication required")
    user = session.query(User).filter_by(email=auth.username).first()
    if user is None or not bcrypt.check_password_hash(user.password, auth.password):
        raise HttpError(401, "Invalid email or password")
    return user

class UserView(MethodView):
    def post(self):
        data = validate(CreateUser, request.json)
        data["password"] = bcrypt.generate_password_hash(data["password"]).decode()
        with Session() as session:
            try:
                user = User(**data)
                session.add(user)
                session.commit()
                return jsonify({"id": user.id}), 201
            except IntegrityError:
                raise HttpError(409, "User already exists")

class AdvView(MethodView):
    def get(self, adv_id: int):
        with Session() as session:
            adv = session.get(Advertisement, adv_id)
            if not adv:
                raise HttpError(404, "Not found")
            return jsonify(adv.dict)

    def post(self):
        with Session() as session:
            user = get_auth_user(session)
            data = validate(CreateAdv, request.json)
            adv = Advertisement(**data, owner_id=user.id)
            session.add(adv)
            session.commit()
            return jsonify({"id": adv.id}), 201

    def patch(self, adv_id: int):
        with Session() as session:
            user = get_auth_user(session)
            adv = session.get(Advertisement, adv_id)
            if not adv or adv.owner_id != user.id:
                raise HttpError(403, "Access denied")
            
            data = validate(UpdateAdv, request.json)
            for key, value in data.items():
                setattr(adv, key, value)
            session.commit()
            return jsonify({"status": "updated"})

    def delete(self, adv_id: int):
        with Session() as session:
            user = get_auth_user(session)
            adv = session.get(Advertisement, adv_id)
            if not adv or adv.owner_id != user.id:
                raise HttpError(403, "Access denied")
            
            session.delete(adv)
            session.commit()
            return jsonify({"status": "deleted"})

app.add_url_rule("/users", view_func=UserView.as_view("user_view"), methods=["POST"])
adv_view = AdvView.as_view("adv_view")
app.add_url_rule("/advertisements", view_func=adv_view, methods=["POST"])
app.add_url_rule("/advertisements/<int:adv_id>", view_func=adv_view, methods=["GET", "PATCH", "DELETE"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)