from flask import Flask, jsonify, request
from flask.views import MethodView
from db import Session, Advertisement
from errors import HttpError
from schema import CreateAdv, UpdateAdv, validate

app = Flask("app")

@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    return jsonify({"error": error.message}), error.status_code

class AdvView(MethodView):
    def get(self, adv_id: int):
        with Session() as session:
            adv = session.get(Advertisement, adv_id)
            if not adv:
                raise HttpError(404, "Advertisement not found")
            return jsonify(adv.dict)

    def post(self):
        data = validate(CreateAdv, request.json)
        with Session() as session:
            adv = Advertisement(**data)
            session.add(adv)
            session.commit()
            return jsonify({"id": adv.id}), 201

    def patch(self, adv_id: int):
        data = validate(UpdateAdv, request.json)
        with Session() as session:
            adv = session.get(Advertisement, adv_id)
            if not adv:
                raise HttpError(404, "Advertisement not found")
            for key, value in data.items():
                setattr(adv, key, value)
            session.add(adv)
            session.commit()
            return jsonify({"status": "updated"})

    def delete(self, adv_id: int):
        with Session() as session:
            adv = session.get(Advertisement, adv_id)
            if not adv:
                raise HttpError(404, "Advertisement not found")
            session.delete(adv)
            session.commit()
            return jsonify({"status": "deleted"})

adv_view = AdvView.as_view("adv_view")
app.add_url_rule("/advertisements", view_func=adv_view, methods=["POST"])
app.add_url_rule("/advertisements/<int:adv_id>", view_func=adv_view, methods=["GET", "PATCH", "DELETE"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)