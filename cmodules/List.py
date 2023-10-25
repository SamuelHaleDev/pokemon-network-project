import ast

def List(user, s, MAX_LINE, request_queue, response_queue):
    try:
        #  - BUILD CLIENT REQUEST
        print("c: LISTING ALL RECORDS IN POKEMON CARDS TABLE")
        client_request = "LIST"
        owner_id = user[3]
        client_request = client_request + " " + owner_id
        
        #  - SEND AND RECEIVE DATA
        request_queue.put(client_request)
        data = response_queue.get()
        response = ast.literal_eval(data)
        print(response)
    except Exception as e:
        print(f"c: An error occurred: {e}")
        print("c: List failed.")
        return
        
__all__ = ["List"]