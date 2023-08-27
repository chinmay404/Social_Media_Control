import bcrypt
import string
import json
import secrets
import datetime
from cryptography.fernet import Fernet
from insta_login import login, change_pass
from colorama import Fore, init

# addition_control_project_test
# sirius1718
init(autoreset=True)
# wvZrj7AGrcWMPp1i90tUTHWmHkhyA5IqjbUSgxvh0_4=

# ACTIONS


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


def encrypt_data(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data


def display_centered(text):
    cols = 80
    padding = (cols - len(text)) // 2
    return ' ' * padding + text

# ACTIONS END


def lock():
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    time_choice = int(input("Select Lock Time:\n1. Days\n2. Minutes\n"))

    if time_choice == 1:
        days = int(input("Enter the number of days: "))
        if days == 0:
            print(Fore.RED + 'Days Cannot Be 0')
            days = int(input("Enter the number of days: "))
        unlock_time = datetime.datetime.now() + datetime.timedelta(days=days)
    elif time_choice == 2:
        minutes = int(input("Enter the number of minutes: "))
        if minutes == 0:
            print(Fore.RED + 'Minutes Cannot Be 0')
            minutes = int(input("Enter the number of minutes: "))
        unlock_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
    else:
        print(Fore.RED + 'Invalid time choice')
        return

    new_pass = generate_random_password()

    if new_pass == username:
        print(Fore.RED + "Password cannot be the same as the username.")
        return

    if not new_pass:
        print(Fore.RED + "Password cannot be empty.")
        return

    # Simulate Login and Change Process
    print(Fore.YELLOW + 'Logging into Instagram...')
    login(username, password, new_pass)
    # Complete Login Process

    hashed_pass = hash_password(password=password)
    lock_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        'username': username,
        'og_pass': password,
        'new_pass': new_pass,
        'lock_date': lock_date,
        'unlock_date': unlock_time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    # Lock Data With Encryption And Give Key To user
    encryption_key = Fernet.generate_key()
    encrypted_data = encrypt_data(json.dumps(data), encryption_key)

    with open(f'{username}.enc', 'wb') as file:
        file.write(encrypted_data)

    with open(f'{username}.txt', 'wb') as key_file:
        key_file.write(encryption_key)

    print(Fore.GREEN + 'Account locked and encrypted data stored. Here is your encryption key:')
    print(encryption_key.decode())  # Convert bytes to string for display


def unlock():
    username = input("Enter Username: ")
    encryption_key = input("Enter Encryption Key: ").encode()

    try:
        with open(f'{username}.enc', 'rb') as file:
            encrypted_data = file.read()
    except FileNotFoundError:
        print(Fore.RED + f"Account data for {username} not found.")
        return

    decrypted_data = decrypt_data(encrypted_data, encryption_key)
    account_data = json.loads(decrypted_data)

    unlock_date_str = account_data['unlock_date']
    unlock_date = datetime.datetime.strptime(
        unlock_date_str, "%Y-%m-%d %H:%M:%S")

    current_date = datetime.datetime.now()

    if current_date >= unlock_date:
        print(Fore.GREEN + display_centered('Congratulations! You have completed the locked period.'))
        print(display_centered("Account Data:"))
        print(display_centered(f"Username: {account_data['username']}"))
        # print(f"Original Password: {account_data['og_pass']}")
        print(display_centered(f"New Password: {account_data['new_pass']}"))
        print(display_centered(f"Lock Date: {account_data['lock_date']}"))
        print(display_centered(f"Unlock Date: {account_data['unlock_date']}"))
        change_to_pass = input(Fore.YELLOW + 'Enter new Pass To change: ')
        login(account_data['username'],
              account_data['new_pass'], change_to_pass)
    else:
        time_left = unlock_date - current_date
        total_seconds = time_left.total_seconds()
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        print(Fore.RED + display_centered(
            f'Not Allowed Time! Time remaining: {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds\n'))


def main():
    print(Fore.CYAN + display_centered("Welcome to the Account Locking System!"))
    action = int(input(display_centered('1. Lock  2. Unlock\n')))
    if action == 1:
        lock()
    elif action == 2:
        unlock()
    else:
        print(Fore.RED + display_centered('Invalid Choice'))


if __name__ == '__main__':
    main()
