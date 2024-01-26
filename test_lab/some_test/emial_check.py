import bcrypt

def check_email_existence(file_path, username, hashed_email):
    with open(file_path, 'r') as file:
        inside_block = False
        for line in file:
            if '---{}---'.format(username) in line:
                inside_block = True
            elif '---*end of {}*---'.format(username) in line:
                inside_block = False
            elif inside_block and line.strip() == hashed_email.decode("utf-8"):
                return True
    return False

def write_to_file(file_path, username, salt, hashed_email):
    with open(file_path, 'a') as file:
        file.write('---{}---\n'.format(username))
        file.write(salt.decode('utf-8') + '\n')
        file.write(hashed_email.decode('utf-8') + '\n')
        file.write('---*end of {}*---\n'.format(username))

username = "someone"
email = 'something@gmail.com'
password = "50031533"
file_path = "C:\\Users\\zombi\\OneDrive\\Desktop\\system_proj\\test_lab\\some_test\\TextFile1.txt"

email = "something@gmail.com"

bytes_email = email.encode("utf-8")

salt = bcrypt.gensalt()

user = "something@gmail.com"

userbytes = user.encode("utf-8")

hash2 = bcrypt.hashpw(userbytes, salt)
hash = bcrypt.hashpw(bytes_email, salt)
print(hash2.decode('utf-8')+'\n',hash.decode("utf-8"))

if check_email_existence(file_path, username, hash):
    print("Email is already in use.")
else:
    print("New email")
    write_to_file(file_path, username, salt, hash)

# Rest of your code...
