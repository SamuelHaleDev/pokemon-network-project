from c import MAX_LINE

def BALANCE(user, s):
    #User Checks their balance
    userID = user[0]
    money = "BALANCE " + userID
    s.sendall(money.encode())
    money = str(s.recv(MAX_LINE))
    money = money.split("'")[1]
    balance = ""
    for c in money: 
            if c.isdigit() or (c == '.'): 
                balance = balance + c

    print(balance)
    
__all__ = ["BALANCE"]