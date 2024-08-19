from flask import Flask, request, jsonify, send_file
from flask_mysqldb import MySQL
import random
import smtplib
import string
import os
from email.message import EmailMessage
import ssl

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tiger'
app.config['MYSQL_DB'] = 'iphone_waitlist'

mysql = MySQL(app)

@app.route('/')
def home():
    return send_file('./template/index.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data['name']
    email = data['email']
    phone = data['phone']
    referral_code = data.get('referralCode')
    cursor = mysql.connection.cursor()

    # Check for duplicate email
    cursor.execute('SELECT * FROM customers WHERE email = %s', (email,))
    if cursor.fetchone():
        return jsonify({'error': 'Email already registered'}), 400

    # Check for duplicate phone number
    cursor.execute('SELECT * FROM customers WHERE phone = %s', (phone,))
    if cursor.fetchone():
        return jsonify({'error': 'Phone number already registered'}), 400

    if referral_code:
        cursor.execute('SELECT * FROM customers WHERE referral_code = %s', (referral_code,))
        referrer = cursor.fetchone()
        if not referrer:
            return jsonify({'error': 'Invalid referral code'}), 400
        new_referrals = referrer[4] - 1
        print(new_referrals)
        cursor.execute('UPDATE customers SET referrals = %s WHERE referral_code = %s', (new_referrals, referral_code))
        
        # Calculate new position based on referrals
        cursor.execute('SELECT email, position, referrals, referral_code FROM customers ORDER BY referrals DESC, position ASC')
        customers = cursor.fetchall()
        for index, customer in enumerate(customers):
            cursor.execute('UPDATE customers SET position = %s WHERE email = %s', (99 + index, customer[0]))
        position = 99 + len(customers)
    else:
        cursor.execute('SELECT COUNT(*) FROM customers')
        count = cursor.fetchone()[0]
        position = 99 + count

    new_referral_code = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=9))
    cursor.execute('INSERT INTO customers (name, email, phone, position, referral_code) VALUES (%s, %s, %s, %s, %s)', (name, email, phone, position, new_referral_code))
    mysql.connection.commit()

    return jsonify({'position': position, 'referralCode': new_referral_code})

@app.route('/rank')
def rank():
    return send_file('./template/rank.html')

@app.route('/top10')
def top10():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT email, position, referral_code FROM customers ORDER BY referrals DESC, position ASC')
    top10 = cursor.fetchall()
    cursor.close()
    result = [{'email': row[0], 'position': row[1], 'referral_code': row[2]} for row in top10]
    return jsonify(result)

@app.route('/referral', methods=['POST'])
def referral():
    referral_code = request.json['referralCode']
    email = request.json['email']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM customers WHERE referral_code = %s', (referral_code,))
    referrer = cursor.fetchone()
    if referrer:
        cursor.execute('SELECT MAX(position) FROM customers')
        pos = cursor.fetchone()
        new_position = referrer[2] - 1 if referrer[2] >= 1 else 1
        cursor.execute('UPDATE customers SET position = %s WHERE referral_code = %s', (new_position, referral_code))
        cursor.execute('INSERT INTO customers (email, position, referral_code) VALUES (%s, %s, %s)', (email, pos + 1, ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=9))))
        mysql.connection.commit()
        if new_position<99:
            cursor.execute(f'SELECT email FROM customers WHERE referral_code = {referral_code}')
            reciever = cursor.fetchone()
            send_email(reciever, 'Iphone 16 Pre-Order Coupon Code')
        return jsonify({'referrerPosition': new_position})
    else:
        return jsonify({'error': 'Invalid referral code'}), 400

def send_email(email, subject):
    send = 'tharunmctv@gmail.com'
    password = os.environ.get('EMAIL_PASSWORD')
    reciever = email

    subject = "testing"
    coupon_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    body = f"""
    Dear Customer,

    Congratulations on joining our waitlist for the iPhone 16 pre-order!

    As a token of our appreciation, here is your exclusive coupon code: {coupon_code}

    Use this coupon code to get a special discount on your purchase.

    Thank you for being with us.

    Best Regards,
    Apple Team
    """

    em = EmailMessage()
    em['From'] = send
    em['To'] = reciever
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(send, password)
        smtp.sendmail(send, reciever, em.as_string())

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(send, password)
            smtp.sendmail(send, reciever, em.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == '__main__':
    app.run(debug=True)