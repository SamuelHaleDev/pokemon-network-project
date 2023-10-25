def handle_request(s, request_queue):
    while True:
        request = request_queue.get()
        s.sendall(request.encode())
        if "QUIT" in request:
            break
        