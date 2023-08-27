import bcrypt
import time
import string
import secrets

pass_dic = {
    'og_pass': None,
    'r_new_pass': None
}


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def generate_strong_password(length=12):
    alphabet = string.ascii_letters
    digits = string.digits
    special_characters = string.punctuation
    all_characters = alphabet + digits + special_characters
    password = ''.join(secrets.choice(all_characters) for _ in range(length))
    return password


def save_in_db(pwd):
    print(f"Saved DataBase : {pwd}")
    return True


def change_pass(ogpwd, rpwd):
    return True


def acc_login(current_pwd, new_pwd):
    print("\n\n\n---------- Login Activity ----------")
    print('Logged In To Account')
    print(f'Looged In with : {current_pwd}')
    print(f'Pass Chnaged To : {new_pwd}')
    print('Logged Out From Account')
    print("---------- End Of Login Activity ----------\n\n\n")
    return True


def main():
    og_password = input("Enter Orignal Pass password  : ")
    og_hashed_password = hash_password(og_password)
    print("Orignal Hashed Password  :  ", og_hashed_password)
    save_in_db(og_hashed_password)
    rpwd = generate_strong_password()
    print(f"randomly Genrated Pass : {rpwd}")
    r_hashed_password = hash_password(rpwd)
    print("Random Genratd Password Hash : ", r_hashed_password)
    save_in_db(r_hashed_password)
    acc_login(og_password, rpwd)


if __name__ == "__main__":
    main()
