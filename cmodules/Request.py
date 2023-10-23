def handle_request(s, request_queue):
    while True:
        request = request_queue.get()
        if request == "QUIT" or "SHUTDOWN":
            break
        print("f: Handling request: {}".format(request))
        s.sendall(request.encode())
        