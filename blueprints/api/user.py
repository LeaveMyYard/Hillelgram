# .../api/user
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import HTTPException
from models.user import RegistrationModel
from crud import user_crud
from core.db import get_connection

user_blueprint = Blueprint("user_blueprint", __name__, url_prefix="/user")


@user_blueprint.route("", methods=["POST"])
def register():
    if request.json is None:
        raise HTTPException("Json not found")

    registration_data = RegistrationModel(**request.json)

    with get_connection() as conn:
        user_crud.create(conn, registration_data)

    return jsonify({"info": "OK"})


@user_blueprint.route("")
def get_user_data():
    auth_data = request.authorization
    if auth_data is None:
        raise HTTPException("Auth headers not provided")

    with get_connection() as conn:
        user_crud.authenticate(conn, auth_data)
        user_data = user_crud.get(conn, auth_data.username)

    return jsonify(user_data.dict())
