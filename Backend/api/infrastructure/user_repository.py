from api.domain.user import User
import sqlite3


class UserRepository:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

    def add(self, user: User) -> None:
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username,user.password))
        self.conn.commit()
    
    def find_by_username_and_password(self, username: str, password: str) -> User:
        print(username,password)
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username,password))
        results = self.cursor.fetchall()
        if len(results) == 1:
            return User(results[0][0],results[0][1],results[0][2])
        return None
    
