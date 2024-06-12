from api.domain.code import Code
import sqlite3

class CodeRepository():
    def __init__(self) -> None:
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

    def find_all_by_user_id_and_game_name(self, user_id,game_name):
        self.cursor.execute("SELECT * FROM codes WHERE user_id = ? AND game_name = ?", (user_id, game_name))
        results = self.cursor.fetchall()
        code_list = []
        for data in results:
             code_list.append(Code(data[0],data[1],data[2],data[3]))
        return code_list
    
    def add_new_code(self, user_id: int, game_name: str, code: str):
        self.cursor.execute("INSERT INTO codes (user_id, game_name, code) VALUES (?, ?, ?)", (user_id, game_name, code))
        self.conn.commit()

        self.cursor.execute("SELECT * FROM codes WHERE user_id = ? AND game_name = ? AND code = ?", (user_id, game_name, code))
        return self.cursor.fetchall()[0]
    
    def update_code(self, user_id: int, game_name: str, code_id: int, new_code: str):
        self.cursor.execute("UPDATE codes SET code = ? WHERE id = ?", (new_code, code_id))
        self.conn.commit()

        self.cursor.execute("SELECT * FROM codes WHERE id = ?", (str(code_id)))
        reuslt = self.cursor.fetchall()[0]
        return Code(reuslt[0],reuslt[1],reuslt[2],reuslt[3])