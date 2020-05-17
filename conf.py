import _sqlite3


class Config:
    """Class for work with bot configuration"""
    conn = _sqlite3.connect('database.db') # create data base
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM conf")  # select token in database
    __token = cursor.fetchall()[0][0]

    conn.close()

    __url = 'https://latex-edit-bot.herokuapp.com/'

    @staticmethod
    def get_token() -> str:
        return Config.__token

    @staticmethod
    def get_url() -> str:
        return Config.__url
