from models.user import RegistrationModel, UserModel
import sqlite3
import uuid
from core import passwords
from werkzeug.datastructures import Authorization
from core.errors.auth_errors import AuthError
from core.errors.registration_errors import UserExistsError


class UserCRUD:
    def create(self, conn: sqlite3.Connection, data: RegistrationModel) -> None:
        cur = conn.cursor()

        try:
            user = self.get(conn, data.login)
            if user is not None:
                raise UserExistsError(f"User with login {data.login} already exists")

            user_id = uuid.uuid4()
            cur.execute(
                "INSERT INTO User VALUES(?, ?, ?)",
                (str(user_id), data.login, passwords.hash_password(data.password)),
            )
        finally:
            cur.close()

    def authenticate(self, conn: sqlite3.Connection, auth_data: Authorization) -> None:
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT password FROM User WHERE login=?", (auth_data.username,)
            )
            row = cur.fetchone()

            if row is None:
                raise AuthError("User does not exist")

            password_hashed = row[0]

            if not passwords.passwords_equal(auth_data.password, password_hashed):
                raise AuthError("Password is incorrect")
        finally:
            cur.close()

    def get(self, conn: sqlite3.Connection, login: str) -> UserModel | None:
        cur = conn.cursor()

        try:
            cur.execute("SELECT id, login FROM User WHERE login=?", (login,))
            row = cur.fetchone()

            if row is None:
                return None

            return UserModel(id=row[0], login=row[1])
        finally:
            cur.close()
