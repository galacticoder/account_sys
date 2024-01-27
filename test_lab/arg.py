from passlib.hash import argon2

passs = "someone"
bytes = passs.encode("utf-8")

hashed_password = argon2.using(rounds=4).hash(passs)

with open("pass.txt",'w') as file:
    file.write(hashed_password)
    
print(argon2.verify(passs,hashed_password))
    
print(hashed_password)