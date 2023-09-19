import socket
import sqlite3

con = sqlite3.connect("Pokemon.db") # Connect to database

cur = con.cursor() # Create cursor object

# Create tables
cur.execute("CREATE TABLE IF NOT EXISTS Users(ID INTEGER PRIMARY KEY AUTOINCREMENT, first_name Text, last_name Text, user_name Text NOT NULL, password Text, usd_balance DOUBLE NOT NULL)")
cur.execute("CREATE TABLE IF NOT EXISTS Pokemon_cards(ID INTEGER PRIMARY KEY AUTOINCREMENT, card_name TEXT NOT NULL, card_type TEXT NOT NULL, rarity TEXT NOT NULL, count INTEGER, owner_id INTEGER, FOREIGN KEY (owner_id) REFERENCES Users(ID))")

# Insert data into tables
user_data = [ 
    ("John", "Doe", "j_doe", "Passwrd4", 80),
    ("Jane", "Smith", "j_smith", "Pass456", 10),
    ("charlie", "brown", "c_brown", "Snoopy", 90),
    ("lucy", "van", "l_van", "Football", 70),
    ("linus", "blanket", "l_blanket", "security23", 90),
    ]

card_data = [ 
    ("Pikachu", "Electric", "Common", 2, 1),
    ("Charizard", "Fire", "Rare", 1, 1),
    ("Balbasaur", "Grass", "Common", 50, 3),
    ("Squirtle", "Water", "Uncommon", 30, 4),
    ("Jigglypuff", "Normal", "Common", 3, 5),
    ]


cur.executemany("INSERT OR IGNORE INTO Users(first_name, last_name, user_name, password, usd_balance) VALUES (?, ?, ?, ?, ?)", user_data)
con.commit()

cur.executemany("INSERT OR IGNORE INTO Pokemon_cards(card_name, card_type, rarity, count, owner_id) VALUES (?, ?, ?, ?, ?)", card_data)
con.commit()

# Define server port
PORT = 4895 # Port number is a 16-bit unsigned integer
MAX_PENDING = 5 # Maximum number of pending connections
MAX_LINE = 256 # Maximum number of bytes to receive

# Passive open
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
s.bind(('', PORT)) # Bind the socket to the port
s.listen(MAX_PENDING) # Listen for connection

# Wait for connection
while True:
    conn, addr = s.accept() # Accept a connection
    print('s: Connected by', addr) # Print client address

    while True:
        data = conn.recv(MAX_LINE) # Receive data from client
        if not data: break # Break if no more data

        if "QUERY" in data.decode():
            print('s: Received', repr(data), 'from', addr)
            
            #  - GET CARD DATA
            card_name = data.decode().split(" ")[1]
            cur.execute("SELECT * FROM Pokemon_cards WHERE card_name = ?", (card_name,))
            results = cur.fetchall()
            
            #  - SEND CARD DATA OR ERROR MESSAGE
            if len(results) == 0:
                data = b"s: Card does not exist."
            else:
                data = str(results[0]).encode()
        if "LOGIN" in data.decode():
            print('s: Received', repr(data), 'from', addr)
            #  - GET USERNAME AND PASSWORD
            username = data.decode().split(" ")[1]
            password = data.decode().split(" ")[2]
            
            #  - CHECK IF USERNAME AND PASSWORD ARE CORRECT
            cur.execute("SELECT * FROM Users WHERE user_name = ? AND password = ?", (username, password))
            results = cur.fetchall()
            if len(results) == 0:
                data = b"s: 401: Username or password is incorrect."
            else:
                #  - SEND USER DATA
                server_response = b"s: 200: Login successful.|"
                user_data = str(results[0]).encode()
                data = f"{server_response}{user_data}".encode()
        if "BUY" in data.decode():
            #  - GRAB CLIENT REQUEST
            client_request = data.decode().replace("BUY ", "").split(" ")
            print("s: RECEIVED {}".format(client_request))
            
            #  - GRAB CARD DATA
            card_name = data.decode().split(" ")[1]
            cur.execute("SELECT * FROM Pokemon_cards WHERE card_name = ?", (card_name,))
            results = cur.fetchall()
            
            #  - CHECK IF CARD EXISTS. IF NOT, SEND ERROR MESSAGE
            if len(results) == 0:
                data = b"s: 403: Card does not exist."
            else:
                #  - CHECK IF USER IS BUYING ALL CARDS. IF SO, UPDATE OWNER_ID. 
                if int(client_request[3]) == int(results[0][4]):
                    cur.execute("UPDATE Pokemon_cards SET owner_id = ? WHERE card_name = ?", (int(client_request[5]), card_name))
                else:
                    #  - IF NOT, UPDATE COUNT AND ADD NEW ROW
                    cur.execute("UPDATE Pokemon_cards SET count = ? WHERE card_name = ?"
                                , (int(results[0][4]) - int(client_request[3]), card_name))
                    cur.execute("INSERT INTO Pokemon_cards(card_name, card_type, rarity, count, owner_id) VALUES (?, ?, ?, ?, ?)"
                                , (card_name, results[0][2], results[0][3], int(results[0][4])-int(client_request[3]), int(client_request[5])))
                #  - GRAB AND UPDATE USER BALANCE
                cur.execute("SELECT * FROM Users WHERE ID = ?", (int(client_request[5]),))
                balance = cur.fetchall()
                balance = float(balance[0][5])
                cur.execute("UPDATE Users SET usd_balance = ? WHERE ID = ?", (
                    float(balance) - int(client_request[3])*float(client_request[2]), int(client_request[5])))
                con.commit()
                
                #  - GRAB NEW BALANCE
                cur.execute("SELECT * FROM Users WHERE ID = ?", (int(client_request[5]),))
                balance = cur.fetchall()
                
                #  - SEND SUCCESS MESSAGE WITH NEW BALANCE
                data = f"200 OK|{balance[0][5]}".encode()
        conn.sendall(data) # Send data back to client

    # Close the connection
    conn.close()
    
    



    