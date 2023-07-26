from flask import Flask, render_template, request
import psycopg2
import os
from static.sql.functions import *
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='freskoconfirmation@gmail.com',
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
)
mail = Mail(app)

# Set db Constants
host='127.0.0.1'
user=os.getenv('DB_USER')
database=os.getenv('DB_NAME')
password=os.getenv('DB_PASSWORD')

# set email constants
sender='freskogreek@gmail.com'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/lunch')
def lunch():
    return render_template('lunch.html')

@app.route('/dinner')
def dinner():
    return render_template('dinner.html')

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        # Handle form submission
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        contact_number = request.form['contact_number']
        date = request.form['date']
        time = request.form['time']
        party_size = request.form['party_size']
        comment = request.form['comment']

        # get tables(s)
        available_tables=find_available_tables(start_time=date+' '+time, duration='01:30:00.000000',
                                               host=host,database=database,
                                               user=user, password=password)
        # tables=table_assigner(available_tables=available_tables, party_size=party_size)

        # write to db
        sql="""INSERT INTO public."booking" (booking_name, group_size, contact_phone, contact_email, start_time, table_id, comments) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        conn=connect_to_database(host=host, database=database, user=user,
                                 password=password)
        try:
            tables=table_assigner(available_tables=available_tables, party_size=party_size)
            with conn.cursor() as cursor:
                for table in tables:
                    cursor.execute(sql, (first_name+' '+last_name, party_size, contact_number, email, date+' '+time, table, comment))
                    conn.commit()
                cursor.close()
                conn.close()

                msg = Message(subject=f"{first_name}, you're going to Fresko!",
                              sender=sender, recipients=[email])
                msg.html=render_template('reservation_confirmation.html', first_name=first_name, last_name=last_name,
                                    email=email,contact_number=contact_number,date=date,
                                    time=time, party_size=party_size, comment=comment)
                mail.send(message=msg)
                
                return render_template('reservation_confirmation.html', first_name=first_name, last_name=last_name,
                                    email=email,contact_number=contact_number,date=date,
                                    time=time, party_size=party_size, comment=comment)
        except:
            return render_template('sorry.html')
    else:
        # Render the reservation form
        return render_template('reservation_form.html')

@app.route('/nutrition')
def nutrition():
    return render_template('nutrition.html')

@app.route('/delivery')
def delivery():
    return render_template('delivery.html')

@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

@app.route('/about-us')
def about_us():
    return render_template('about-us.html')

@app.route('/privacy')
def privacy():
    month='July'
    year='2023'
    return render_template('privacy.html', month=month, year=year)

@app.route('/terms-of-use')
def terms_of_use():
    month='July'
    year='2023'
    return render_template('terms-of-use.html', month=month, year=year)

@app.route('/cookies')
def cookies():
    return render_template('cookies.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    # Process the email and save it to the database
    return render_template('subscribe.html')

if __name__ == '__main__':
    app.run()
  