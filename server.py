import socket
from users import register


def server(host, port):
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    listening_socket.bind((host, port))
    listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    listening_socket.listen(5)

    print("starting server")

    while True:
        client_connection, client_address = listening_socket.accept()

        request_data = client_connection.recv(1024).decode()
        print("******************** start of request ****************")


        if request_data in ('', '\r\n'):
            client_connection.sendall(
                f"HTTP/1.1 200 OK\r\nContent-Length: {len('')}\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n''".encode()
            )
            client_connection.close()
            continue

        request_data_list = request_data.split("\r\n")

        method, url, http_version = request_data_list[0].split(" ")
        request_arg_dict = {}

        if "?" in url:
            request_args = url[url.index("?") + 1 :]
            for i in request_args.split("&"):
                key, value = i.split('=')
                request_arg_dict[key] = value



        print(f"request data: {request_data}")

        print(f"request arguments: {request_arg_dict}")
        print("******************End of request*******************")
        print()
        print()

        html_page = """
        <html>
            <head>
                <title>BookReview</title>
            </head>
            <body>
                <h1> User registration </h1>

                <form>
                    <label for="username">Username</label><br>
                    <input type="text" id="username", name="username"><br>

                    <label for="password1">Password1</label><br>
                    <input type="password" id="password1", name="password1"><br>

                    <label for="password2">Password1</label><br>
                    <input type="password" id="password2", name="password2"><br>

                    <label for="dateOfBirth">Date of birth</label><br>
                    <input type="date" id="dateOfBirth", name="dateOfBirth"><br>

                    <input type="submit" id="submit">
                </form>
            </body>
        </html>
        """

        response_status = "200 OK"

        if request_data.startswith("GET /?username") and request_arg_dict:
            dateOfBirth = request_arg_dict['dateOfBirth']

            year, month, day = dateOfBirth.split('-')
            date_of_birth = f"{day}/{month}/{year}"

            register_data = register(
                request_arg_dict['username'],
                request_arg_dict['password1'],
                request_arg_dict['password2'],
                date_of_birth)

            print(f"register data: {register_data}")

            response_status = "301 Moved Permanently\r\nLocation: /user/login"

        if request_data.startswith("GET /user/login"):
            html_page = """
                <html>
                    <body>
                        <h1> You have successfully registered </h1>
                    </body>
                </html>
            """

        client_connection.sendall(
            f"HTTP/1.1 {response_status}\r\nContent-Length: {len(html_page)}\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n{html_page}".encode()
        )
        client_connection.close()

        print("done serving request")
