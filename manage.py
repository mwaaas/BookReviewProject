import argparse
import sys
from users import login, register
from server import server

if __name__ == '__main__':
    """ You can put your testing logic here """
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(help="Sub commands", dest="action")

    # registration command configuration
    user_register_parser = subparser.add_parser("user_register", help="Command for registering user")
    user_register_parser.add_argument('--username', action='store', type=str, required=True, help="username to use for registration")
    user_register_parser.add_argument('--password', action='store', type=str, required=True, help="password to use for registraion")
    user_register_parser.add_argument('--password2', action='store', type=str, required=True, help="password matching password one")
    user_register_parser.add_argument('--dateOfBirth', action='store', type=str, required=True, help="date of birth to use for registration")

    # login command configuration
    user_login_parser = subparser.add_parser("user_login", help="Command for user login")
    user_login_parser.add_argument('--username', action='store', type=str, required=True, help="username to use for login")
    user_login_parser.add_argument('--password', action='store', type=str, required=True, help="password to use for login")

    # server command configuration
    run_server_parser = subparser.add_parser("run_server", help="Command for running server")
    run_server_parser.add_argument('--host', action='store', type=str, required=False, default='localhost', help='host address server to bind to')
    run_server_parser.add_argument('--port', action='store', type=int, required=False, default=5050, help='port server to bind to.')

    args = parser.parse_args()

    if args.action == "user_register":
        print(register(args.username, args.password, args.password2, args.dateOfBirth))
    elif args.action == "user_login":
        print(login(args.username, args.password))
    elif args.action == "run_server":
        server(args.host, args.port)
