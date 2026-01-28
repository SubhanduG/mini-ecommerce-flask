from database.db_config import get_getconnection
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector import IntegrityError
import smtplib
from email.mime.text import MIMEText
import random
import datetime


def send_otp_email(email, otp):
    print("===================================")
    print(f"[DEBUG OTP]")
    print(f"Email: {email}")
    print(f"OTP  : {otp}")
    print("===================================")


def create_user(username, email, password):
    conn = get_getconnection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id FROM users WHERE username=%s OR email=%s", (username, email))
        if cursor.fetchone():
            raise ValueError("Username or email already exists")

        hashed_password = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users (username, email, password_hash, is_verified) VALUES (%s,%s,%s,0)",
            (username, email, hashed_password)
        )
        conn.commit()

        otp = str(random.randint(100000, 999999))
        expires_at = datetime.datetime.now() + datetime.timedelta(minutes=10)
        cursor.execute(
            "INSERT INTO email_otp (email, otp, type, expires_at) VALUES (%s,%s,'register',%s)",
            (email, otp, expires_at)
        )
        conn.commit()

        send_otp_email(email, otp)
        return True
    finally:
        cursor.close()
        conn.close()


def verify_registration_otp(email, otp):
    conn = get_getconnection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM email_otp WHERE email=%s AND otp=%s AND type='register' AND expires_at>NOW()",
            (email, otp)
        )
        record = cursor.fetchone()
        if not record:
            return False

        cursor.execute(
            "UPDATE users SET is_verified=1 WHERE email=%s", (email,))
        conn.commit()

        cursor.execute("DELETE FROM email_otp WHERE id=%s", (record['id'],))
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()


def authenticate_user(identifier, password):
    conn = get_getconnection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM users WHERE username=%s OR email=%s", (identifier, identifier))
        user = cursor.fetchone()
        if user and check_password_hash(user["password_hash"], password):
            if user["is_verified"] == 0:
                raise ValueError("Email not verified")
            return user
        return None
    finally:
        cursor.close()
        conn.close()


def send_forgot_password_otp(email):
    conn = get_getconnection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        if not user:
            return False

        otp = str(random.randint(100000, 999999))
        expires_at = datetime.datetime.now() + datetime.timedelta(minutes=10)
        cursor.execute(
            "INSERT INTO email_otp (email, otp, type, expires_at) VALUES (%s,%s,'forgot',%s)",
            (email, otp, expires_at)
        )
        conn.commit()
        send_otp_email(email, otp)
        return True
    finally:
        cursor.close()
        conn.close()


def reset_password_with_otp(email, otp, new_password):
    conn = get_getconnection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM email_otp WHERE email=%s AND otp=%s AND type='forgot' AND expires_at>NOW()",
            (email, otp)
        )
        record = cursor.fetchone()
        if not record:
            return False

        hashed_password = generate_password_hash(new_password)
        cursor.execute(
            "UPDATE users SET password_hash=%s WHERE email=%s", (hashed_password, email))
        conn.commit()

        cursor.execute("DELETE FROM email_otp WHERE id=%s", (record['id'],))
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()
