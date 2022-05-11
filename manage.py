import argparse
import sys
from users import login, register

if __name__ == '__main__':
    """ You can put your testing logic here """
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('action',
                       metavar='action',
                       type=str,
                       help='the path to list')
    my_parser.add_argument('--username', action='store', type=str, required=True)
    my_parser.add_argument('--password', action='store', type=str, required=True)

    if len(sys.argv) >= 2 and sys.argv[1] == "user_register":
        my_parser.add_argument('--password2', action='store', type=str, required=True)
        my_parser.add_argument('--dateOfBirth', action='store', type=str, required=True)

    args = my_parser.parse_args()

    if args.action == "user_register":
        print(register(args.username, args.password, args.password2, args.dateOfBirth))
    else:
        print(login(args.username, args.password))
