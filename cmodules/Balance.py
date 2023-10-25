def Balance(user, s, MAX_LINE, request_queue):
    #User Checks their balance
    userID = user[0]
    money = "BALANCE " + userID
    request_queue.put(money)
    money = str(s.recv(MAX_LINE))
    money = money.split("'")[1]
    balance = ""
    for c in money: 
            if c.isdigit() or (c == '.'): 
                balance = balance + c

    print(balance)
    
__all__ = ["Balance"]