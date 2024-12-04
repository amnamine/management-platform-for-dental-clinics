from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database initialization
DATABASE = 'database.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Stock Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            expiration_date TEXT
        )
    ''')
    # Prosthesis Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prosthesis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            payment_status TEXT
        )
    ''')
    # Appointments Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor TEXT NOT NULL,
            date TEXT,
            time TEXT
        )
    ''')
    # User Roles Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            role TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize Database
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_stock', methods=['POST'])
def add_stock():
    product_name = request.form['product_name']
    quantity = request.form['quantity']
    expiration_date = request.form['expiration_date']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO stock (product_name, quantity, expiration_date) VALUES (?, ?, ?)',
                   (product_name, quantity, expiration_date))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/stock')
def stock():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stock')
    items = cursor.fetchall()
    conn.close()
    return render_template('index.html', stock_items=items)

if __name__ == '__main__':
    app.run(debug=True)
