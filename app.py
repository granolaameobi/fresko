from flask import Flask, render_template, request
import psycopg2
import os
from static.sql.functions import *
from kubernetes import client, config
import base64

app = Flask(__name__)

# Set db Constants
host='35.205.66.81'
database='Fresko'
user='postgres'

# Set db Password

import os

if 'KUBERNETES_SERVICE_HOST' in os.environ:
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    secret = v1.read_namespaced_secret("my-secret", "")
    password = base64.b64decode(secret.data["DB_PASSWORD"]).decode('utf-8')
else:
    password=os.getenv('DB_PASSWORD')

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
    # Retrieve menu items from a database or file
    menu_items = [
        {'name': 'Pork (GF)', 'price': '9.00'},
        {'name': 'Lamb (GF)', 'price': '9.00'},
        {'name': 'Falafel (GF)', 'price': '9.50'}
    ]
    return render_template('dinner.html',menu_items=menu_items)

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
        available_tables=find_available_tables(start_time=date+' '+time+'.000000',duration='02:00:00.000000',
                                               host=host,database=database,
                                               user=user, password=password)
        tables=table_assigner(available_tables=available_tables, party_size=party_size)

        # write to db
        sql="""INSERT INTO public."Booking" (booking_id, booking_name, group_size, contact_phone, contact_email, start_time, duration, table_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        data=(9, first_name+' '+last_name, party_size, contact_number, email, date+' '+time+'.000000', '02:00:00.000000', tables[0])
        conn=connect_to_database(host=host, database=database, user=user,
                                 password=password)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, data)
                conn.commit()
                cursor.close()
                conn.close()
                return render_template('reservation_confirmation.html', first_name=first_name, last_name=last_name,
                                    email=email,contact_number=contact_number,date=date,
                                    time=time, party_size=party_size, comment=comment)
        except:
            return 'Error inserting data into database'
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
  