from csv import writer, reader, QUOTE_MINIMAL

DB_ROUTE = './db'
try:
    with open(DB_ROUTE, 'x', newline='\n'):
        pass
except:
    pass

def user_exists(username):
    with open(DB_ROUTE, 'r', newline='\n') as db:
        read = reader(db, delimiter=';')
        for row in read:
            if row[0] == username:
                return True, row
    return False, None

def user_create(username, password):
    with open(DB_ROUTE, 'a', newline='\n') as db:
        write = writer(db, delimiter=';', quoting=QUOTE_MINIMAL)
        write.writerow((username, password))