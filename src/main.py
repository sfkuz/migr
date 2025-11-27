# ниц не должен знать про sql

import argparse
from typing import List

# Импорт сервиса, схем и кастомных ошибок
from lib.services.user_se import user_service
from lib.schemas.user_she import User, UserCreate, UserUpdate
from lib.repository.user_re import UserAlreadyExistsError


def print_users(users: List[User]):   # красивенький вывод
    if not users:
        print("Users not found.")
        return

    print(f"{'ID':<5}{'NAME':<20}{'EMAIL':<30}{'AGE':<5}{'ACTIVE':<10}{'CREATED AT':<20}")
    print('-' * 90)
    for user in users:
        age_display = user.age if user.age is not None else ''
        created_at_display = user.created_at.strftime('%Y-%m-%d %H:%M')
        print(f"{user.id:<5}{user.name:<20}{user.email:<30}{str(age_display):<5}"
              f"{str(user.is_active):<10}{created_at_display:<20}")

def main():
    parser = argparse.ArgumentParser(description='Database manipulation')
    subparsers = parser.add_subparsers(dest='command', help='available commands')

    # add
    parser_add = subparsers.add_parser('add', help='add a new user')
    parser_add.add_argument('--name', type=str, required=True, help='user name')
    parser_add.add_argument('--email', type=str, required=True, help='email address')
    parser_add.add_argument('--age', type=int, help='age user')

    # read
    parser_get = subparsers.add_parser('read', help='read a user')
    parser_get.add_argument('--id', type=int, help='ID user to read')
    parser_get.add_argument('--name', type=str, help='user name to read')

    # update
    parser_update = subparsers.add_parser('update', help='update a user')
    parser_update.add_argument('--id', type=int, required=True, help='ID user to update')
    parser_update.add_argument('--new-name', type=str, help='new user name')
    parser_update.add_argument('--new-email', type=str, help='new email')
    parser_update.add_argument('--is-active', type=lambda x: (str(x).lower() == 'true'),
                               help='status active (true/false)')
    parser_update.add_argument('--age', type=int, help='new age')

    # delete
    parser_delete = subparsers.add_parser('delete', help='delete a user')
    parser_delete.add_argument('--id', type=int, required=True, help='ID user to delete')

    args = parser.parse_args()

    try:
        if args.command == 'add':
            user_data = UserCreate(name=args.name, email=args.email, age=args.age)
            new_user = user_service.add_user(user_data)
            print(f"User '{new_user.name}' with ID {new_user.id} was successfully created.")

        elif args.command == 'read':
            user = user_service.read_user(args.id, name=args.name)
            print_users(user)

        elif args.command == 'update':
            updated_data = UserUpdate(name=args.new_name, email=args.new_email, is_active=args.is_active, age=args.age)
            updated_user = user_service.update_user(args.id, updated_data)
            if updated_user:
                print(f"User with ID {updated_user.id} was successfully updated:")
                print_users([updated_user])
            else:
                print(f"User with ID {args.id} not found or no new data provided.")

        elif args.command == 'delete':
            success = user_service.delete_user(args.id)
            if success:
                print(f"User with ID {args.id} successfully deleted.")
            else:
                print(f"User with ID {args.id} not found.")

    except UserAlreadyExistsError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()
