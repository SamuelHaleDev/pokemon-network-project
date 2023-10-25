def Who(s, MAX_LINE, request_queue, response_queue):
    request = f"WHO\n"
    request_queue.put(request)
    response = response_queue.get()
    if "400" in response or "401" in response or "404" in response:
        print("c: WHO failed.")
    else:
        print(f"The list of active users: {response}")
        
__all__ = ["Who"]