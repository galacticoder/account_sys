import bcrypt 

    
    
def saltss():
    global salt
    password = input("pass: ")
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()

    hash = bcrypt.hashpw(bytes,salt)
    
    
    with open("pass_store.txt",'w') as file:
        file.write(hash.decode("utf-8"))

    passs = input("some: ")
    bytes2 = passs.encode("utf-8")
    hash2 = bcrypt.hashpw(bytes2, salt)

    print(bcrypt.checkpw(hash2, hash))
    print(hash.decode("utf-8"))
    print(hash2.decode("utf-8"))
    
saltss()