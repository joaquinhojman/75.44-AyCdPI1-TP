from csv import writer, reader, QUOTE_MINIMAL

DB_ROUTE_USERS = './db'
DB_ROUTE_HOUSES = './db_houses'

try:
    with open(DB_ROUTE_USERS, 'x', newline='\n'):
        pass
except:
    pass

def user_exists(username):
    with open(DB_ROUTE_USERS, 'r', newline='\n') as db:
        read = reader(db, delimiter=';')
        for row in read:
            if row[0] == username:
                return True, row
    return False, None

def user_create(username, password):
    with open(DB_ROUTE_USERS, 'a', newline='\n') as db:
        write = writer(db, delimiter=';', quoting=QUOTE_MINIMAL)
        write.writerow((username, password))

def house_create(description, start_date, end_date):
    with open(DB_ROUTE_HOUSES, 'a', newline='\n') as db:
        write = writer(db, delimiter=';', quoting=QUOTE_MINIMAL)
        write.writerow((description, start_date, end_date))

def read_houses():
    with open(DB_ROUTE_HOUSES, 'r', newline='\n') as db:
        f = reader(db, delimiter=';')
        contenido = []
        for line in f:
            contenido.append(line)
    return contenido
