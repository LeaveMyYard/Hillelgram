from models.user import RegistrationModel, UserModel
import sqlite3
import uuid
from core import passwords
from werkzeug.datastructures import Authorization
from core.errors.auth_errors import AuthError


class UserCRUD:
    def create(self, conn: sqlite3.Connection, data: RegistrationModel) -> None:
        cur = conn.cursor()

        user_id = uuid.uuid4()
        cur.execute(
            "INSERT INTO User VALUES(?, ?, ?)",
            (str(user_id), data.login, passwords.hash_password(data.password)),
        )

        cur.close()

    def authenticate(self, conn: sqlite3.Connection, auth_data: Authorization) -> None:
        cur = conn.cursor()

        cur.execute("SELECT password FROM User WHERE login=?", (auth_data.username,))
        row = cur.fetchone()

        if row is None:
            raise AuthError("User does not exist")

        password_hashed = row[0]

        if not passwords.passwords_equal(auth_data.password, password_hashed):
            raise AuthError("Password is incorrect")

        cur.close()

    def get(self, conn: sqlite3.Connection, login: str) -> UserModel:
        cur = conn.cursor()

        cur.execute("SELECT id, login FROM User WHERE login=?", (login,))
        row = cur.fetchone()

        if row is None:
            raise ValueError(f"No user with login {login}")

        cur.close()

        return UserModel(id=row[0], login=row[1])
