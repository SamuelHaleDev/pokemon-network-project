import ast

def Who(s, MAX_LINE, request_queue, response_queue):
    try:
        request = f"WHO\n"
        request_queue.put(request)
        response = ast.literal_eval(response_queue.get())
        if "400" in response or "401" in response or "404" in response:
            print("c: WHO failed.")
        else:
            print(f"The list of active users: {response}")
    except Exception as e:
        print(f"c: An error occurred: {e}")
        print("c: WHO failed.")
        return
        
__all__ = ["Who"]