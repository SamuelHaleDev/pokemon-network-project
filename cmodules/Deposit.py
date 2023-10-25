def Deposit(user, s, MAX_LINE, request_queue, response_queue):
    try:
        dep_amount = -1
        while dep_amount < 0:
            try:
                dep_amount = int(input("Enter amount to deposit: "))
            except ValueError:
                print("Invalid amount.")
        request = f"DEPOSIT {dep_amount} {user[3]}\n"
        request_queue.put(request)
        response = response_queue.get()
        if "200" in response:
            print("Deposit successful.")
        else:
            print("Deposit failed.")
    except Exception as e:
        print(f"c: An error occurred: {e}")
        print("c: Deposit failed.")
        return
__all__ = ["Deposit"]