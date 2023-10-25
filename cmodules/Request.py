def handle_request(s, request_queue):
    while True:
        try:
            request = request_queue.get()
            s.sendall(request.encode())
            if "QUIT" in request:
                break
            if "SHUTDOWN" in request:
                break
        except Exception as e:
            print(f"c: handle_request: An error occurred: {e}")
            break
        