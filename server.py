from http.server import BaseHTTPRequestHandler, HTTPServer

# code borrowed from https://www.geeksforgeeks.org/building-a-basic-http-server-from-scratch-in-python/
class BasicServer(BaseHTTPRequestHandler):

    # creating a function for Get Request
    def do_GET(self):

        # Success Response --> 200
        self.send_response(200)

        # Type of file that we are using for creating our
        # web server.
        self.send_header('content-type', 'text/html')
        self.end_headers()

        # what we write in this function it gets visible on our
        # web-server
        self.wfile.write(
            """
            <html>
                <head>
                   <title>BookReview</title>
                </head>
                <body>
                    <h1>Hello world</h1>
                </body>
            </html>
            """.encode()
        )

def server(host, port):
    """
    Write code that starts server on host proviced and port. 
    """
    port = HTTPServer((host, port), BasicServer)

    # this is used for running our
    # server as long as we wish
    # i.e. forever
    port.serve_forever()
