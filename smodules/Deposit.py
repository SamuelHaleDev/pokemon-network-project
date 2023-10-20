def Deposit(cur, con, data, addr):
    print('s: Received DEPOSIT command from', addr)
    # data will be 'DEPOSIT <amount>'
    # parse data
    data = data.decode()
    data = data.split(' ')
    amount = data[1]
    user = data [2]
    user = user.replace('\n', '')
    
    cur.execute("UPDATE users SET usd_balance = usd_balance + ? WHERE user_name = ?", (amount, user))
    con.commit()
    
    # Check if the deposit was successful
    cur.execute(f"SELECT usd_balance FROM users WHERE user_name = ?", (user,))
    balance = cur.fetchone()
    balance = balance[0]
    
    if balance == None:
        return "400 ERROR"
    else:
        return "200 OK"
    
__all__ = ["Deposit"]