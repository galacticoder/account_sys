import re #getting an error when sending email, fix it
import bcrypt
import msvcrt
from compress import encry_compr, decry_decom
import pyotp 
import qrcode
import os
import shutil
from email_sender import *

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

    if found_lines and username in found_lines[0]:
        return found_lines[1:3] if len(found_lines) >= 3 else []
    else:
        return []

def account():
    try:
        with open('params.txt', 'r') as params:
            lines = params.readlines()
            key = lines[0].strip().replace('key=', '').replace('"', '')
            unallowed = lines[2].strip().replace('unallowed=', '')
            file_path = lines[3].strip().replace('file_path=', '').replace('"', '')
            secret_key = lines[4].strip().replace('secret_key=', '').replace('"', '')
            ver = lines[5].strip().replace('ver=', '').replace('"', '')
            qr = lines[6].strip().replace('qr_code_path=', '').replace('"', '')
            user_key_path = lines[7].strip().replace('tr_key=', '').replace('"', '')
            sendr_email = lines[8].strip().replace('sender_email=', '').replace('"', '')
            sendr_pass = lines[9].strip().replace('sender_pass=', '').replace('"', '')
            sub = lines[10].strip().replace('sub=', '').replace('"', '')
            msg = lines[11].strip().replace('msg=', '').replace('"', '')

        decry_decom(key, file_path)
        print("|------*Login*------|")
        username = input("Username: ")
        password = masked_input()
        email = input("Email(2fa)(only google emails allowed): ")

        with open(f"{username}_key.key",'w') as user_key:
            user_key.write(pyotp.random_base32())
        
        shutil.move(f"{username}_key.key",user_key_path+f"\\{username}_key.key")

        bytes_password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(bytes_password, salt)

        lines = extract_lines(username, file_path)
        # print(lines[1]+'\n')

        if lines and bcrypt.checkpw(bytes_password, lines[1].encode('utf-8')) and email == :
            with open(f"{user_key_path}\\{username}_key.key", 'r') as f:
                contents = f.read()
            print("email found")
            send_email(sender_email=sendr_email,
                    sender_password=sendr_pass,
                    recipient_email=email, 
                    subject=sub,
                    message=msg,
                    attachment_path=qr+f'\\{username}_qr.png')
            totp = pyotp.TOTP(contents)
            verification = totp.verify(input("Enter the Code : "))

            if verification:
                print("Login verification successful")
                encry_compr(key, file_path)
                return
            else:
                print("Login verification unsuccessful")
                encry_compr(key, file_path)
                return

        sign_up = input('Account not found. Would you like to sign up using these credentials? (y/n): ').lower()

        if sign_up == 'y':
            with open(file_path, 'a') as sign:
                with open(file_path, 'r') as file:
                    for line in file:
                        if re.search(r'---{}---'.format(re.escape(username)), line):
                            print("Username is already in use\n")
                            os.remove(user_key_path+f"\\{username}_key.key")
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
                    
                if len(username)-1 < 4 and len(password)-1 < 8:
                    print("Username must be more than 3 characters long and password must be 8 or more characters")
                    os.remove(user_key_path+f"\\{username}_key.key")
                    if os.path.getsize(file_path) == 0:
                        return
                    else:
                        encry_compr(key, file_path)
                        return
                    
                elif len(username)-1 < 4 or len(username)-1 > 20:
                    print("Username must be more than 3 characters long")
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
                    
                uri = pyotp.totp.TOTP(contents).provisioning_uri( 
                name=username, 
                issuer_name='GalacticCoder')
                qrcode.make(uri).save(f"{username}_qr.png")
                shutil.move(f"{username}_qr.png", qr+f'\\{username}_qr.png')

                sign.write(f'---{username}---\n')
                sign.write(f'{username}\n')
                sign.write(f'{hash_password.decode("utf-8")}\n')
                sign.write(f'{email}\n')
                sign.write(f'---*end of {username}*---\n')

                print("Sign up successful")

            encry_compr(key, file_path)

        elif sign_up == 'n':
            os.remove(qr+f"\\{username}_qr.png")
            os.remove(user_key_path+f"\\{username}_key.key")
            if os.path.getsize(file_path) == 0:
                return
            else:
                encry_compr(key, file_path)
                return
        else:
            os.remove(user_key_path+f"\\{username}_key.key")
            if os.path.getsize(file_path) == 0:
                print("Invalid option. Exiting")
                return
            else:
                print("Invalid option. Exiting")
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
        os.remove(user_key_path+f"\\{username}_key.key")
        if os.path.getsize(file_path) == 0:
            print(Error)
            return
        else:
            print(Error)
            encry_compr(key, file_path)
            return

account()