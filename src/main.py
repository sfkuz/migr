# ниц не должен знать про sql
from typing import List
from datetime import datetime

# Импорт сервиса, схем и кастомных ошибок
from lib.services.user_se import user_service
from lib.schemas.user_she import User, UserCreate, UserUpdate
from lib.repository.user_re import UserAlreadyExistsError


def print_users(users: List[User]):
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


def menu():
    while True:
        print("\n=== User Management Menu ===")
        print("1. Add User")
        print("2. Read User")
        print("3. Update User")
        print("4. Delete User")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == '1':
                name = input("Enter user name: ").strip()
                email = input("Enter user email: ").strip()
                age = input("Enter age (optional): ").strip()
                age = int(age) if age else None

                user_data = UserCreate(name=name, email=email, age=age)
                new_user = user_service.add_user(user_data)
                print(f"User '{new_user.name}' with ID {new_user.id} was successfully created.")


            elif choice == '2':

                user_id_input = input("Enter user ID (leave blank to search by name or show all): ").strip()
                name_input = None
                user_id = None
                if user_id_input:
                    user_id = int(user_id_input)
                else:
                    name_input = input("Enter user name to search (leave blank to show all users): ").strip()
                    if not name_input:
                        users = user_service.read_user(None, None)
                        print_users(users)
                        continue
                users = user_service.read_user(user_id, name=name_input)

                print_users(users)

            elif choice == '3':
                user_id = int(input("Enter user ID to update: ").strip())
                new_name = input("Enter new name (leave blank to skip): ").strip() or None
                new_email = input("Enter new email (leave blank to skip): ").strip() or None
                is_active_input = input("Is active? (true/false, leave blank to skip): ").strip()
                is_active = None
                if is_active_input.lower() in ('true', 'false'):
                    is_active = is_active_input.lower() == 'true'
                age_input = input("Enter new age (leave blank to skip): ").strip()
                age = int(age_input) if age_input else None

                updated_data = UserUpdate(name=new_name, email=new_email, is_active=is_active, age=age)
                updated_user = user_service.update_user(user_id, updated_data)
                if updated_user:
                    print(f"User with ID {updated_user.id} was successfully updated:")
                    print_users([updated_user])
                else:
                    print(f"User with ID {user_id} not found or no new data provided.")

            elif choice == '4':
                user_id = int(input("Enter user ID to delete: ").strip())
                success = user_service.delete_user(user_id)
                if success:
                    print(f"User with ID {user_id} successfully deleted.")
                else:
                    print(f"User with ID {user_id} not found.")

            elif choice == '5':
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

        except UserAlreadyExistsError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    menu()
