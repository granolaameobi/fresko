from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    # Retrieve menu items from a database or file
    menu_items = [
        {'name': 'Hamburger', 'price': 9.99},
        {'name': 'Cheese Pizza', 'price': 12.99},
        {'name': 'Caesar Salad', 'price': 7.99}
    ]
    return render_template('menu.html', menu_items=menu_items)

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        # Handle form submission
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        party_size = request.form['party_size']
        # Save reservation to a database or file
        return render_template('reservation_confirmation.html', name=name, date=date, time=time, party_size=party_size)
    else:
        # Render the reservation form
        return render_template('reservation_form.html')

if __name__ == '__main__':
    app.run()
  