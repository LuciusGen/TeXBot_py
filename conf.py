import _sqlite3

class Config:
    conn = _sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM conf")
    __token = cursor.fetchall()[0][0]

    conn.close()

    @staticmethod
    def get_token() -> str:
        return Config.__token