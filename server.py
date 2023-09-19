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

    # Receive data and send it back
    while True:
        data = conn.recv(MAX_LINE) # Receive data from client
        if not data: break # Break if no more data
        # Print the received data and client address
        print('s: Received', repr(data), 'from', addr)
        # Check if "QUERY" is in the data
        if "QUERY" in data.decode():
            # If "QUERY" is in the data, query for card name
            card_name = data.decode().split(" ")[1]
            cur.execute("SELECT * FROM Pokemon_cards WHERE card_name = ?", (card_name,))
            # Fetch the results
            results = cur.fetchall()
            # Check if results is empty
            if len(results) == 0:
                # If results is empty, send error message to client
                data = b"s: Card does not exist."
            else:
                # If results is not empty, send card information to client
                data = str(results[0]).encode()
        conn.sendall(data) # Send data back to client

    # Close the connection
    conn.close()
    
    



    