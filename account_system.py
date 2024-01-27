import re #if an email is a temp email or not real then cancel account creation
import bcrypt
import msvcrt
from compress import encry_compr, decry_decom
import pyotp 
import qrcode
import os
import shutil
from email_sender import *
import socket
import http.server
import socketserver
import webbrowser
import requests
import json
import uuid
import hashlib
from passlib.hash import argon2
import argon2, binascii
from argon2 import PasswordHasher

sha512_hasher = hashlib.sha512()

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
    lines_between_patterns = []

    with open(file_path) as fp:
        inside_block = False
        
        for line in fp:
            if '---{}---'.format(username) in line:
                inside_block = True
            elif '---*end of {}*---'.format(username) in line:
                inside_block = False
            elif inside_block:
                lines_between_patterns.append(line.strip())

    return lines_between_patterns

def sign_up():
    try:
        global salt, sha512_hasher
        with open('params.txt', 'r') as params:
            lines = params.readlines()
            key = lines[0].strip().replace('key=', '').replace('"', '')
            unallowed = lines[2].strip().replace('unallowed=', '')
            file_path = lines[3].strip().replace('file_path=', '').replace('"', '')
            secret_key = lines[4].strip().replace('secret_key=', '').replace('"', '')
            qr = lines[6].strip().replace('qr_code_path=', '').replace('"', '')
            user_key_path = lines[7].strip().replace('tr_key=', '').replace('"', '')
            sendr_email = lines[8].strip().replace('sender_email=', '').replace('"', '')
            sendr_pass = lines[9].strip().replace('sender_pass=', '').replace('"', '')
            sub = lines[10].strip().replace('sub=', '').replace('"', '')
            msg = lines[11].strip().replace('msg=', '').replace('"', '')
        
        decry_decom(key, file_path)

        print("|------*Sign up*------|")
        username = input("Username: ").strip()
        password = masked_input().strip()
        email = input("Email(2fa)(only google emails allowed): ").strip()

        with open(f"{username}_key.key",'w') as user_key:
            user_key.write(pyotp.random_base32())
        
        shutil.move(f"{username}_key.key",user_key_path+f"\\{username}_key.key")
        
        # hostname = socket.gethostname()
        aa = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])
        
        bytes_password = password.encode('utf-8')
        bytes_aa = aa.encode('utf-8')
        bytes_email = email.encode("utf-8")
        
        sha512_hasher.update(bytes_aa)
        salt = bcrypt.gensalt(12)
        
        hash_password = bcrypt.hashpw(bytes_password, salt)
        hash_aa = sha512_hasher.hexdigest()
        
        lines = extract_lines(username, file_path)
        
        if lines and bcrypt.checkpw(bytes_password, lines[1].encode('utf-8')) and bytes_email == lines[2].encode('utf-8') and hash_aa == lines[3]:
            print("account found")
            encry_compr(key, file_path)
            return
        
        with open(file_path, 'a') as sign:
            with open(file_path, 'r') as file:
                find_e = file.readlines()
                for line in find_e:
                    if email in line:
                        print("Email is already in use.")
                        os.remove(user_key_path+f'\\{username}_key.key')
                        encry_compr(key, file_path)
                        return
                for line in find_e:
                    if re.search(r'---{}---'.format(re.escape(username)), line) and os.path.exists(user_key_path+f'\\{username}_key.key') and os.path.exists(qr+f'\\{username}_qr.png'):
                        print("Username is already in use\n")
                        if os.path.getsize(file_path) == 0:
                            return
                        else:
                            encry_compr(key, file_path)
                            return
                        
            if email[-10:] != '@gmail.com':
                print("invalid email format")
                os.remove(user_key_path+f"\\{username}_key.key")
                if os.path.getsize(file_path) == 0:
                    return
                else:
                    encry_compr(key, file_path)
                    return
            # response = requests.get(f"https://emailvalidation.abstractapi.com/v1/?api_key=d2cc1e7dc7c64f78b66ed5b843cc5689&email={email}")
            # result_dict = json.loads(response.content.decode('utf-8'))

            # print(result_dict)
            # print(response.status_code)
                                
            elif len(username)-1 < 4 or len(username)-1 > 20:
                print("Username must be more than 3 characters long")
                os.remove(user_key_path+f"\\{username}_key.key")
                if os.path.getsize(file_path) == 0:
                    return
                else:
                    encry_compr(key, file_path)
                    return
        
            elif len(username)-1 < 4 and len(password)-1 < 8:
                print("Username must be more than 3 characters long and password must be 8 or more characters")
                os.remove(user_key_path+f"\\{username}_key.key")
                if os.path.getsize(file_path) == 0:
                    return
                else:
                    encry_compr(key, file_path)
                    return
                
            elif len(password)-1 < 4 or len(password)-1 > 20:
                print("Password must be 8 or more characters")
                os.remove(user_key_path+f"\\{username}_key.key")
                if os.path.getsize(file_path) == 0:
                    return
                else:
                    encry_compr(key, file_path)
                    return
                
            for char in username:
                if char in unallowed:
                    print("Invalid character(s)")
                    os.remove(user_key_path+f"\\{username}_key.key")
                    if os.path.getsize(file_path) == 0:
                        return
                    else:
                        encry_compr(key, file_path)
                        return

            with open(f"{user_key_path}\\{username}_key.key",'r') as ver_key:
                contents = ver_key.read()
                
                uri = pyotp.totp.TOTP(contents, digest=hashlib.sha512).provisioning_uri( 
                name=username, 
                issuer_name='GalacticCoder')
                qrcode.make(uri).save(qr+f"\\{username}_qr.png")

                sign.write(f'---{username}---\n')
                sign.write(f'{username}\n')
                sign.write(f'{hash_password.decode("utf-8")}\n')
                sign.write(f'{email}\n')
                sign.write(f'{hash_aa}\n')
                sign.write(f'---*end of {username}*---\n')

                print("Sign up successful")

        encry_compr(key, file_path)

    except KeyboardInterrupt:
        if os.path.getsize(file_path) == 0:
            print("\nOperation canceled by user")
            return
        else:
            print("Operation canceled by user")
            encry_compr(key, file_path)
            return
    except Exception as Error:
        os.remove(user_key_path+f"\\{username}_key.key")
        if os.path.getsize(file_path) == 0:
            print(Error)
            return
        else:
            print(Error)
            encry_compr(key, file_path)
            return

def sign_in():
    try:
        with open('params.txt', 'r') as params:
            lines = params.readlines()
            key = lines[0].strip().replace('key=', '').replace('"', '')
            unallowed = lines[2].strip().replace('unallowed=', '')
            file_path = lines[3].strip().replace('file_path=', '').replace('"', '')
            secret_key = lines[4].strip().replace('secret_key=', '').replace('"', '')
            qr = lines[6].strip().replace('qr_code_path=', '').replace('"', '')
            user_key_path = lines[7].strip().replace('tr_key=', '').replace('"', '')
            sendr_email = lines[8].strip().replace('sender_email=', '').replace('"', '')
            sendr_pass = lines[9].strip().replace('sender_pass=', '').replace('"', '')
            sub = lines[10].strip().replace('sub=', '').replace('"', '')
            msg = lines[11].strip().replace('msg=', '').replace('"', '')

        decry_decom(key, file_path)

        print("|------*Login*------|")
        username = input("Username: ").strip()
        password = masked_input().strip()
        email = input("Email(2fa)(only google emails allowed): ").strip()
        
        aa = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])
        
        bytes_email = email.encode('utf-8')
        bytes_password = password.encode('utf-8')
        bytes_aa = aa.encode('utf-8')
        
        sha512_hasher.update(bytes_aa)
        hash_aa = sha512_hasher.hexdigest()
        
        lines = extract_lines(username, file_path)
        
        if lines and bcrypt.checkpw(bytes_password, lines[1].encode('utf-8')) and bytes_email == lines[2].encode('utf-8') and hash_aa == lines[3]:
            print("account found")
            encry_compr(key, file_path)
            return
        
        elif lines and bcrypt.checkpw(bytes_password, lines[1].encode('utf-8')) and bytes_email == lines[2].encode('utf-8') and hash_aa != lines[3]:                            
            if os.path.exists(user_key_path+f'\\{username}_key.key'):
                print("account found but your signing in from a different location need verification")
                
                with open(user_key_path+f'\\{username}_key.key', 'r') as user_key_file:
                    user_key = user_key_file.read().strip()

                    totp = pyotp.TOTP(user_key)
                    send_email(sendr_email, sendr_pass, email, sub, msg, attachment_path=qr+f'\\{username}_qr.png')
                    print(totp.now())
                    user_input_otp = input("Enter the OTP: ")
                    is_valid = totp.verify(user_input_otp)#verificication errors fixed
                    
                    if is_valid:
                        print("verification successful")#make something where it can access after succeful verification
                    else:
                        print("verification unsuccessful")
                        encry_compr(key, file_path)
                        return
        
        else:
            ask = input("Account not found. Would you like to sign up instead using these credentials? (y/n): ").lower()
            if ask == "y":
                os.remove(user_key_path+f'\\{username}_key.key')
                sign_up() #use sign up function
            if ask == 'n':
                encry_compr(key, file_path)
                return
            
    except KeyboardInterrupt:
        if os.path.getsize(file_path) == 0:
            print("\nOperation canceled by user")
            return
        else:
            print("Operation canceled by user")
            encry_compr(key, file_path)
            return
    except Exception as Error:
        print("unexpected error occured")
        if os.path.getsize(file_path) == 0:
            print(Error)
            return
        else:
            print(Error)
            encry_compr(key, file_path)
            return
        
try:
    option = input("Sign in or Sign up?(sg/su): ").lower()

    if option == 'su':
        sign_up()

    elif option == 'sg':
        sign_in()
        
    else:
        print("not an option")
except KeyboardInterrupt:
    print("User canceled operation")
    exit
    
    