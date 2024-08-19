import os
import random
import string
from email.message import EmailMessage
import ssl
import smtplib


def send_email(email, subject):
    send = 'tharunmctv@gmail.com'
    password = os.environ.get('EMAIL_PASSWORD')
    reciever = 'tharunmbecse@gmail.com'

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

send_email('tharunmbecse@gmail.com', 'Congrats...')

# import os
# import random
# import string
# from email.message import EmailMessage
# import ssl
# import smtplib

# send = 'tharunmctv@gmail.com'
# password = os.environ.get('EMAIL_PASSWORD')
# reciever = 'tharunmbecse@gmail.com'

# subject = "testing"
# coupon_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
# body = f"""
# Dear Customer,

# Congratulations on joining our waitlist for the iPhone 16 pre-order!

# As a token of our appreciation, here is your exclusive coupon code: {coupon_code}

# Use this coupon code to get a special discount on your purchase.

# Thank you for being with us.

# Best Regards,
# Apple Team
# """

# em = EmailMessage()
# em['From'] = send
# em['To'] = reciever
# em['Subject'] = subject
# em.set_content(body)

# context = ssl.create_default_context()

# with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#     smtp.login(send, password)
#     smtp.sendmail(send, reciever, em.as_string())