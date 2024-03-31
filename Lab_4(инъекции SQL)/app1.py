import sqlite3
from flask import Flask, request, render_template

app = Flask(__name__)

conn = sqlite3.connect('my_data.db')
cursor = conn.cursor()
cursor.execute('''DROP TABLE IF EXISTS my_data''')
cursor.execute('''CREATE TABLE IF NOT EXISTS my_data (id INTEGER PRIMARY KEY, first_name TEXT, middle_name TEXT, last_name TEXT)''')
cursor.execute('''INSERT INTO my_data (first_name, middle_name, last_name) VALUES 
    ('Иван', 'Иванович', 'Иванов'),
    ('Федор', 'Федорович', 'Федоров')
    ''')
conn.commit()
conn.close()

@app.route('/')
def index():
    user_info = None
    message = None

    user_id = request.args.get('user_id')

    if user_id:
        user_info = get_user_info(user_id)

        if user_info:
            message = None
        else:
            message = "Пользователь с данным id не найден"

    return render_template('site.html', user_info=user_info, message=message)

def get_user_info(user_id):
    conn = sqlite3.connect('my_data.db')
    cursor = conn.cursor()
    query = 'SELECT * FROM my_data WHERE id = ?'
    cursor.execute(query, (user_id,))
    user_info = cursor.fetchone()
    conn.close()

    return user_info if user_info else None

if __name__ == '__main__':
    app.run(debug=True)
