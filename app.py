from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret_key'
DATABASE = 'database.db'

# Initialize Database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Stock Management Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            expiration_date TEXT NOT NULL
        )
    ''')
    # Prosthesis Management Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prosthesis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            provider TEXT NOT NULL,
            payment_status TEXT NOT NULL
        )
    ''')
    # Appointments Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            patient_name TEXT NOT NULL
        )
    ''')
    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

# Add Stock
@app.route('/add_stock', methods=['POST'])
def add_stock():
    product_name = request.form['product_name']
    quantity = int(request.form['quantity'])
    expiration_date = request.form['expiration_date']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO stock (product_name, quantity, expiration_date) VALUES (?, ?, ?)',
                   (product_name, quantity, expiration_date))
    conn.commit()
    conn.close()
    flash('Stock added successfully!')
    return redirect(url_for('index'))

# View Stock with Alerts
@app.route('/stock')
def stock():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stock')
    stock_items = cursor.fetchall()
    # Check for alerts
    alerts = []
    today = datetime.today().date()
    for item in stock_items:
        if item[2] <= 5:
            alerts.append(f'Low stock alert: {item[1]} has only {item[2]} left.')
        if datetime.strptime(item[3], '%Y-%m-%d').date() < today:
            alerts.append(f'Expiration alert: {item[1]} has expired!')
    conn.close()
    return render_template('index.html', stock_items=stock_items, alerts=alerts)

# Add Prosthesis
@app.route('/add_prosthesis', methods=['POST'])
def add_prosthesis():
    name = request.form['name']
    provider = request.form['provider']
    payment_status = request.form['payment_status']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO prosthesis (name, provider, payment_status) VALUES (?, ?, ?)',
                   (name, provider, payment_status))
    conn.commit()
    conn.close()
    flash('Prosthesis added successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
