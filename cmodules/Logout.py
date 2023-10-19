def Logout(user, s, MAX_LINE):
    user_name = user[3]
    request = f"LOGOUT {user_name}\n"
    
    s.sendall(request.encode())
    response = request.decode()
    
    if "200" in response:
        print("c: Logout successful.")
        return []
    else:
        print("c: Logout failed.")
        return user
    
__all__ = ["Logout"]