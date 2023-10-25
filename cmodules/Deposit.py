def Deposit(user, s, MAX_LINE, request_queue, response_queue):
    dep_amount = -1
    while dep_amount < 0:
        try:
            dep_amount = int(input("Enter amount to deposit: "))
        except ValueError:
            print("Invalid amount.")
    request = f"DEPOSIT {dep_amount} {user[3]}\n"
    request_queue.put(request)
    response = s.recv(MAX_LINE)
    response = response.decode()
    if "200" in response:
        print("Deposit successful.")
    else:
        print("Deposit failed.")
__all__ = ["Deposit"]