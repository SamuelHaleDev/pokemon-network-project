def Logout(user, s, MAX_LINE):
    user_name = user[3]
    data = f"LOGOUT {user_name}\n"
    
    s.sendall(data.encode())
    data = s.recv(MAX_LINE)
    response = data.decode()
    
    if "200" in response:
        print("c: Logout successful.")
        return []
    else:
        print("c: Logout failed.")
        return user
    
__all__ = ["Logout"]