import db_connector

def search_showing(genre=None, date_b=None, date_e=None, not_full=None, title=None):
    ##NEEDS A SECURE IMPLEMENTATION - VULNERABLE TO SQL INJECTION##
    call = "SELECT showing.idShowing, MovieName, ShowingDateTime, TheatreRoom_RoomNumber, TicketPrice, seats_left " \
           "FROM Showing left join Movie on Movie_idMovie=idMovie left join " \
           "(select idShowing, (Capacity-ifnull(attendance,0)) as seats_left, attendance, Capacity from Showing left join " \
           "(select count(Showing_idShowing) as attendance, Showing_idShowing from attend group by Showing_idShowing) as countShow on countShow.Showing_idShowing=idShowing " \
           "left join TheatreRoom on TheatreRoom_RoomNumber=RoomNumber) as seatsQuery on seatsQuery.idShowing=showing.idShowing "

    if genre or date_b or date_e or title or not_full:
        call += "WHERE "

    if genre:
        call += "Movie_idMovie IN (SELECT idMovie FROM Movie LEFT JOIN Genre on idMovie = Movie_idMovie WHERE Genre=\"{0}\") ".format(genre)

    if date_b and date_e:
        if genre:
            call += "AND "
        call += "ShowingDateTime BETWEEN \"{0}\" AND \"{1}\" ".format(date_b, date_e)

    if title:
        if genre or (date_b and date_e):
            call += "AND "
        call += "Movie_idMovie IN (SELECT idMovie FROM Movie WHERE MovieName=\"{0}\") ".format(title)

    if not_full:
        if genre or date_b or date_e or title:
            call += "AND "
        call += "seats_left > 0"

    return db_connector.query_db(call)


def selected_showing(showing_id):
    call = "SELECT showing.idShowing, MovieName, ShowingDateTime, TheatreRoom_RoomNumber, TicketPrice, seats_left " \
           "FROM Showing left join Movie on Movie_idMovie=idMovie left join " \
           "(select idShowing, (Capacity-ifnull(attendance,0)) as seats_left, attendance, Capacity from Showing left join " \
           "(select count(Showing_idShowing) as attendance, Showing_idShowing from attend group by Showing_idShowing) as countShow on countShow.Showing_idShowing=idShowing " \
           "left join TheatreRoom on TheatreRoom_RoomNumber=RoomNumber) as seatsQuery on seatsQuery.idShowing=showing.idShowing WHERE showing.idShowing=%s"
    return db_connector.query_db_param(call, (showing_id,))


def attend_showing(customer_id, showing_id):
    call = ("INSERT INTO Attend (Customer_idCustomer, Showing_idShowing)"
            "VALUES (%s, %s)")
    db_connector.append_row(call, (customer_id, showing_id))


def rate_showing(customer_id, showing_id, rating):
    call = ("UPDATE Attend set rating=%s WHERE Customer_idCustomer=%s AND Showing_idShowing=%s")
    db_connector.append_row(call, (rating, customer_id, showing_id))


def customer_movies(customer_id):
    query = ("select Showing_idShowing, MovieName, ShowingDateTime, TicketPrice, Rating from attend left join Showing on Showing_idShowing=idShowing "
            "left join Movie on Movie_idMovie=idMovie where Customer_idCustomer=%s")
    return db_connector.query_db_param(query, (customer_id,))


def customer_profile(customer_id):
    query = ("select * from Customer where idCustomer=%s")
    return db_connector.query_db_param(query, (customer_id,))

