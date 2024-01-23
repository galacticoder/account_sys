import re

username = "someone"
email = "ilovevibingtolofii@gmail.com"
password = "50031533"
file_path = "C:\\Users\\zombi\\source\\repos\\some_test\\some_test\\TextFile1.txt"

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
            
print(lines_between_patterns)