def Deposit(user, s, MAX_LINE):
    dep_amount = -1
    while dep_amount < 0:
        try:
            dep_amount = int(input("Enter amount to deposit: "))
        except ValueError:
            print("Invalid amount.")
    request = f"DEPOSIT {dep_amount}\n"
    s.sendall(request.encode())
    response = s.recv(MAX_LINE)
    response = response.decode()
    if "200" in response:
        print("Deposit successful.")
    else:
        print("Deposit failed.")
__all__ = ["Deposit"]