import socket


def server(host, port):
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    listening_socket.bind((host, port))
    listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    listening_socket.listen(5)

    print("starting server")

    while True:
        client_connection, client_address = listening_socket.accept()

        request_data = client_connection.recv(1024)

        print(f"request data: {request_data.decode()}")

        html_page = """
        <html>
            <head>
                <title>BookReview</title>
            </head>
            <body>
                <h1> Hello world </h1>
            </body>
        </html>
        """

        client_connection.sendall(
            f"HTTP/1.1 200 OK\r\nContent-Length: {len(html_page)}\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n{html_page}".encode()
        )
        client_connection.close()

        print("done serving request")
