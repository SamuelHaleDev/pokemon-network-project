def handle_request(s, request_queue):
    while True:
        request = request_queue.get()
        if request == "QUIT" or request ==  "SHUTDOWN":
            break
        s.sendall(request.encode())
        