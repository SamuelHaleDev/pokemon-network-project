def Logout(user, s, MAX_LINE, request_queue, response_queue):
    try:
        user_name = user[3]
        data = f"LOGOUT {user_name}\n"
        
        request_queue.put(data)
        data = response_queue.get()
        
        if "200" in data:
            print("c: Logout successful.")
            return []
        else:
            print("c: Logout failed.")
            return user
    except Exception as e:
        print(f"c: An error occurred: {e}")
        print("c: Logout failed.")
        return user
    
__all__ = ["Logout"]