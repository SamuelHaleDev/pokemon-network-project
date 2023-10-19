from c import MAX_LINE

def List(user, s):
    #  - BUILD CLIENT REQUEST
    print("c: LISTING ALL RECORDS IN POKEMON CARDS TABLE")
    client_request = "LIST"
    owner_id = user[3]
    client_request = client_request + " " + owner_id
    
    #  - SEND AND RECEIVE DATA
    s.sendall(client_request.encode())
    data = s.recv(MAX_LINE)
    if b"200 OK" in data:
        response = data.decode().split("|")[1].strip()
        print(response)
        
__all__ = ["List"]