import time
import lzma
from cryptography.fernet import Fernet
import os
import shutil

with open("params.txt",'r') as par:
    lines = par.readlines()
    key = lines[0].strip().replace('key=', '').replace('"', '')

if os.path.exists(key) != True:
    key_write = Fernet.generate_key()

    with open(key, 'wb') as filekey:
        contents = filekey.write(key_write)

def format_size(size_in_bytes):
    if size_in_bytes >= 2**30:  # 1 GB = 2^30 bytes
        size_in_units = size_in_bytes / 2**30
        unit = "GB"
    elif size_in_bytes >= 2**20:  # 1 MB = 2^20 bytes
        size_in_units = size_in_bytes / 2**20
        unit = "MB"
    else:
        size_in_units = size_in_bytes / 2**10
        unit = "KB"
    return f"{size_in_units:.2f} {unit}"

def format_time(time_in_seconds):
    if time_in_seconds >= 1:
        return f"{time_in_seconds:.4f} seconds"
    else:
        time_in_milliseconds = time_in_seconds * 1000
        return f"{time_in_milliseconds:.2f} milliseconds"

def encry_compr(key, file): #first is encrypt and then compress
    global key_contents
    try:
        with open(key,'rb') as key_file:
            key_contents = key_file.read()
        fernet = Fernet(key_contents)
        with open(file,'rb') as file_co:
            fl = file_co.read()
            encrypted = fernet.encrypt(fl)
        with open(file,'wb') as enc_file:
            ee = enc_file.write(encrypted)
            print("File encrypted")
        original_data_size = len(encrypted)
        original_data_size = format_size(original_data_size)
        print('Original data size: ', original_data_size)
        start = time.time()
        compressed_data_lzma = lzma.compress(encrypted,preset=9) #all the way to 9
        end = time.time()
        compression_time = format_time(end - start)
        print("Compression time: ", compression_time)
        compressed_data_size = len(compressed_data_lzma)
        compressed_data_size = format_size(compressed_data_size)
        print("Compressed data size: ", compressed_data_size)
        with open(file,'wb') as fie:
            fie.write(compressed_data_lzma)
            print("Saved compression")
    except FileNotFoundError:
        print("File not found")
        return

def decry_decom(key, file): #first uncompress and then unencrypt
    try:
        with open(key, 'rb') as key_file:
            key_content2 = key_file.read()
        fernet = Fernet(key_content2)
        with open(file, 'rb') as file_co:
            compressed_data = file_co.read()
        start = time.time()
        decompressed_data = lzma.decompress(compressed_data)
        end = time.time()
        decompression_time = format_time(end - start)
        print("Decompression time: ", decompression_time)
        decrypted = fernet.decrypt(decompressed_data)
        with open(file, 'wb') as decry_file:
            decry_file.write(decrypted)
        print("File decrypted")
    except FileNotFoundError:
        print("File not found")
        return
    except Exception:
        print("File is already decrypted and decompressed")
        return