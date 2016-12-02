import db_connector


def add_movie(movie_name, movie_year):
    call = ("INSERT INTO Movie (MovieName, MovieYear)"
            "VALUES (%s, %s)")
    db_connector.append_row(call, (movie_name, movie_year))


def delete_movie(movie_id):
    call = ("DELETE FROM Genre WHERE Movie_idMovie=%s")
    db_connector.append_row(call, (movie_id,))

    call = ("DELETE FROM Movie WHERE idMovie=%s")
    db_connector.append_row(call, (movie_id,))


def modify_movie(movie_id, new_movie_name=None, new_movie_year=None):
    if new_movie_name:
        call = ("UPDATE Movie SET MovieName=%s WHERE idMovie=%s")
        db_connector.append_row(call, (new_movie_name, movie_id))

    if new_movie_year:
        call = ("UPDATE Movie SET MovieYear=%s WHERE idMovie=%s")
        db_connector.append_row(call, (new_movie_year, movie_id))


def get_movies():
    query = ("SELECT * FROM Movie ORDER BY MovieName")
    return db_connector.query_db(query)


def add_genre(movie_id, genre):
    call = ("INSERT INTO Genre (Genre, Movie_idMovie)"
            "VALUES (%s, %s)")
    db_connector.append_row(call, (genre, movie_id))


def delete_genre(movie_id, genre):
    call = ("DELETE FROM Genre WHERE Movie_idMovie=%s AND Genre=%s")
    db_connector.append_row(call, (movie_id, genre))


def get_genres():
    query = ("SELECT Genre, MovieName, idMovie FROM Genre LEFT JOIN Movie "
             "ON Movie_idMovie=idMovie ORDER BY Genre")
    return db_connector.query_db(query)


def add_room(room_num, capacity):
    call = ("INSERT INTO TheatreRoom (RoomNumber, Capacity)"
            "VALUES (%s, %s)")
    db_connector.append_row(call, (room_num, capacity))


def delete_room(room_num):
    call = ("DELETE FROM TheatreRoom WHERE RoomNumber=%s")
    db_connector.append_row(call, (room_num,))


def modify_room(room_num, new_room_num=None, new_capacity=None):
    if new_capacity:
        call = ("UPDATE TheatreRoom SET Capacity=%s WHERE RoomNumber=%s")
        db_connector.append_row(call, (new_capacity, room_num))

    if new_room_num:
        call = ("UPDATE TheatreRoom SET RoomNumber=%s WHERE RoomNumber=%s")
        db_connector.append_row(call, (new_room_num, new_capacity))


def get_rooms():
    query = ("SELECT * FROM TheatreRoom")
    return db_connector.query_db(query)


def add_showing(date_time, movie_id, room_num, price):
    call = ("INSERT INTO Showing (ShowingDateTime, "
            "Movie_idMovie, TheatreRoom_RoomNumber, TicketPrice) "
            "VALUES(%s, %s, %s, %s)")
    db_connector.append_row(call, (date_time, movie_id, room_num, price))


def delete_showing(showing_id):
    call = ("DELETE FROM Showing WHERE idShowing=%s")
    db_connector.append_row(call, (showing_id,))


def modify_showing(showing_id, new_date=None, new_movie_id=None,
                   new_room_num=None, new_price=None):
    if new_date:
        call = ("UPDATE Showing SET ShowingDateTime=%s WHERE idShowing=%s")
        db_connector.append_row(call, (new_date, showing_id))

    if new_movie_id:
        call = ("UPDATE Showing SET Movie_idMovie=%s WHERE idShowing=%s")
        db_connector.append_row(call, (new_movie_id, showing_id))

    if new_room_num:
        call = ("UPDATE Showing SET TheatreRoom_RoomNumber=%s WHERE idShowing=%s")
        db_connector.append_row(call, (new_room_num, showing_id))

    if new_price:
        call = ("UPDATE Showing SET TicketPrice=%s WHERE idShowing=%s")
        db_connector.append_row(call, (new_price, showing_id))


def get_showings():
    query = ("select idShowing, ShowingDateTime, MovieName, TheatreRoom_RoomNumber, TicketPrice "
             "from Showing left join Movie on Movie_idMovie=idMovie ORDER BY ShowingDateTime")
    return db_connector.query_db(query)


def add_customer(fname, lname, email, sex):
    call = ("INSERT INTO Customer (FirstName, LastName, EmailAddress, Sex) "
            "VALUES(%s, %s, %s, %s)")
    db_connector.append_row(call, (fname, lname, email, sex))


def delete_customer(customer_id):
    call = ("DELETE FROM Customer WHERE idCustomer=%s")
    db_connector.append_row(call, (customer_id,))


def modify_customer(customer_id, new_fname=None, new_lname=None,
                    new_email=None, new_sex=None):
    if new_fname:
        call = ("UPDATE Customer SET FirstName=%s WHERE idCustomer=%s")
        db_connector.append_row(call, (new_fname, customer_id))

    if new_lname:
        call = ("UPDATE Customer SET LastName=%s WHERE idCustomer=%s")
        db_connector.append_row(call, (new_lname, customer_id))

    if new_email:
        call = ("UPDATE Customer SET EmailAddress=%s WHERE idCustomer=%s")
        db_connector.append_row(call, (new_email, customer_id))

    if new_sex:
        call = ("UPDATE Customer SET Sex=%s WHERE idCustomer=%s")
        db_connector.append_row(call, (new_sex, customer_id))


def get_customers():
    query = ("SELECT * FROM Customer ORDER BY LastName")
    return db_connector.query_db(query)


def get_attendance():
    query = ("select idShowing, idCustomer, FirstName, LastName, MovieName, ShowingDateTime, TicketPrice, Rating "
             "from Attend left join Customer on Customer_idCustomer=idCustomer "
             "left join Showing on Showing_idShowing=idShowing "
             "left join Movie on Movie_idMovie=idMovie order by Rating")
    return db_connector.query_db(query)

