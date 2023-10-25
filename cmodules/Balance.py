def Balance(user, s, MAX_LINE, request_queue, response_queue):
    #User Checks their balance
    userID = user[0]
    money = "BALANCE " + userID
    request_queue.put(money)
    money = str(response_queue.get())
    money = money.split("'")[1]
    balance = ""
    for c in money: 
            if c.isdigit() or (c == '.'): 
                balance = balance + c

    print(balance)
    
__all__ = ["Balance"]