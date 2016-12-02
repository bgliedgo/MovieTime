from flask import Flask, render_template, request, redirect, url_for, flash
import db_connector
import customer_models
import staff_models


app = Flask(__name__)
app.secret_key = 'key123'


@app.route("/",  methods=["POST", "GET"])
def showings():
    genres = db_connector.query_db("SELECT DISTINCT Genre FROM Genre")
    if request.method == 'GET':
        showings = customer_models.search_showing()
    elif request.method == 'POST':
        showings = customer_models.search_showing(request.form['genre'],
                                                  request.form['b_date'],
                                                  request.form['a_date'],
                                                  request.form.get('not_full'),
                                                  request.form['title'])

    return render_template('showings.html', showings=showings, genres=genres)


@app.route("/tickets/<showing_id>/", methods=["POST", "GET"])
def buy_tickets(showing_id):
    if request.method == 'GET':
        showing = customer_models.selected_showing(showing_id)
        customers = staff_models.get_customers()
        return render_template('tickets.html', showing=showing[0], customers=customers)
    elif request.method == 'POST':
        if request.form.get('customer'):
            customer_models.attend_showing(request.form.get('customer'),
                                           request.form.get('showing'))

        return redirect(url_for('showings'))


@app.route("/customer/")
def customer_list():
    customers = staff_models.get_customers()
    return render_template('customer.html', customers=customers)


@app.route("/customer/<customer_id>/", methods=["POST", "GET"])
def customer_profile(customer_id):
    if request.method == 'POST':
        customer_models.rate_showing(customer_id,
                                     request.form.get('showing'),
                                     request.form.get('rating'))

    user_profile = customer_models.customer_profile(customer_id)
    profile = user_profile[0] + (user_profile[0][4].decode("utf-8"), )
    user_movies = customer_models.customer_movies(customer_id)
    return render_template('customer_profile.html',
                           profile=profile,
                           movies=user_movies)


@app.route("/staff/")
def stall_login():
    return render_template('staff_login.html')



@app.route("/staff/movies/", methods=["POST", "GET"])
def movie_admin():
    if request.method == 'POST':
        if request.form.get('delete'):
            try:
                staff_models.delete_movie(request.form.get('delete'))
            except:
                flash('ERROR: Movie has booked showings - can\'t delete!', 'error')
        elif request.form.get('new_title'):
            try:
                staff_models.add_movie(request.form.get('new_title'),
                                       request.form.get('new_year'))
            except:
                flash('Error adding new movie')
        elif request.form.get('edit_id'):
            try:
                staff_models.modify_movie(request.form.get('edit_id'),
                                          request.form.get('edit_title'),
                                          request.form.get('edit_year'))
            except:
                flash('Error Editing Movie')

    movies = staff_models.get_movies()
    return render_template('admin_templates/movie_admin.html', movies=movies)


@app.route("/staff/genres/", methods=["POST", "GET"])
def genre_admin():
    if request.method == 'POST':
        if request.form.get('delete_id') and request.form.get('delete_genre'):
            try:
                staff_models.delete_genre(request.form.get('delete_id'),
                                          request.form.get('delete_genre'))
            except:
                flash('Error Deleting Genre')
        elif request.form.get('new_movie') and request.form.get('new_genre'):
            try:
                staff_models.add_genre(request.form.get('new_movie'),
                                       request.form.get('new_genre'))
            except:
                flash('Error Adding Genre')
    movies = staff_models.get_movies()
    genres = staff_models.get_genres()
    return render_template('admin_templates/genre_admin.html', genres=genres, movies=movies)

@app.route("/staff/rooms/", methods=["POST", "GET"])
def room_admin():
    if request.method == 'POST':
        if request.form.get('delete'):
            try:
                staff_models.delete_room(request.form.get('delete'))
            except:
                flash('Error Deleting Room')
        elif request.form.get('new_id'):
            try:
                staff_models.add_room(request.form.get('new_id'),
                                      request.form.get('new_capacity'))
            except:
                flash('Error Adding Room')
        elif request.form.get('edit_id'):
            try:
                staff_models.modify_room(request.form.get('edit_id'),
                                         request.form.get('edit_id_new'),
                                         request.form.get('edit_capacity'))
            except:
                flash('Error Editing Room')
    rooms = staff_models.get_rooms()
    return render_template('admin_templates/room_admin.html', rooms=rooms)


@app.route("/staff/showings/", methods=["POST", "GET"])
def showing_admin():
    if request.method == 'POST':
        if request.form.get('delete'):
            try:
                staff_models.delete_showing(request.form.get('delete'))
            except:
                flash('Error Deleting Showing')
        if request.form.get('new_movie') and request.form.get('new_date'):
            try:
                staff_models.add_showing(request.form.get('new_date'),
                                         request.form.get('new_movie'),
                                         request.form.get('new_room'),
                                         request.form.get('new_price'))
            except:
                flash('Error Adding Showing')
        if request.form.get('edit_id'):
            try:
                staff_models.modify_showing(request.form.get('edit_id'),
                                            request.form.get('edit_date'),
                                            request.form.get('edit_movie'),
                                            request.form.get('edit_room'),
                                            request.form.get('edit_price'))
            except:
                flash('Error Editing Showing')

    showings = staff_models.get_showings()
    movies = staff_models.get_movies()
    rooms = staff_models.get_rooms()
    return render_template('admin_templates/showing_admin.html', showings=showings,
                           movies=movies, rooms=rooms)


@app.route("/staff/customers/", methods=["POST", "GET"])
def customer_admin():
    if request.method == 'POST':
        if request.form.get('delete'):
            try:
                staff_models.delete_customer(request.form.get('delete'))
            except:
                flash('Error Deleting Customer')
        if request.form.get('new_fname') and request.form.get('new_lname'):
            try:
                staff_models.add_customer(request.form.get('new_fname'),
                                         request.form.get('new_lname'),
                                         request.form.get('new_email'),
                                         request.form.get('new_sex'))
            except:
                raise
                flash('Error Adding Customer')
        if request.form.get('edit_id'):
            try:
                staff_models.modify_customer(request.form.get('edit_id'),
                                            request.form.get('edit_fname'),
                                            request.form.get('edit_lname'),
                                            request.form.get('edit_email'),
                                            request.form.get('edit_sex'))
            except:
                flash('Error Editing Customer')

    customers_response = staff_models.get_customers()
    customers=[]
    for customer in customers_response:
        customers.append(customer + (customer[4].decode("utf-8"),))
    return render_template('admin_templates/customer_admin.html', customers=customers)


@app.route("/staff/attend/", methods=["GET"])
def attend_admin():
    attends = staff_models.get_attendance()
    return render_template('admin_templates/attend_admin.html', attends=attends)


@app.route("/sql_injection/", methods=["GET", "POST"])
def sql_injection():
    data = ''
    if request.method == 'POST':
        call = 'SELECT * FROM Customer WHERE idCustomer=\'{0}\''.format(request.form.get('sql'))
        data = db_connector.query_db(call)

    return render_template("sql_injection.html", data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

