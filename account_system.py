import re #make it so the username is saved as key and qr code dedicated to that user and then save the user key in a different folder and the qr codes maybe
import bcrypt
import msvcrt
from compress import *
import time 
import pyotp 
import qrcode
import os
import secrets

def masked_input(prompt='Password: '):
    print(prompt, end='', flush=True)
    password = ''
    while True:
        char = msvcrt.getch().decode('utf-8')
        if char == '\r' or char == '\n':
            break
        elif char == '\b': #for backspace
            password = password[:-1]
            print('\b \b', end='', flush=True)
        else:
            password += char
            print('*', end='', flush=True)
    print()
    return password

def extract_lines(username, file_path):
    start_pattern = re.compile(r'---{}---'.format(re.escape(username)))
    end_pattern = re.compile(r'---\*end of {}\*---'.format(re.escape(username)))

    found_lines = []

    with open(file_path, 'r') as file:
        inside_block = False

        for line in file:
            if start_pattern.search(line):
                inside_block = True
            elif end_pattern.search(line):
                inside_block = False
                break

            if inside_block:
                found_lines.append(line.strip())

    return found_lines[1:] if found_lines and username in found_lines[0] else []

def account():
    try:
        with open('params.txt', 'r') as params:
            lines = params.readlines()
            key = lines[0].strip().replace('key=', '').replace('"', '')
            data_to_process = lines[1].strip().replace('file=', '').replace('"', '')
            unallowed = lines[2].strip().replace('unallowed=', '')
            file_path = lines[3].strip().replace('file_path=', '').replace('"', '')
            secret_key = lines[4].strip().replace('secret_key=', '').replace('"', '')
            ver = lines[5].strip().replace('ver=', '').replace('"', '')
            qr = lines[6].strip().replace('qr_code_path=f', '').replace('"', '')

        # if os.path.exists(ver):
        #     print("Key file exists")
        #     with open(ver,'r') as f_verify:
        #         contents = f_verify.read()
        # else:
        #     with open(ver,'w') as k:
        #         qr_key = k.write(pyotp.random_base32())
        #         contents = k.read()

        decry_decom(key, data_to_process)
        print("|------*Login*------|")
        username = input("Username: ")
        password = masked_input()

        if os.path.exists(f"{username}_key.key"):
            print("User key already exists")
        else:
            with open(f"{username}_key.key",'w') as user_key:
                user_key.write(pyotp.random_base32())

        bytes_password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(bytes_password, salt)

        lines = extract_lines(username, file_path)

        if lines and bcrypt.checkpw(bytes_password, lines[1].encode('utf-8')):
            print("Sign in successful")

            encry_compr(key, data_to_process)
            return

        sign_up = input('Account not found. Would you like to sign up using these credentials? (y/n): ').lower()

        if sign_up == 'y':
            with open(file_path, 'a') as sign:
                with open(file_path, 'r') as file:
                    for line in file:
                        if re.search(r'---{}---'.format(re.escape(username)), line):
                            print("Username is already in use\n")
                            if os.path.getsize(file_path) == 0:
                                return
                            else:
                                encry_compr(key, data_to_process)
                                return
                if len(username)-1 < 4 and len(password)-1 < 8:
                    print("Username must be more than 3 characters long and password must be 8 or more characters")
                    if os.path.getsize(file_path) == 0:
                        return
                    else:
                        encry_compr(key, data_to_process)
                        return
                elif len(username)-1 < 4 or len(username)-1 > 20:
                    print("Username must be more than 3 characters long")
                    if os.path.getsize(file_path) == 0:
                        return
                    else:
                        encry_compr(key, data_to_process)
                        return
                elif len(password)-1 < 4 or len(password)-1 > 20:
                    print("Password must be 8 or more characters")
                    if os.path.getsize(file_path) == 0:
                        return
                    else:
                        encry_compr(key, data_to_process)
                        return
                for char in username:
                    if char in unallowed:
                        print("Invalid character(s)")
                        if os.path.getsize(file_path) == 0:
                            return
                        else:
                            encry_compr(key, data_to_process)
                            return
                        
                with open(f"{username}_key.key",'r') as ver_key:
                    contents = ver_key.read()
                uri = pyotp.totp.TOTP(contents).provisioning_uri( 
                    name=username, 
                    issuer_name='GalacticCoder') 
                qrcode.make(uri).save(qr)
                totp = pyotp.TOTP(contents)
                verification = totp.verify(input(("Enter the Code : ")))

                if verification == True:
                    print("Verification sucessful")
                    if os.path.exists(qr):
                        os.remove(qr)
                else:
                    print("Verification unsucessful")
                    if os.path.exists(qr):
                        os.remove(qr)
                    return

                sign.write(f'---{username}---\n')
                sign.write(f'{username}\n')
                sign.write(f'{hash_password.decode("utf-8")}\n')
                sign.write(f'---*end of {username}*---\n')
                print("Sign up successful")

            if os.path.exists(qr):
                os.remove(qr)
            encry_compr(key, data_to_process)
        elif sign_up == 'n':
            if os.path.getsize(file_path) == 0:
                return
            else:
                encry_compr(key, data_to_process)
                return
        else:
            if os.path.getsize(file_path) == 0:
                print("Invalid option. Exiting")
                return
            else:
                print("Invalid option. Exiting")
                encry_compr(key, data_to_process)
                return
    except KeyboardInterrupt:
        if os.path.exists(qr):
            os.remove(qr)
        if os.path.getsize(file_path) == 0:
            print("Operation canceled by user")
            return
        else:
            print("Operation canceled by user")
            encry_compr(key, data_to_process)
            return
    except Exception as Error:
        if os.path.exists(qr):
            os.remove(qr)
        if os.path.getsize(file_path) == 0:
            print(Error)
            return
        else:
            print(Error)
            encry_compr(key, data_to_process)
            return

account()