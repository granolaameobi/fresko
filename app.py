from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/lunch')
def lunch():
    # Retrieve menu items from a database or file
    menu_items = [
        {'name': 'Pork (GF)', 'price': '9.00'},
        {'name': 'Lamb (GF)', 'price': '9.00'},
        {'name': 'Falafel (GF)', 'price': '9.50'}
    ]
    return render_template('lunch.html',menu_items=menu_items)

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
        # Save reservation to a database or file
        return render_template('reservation_confirmation.html', first_name=first_name, last_name=last_name,
                               email=email,contact_number=contact_number,date=date,
                               time=time, party_size=party_size)
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

if __name__ == '__main__':
    app.run()
  