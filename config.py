import os

with open('.env', 'r') as file:
    line = file.readline()
    os.environ[line[:line.find("=")]] = line[line.find("=") + 1:]

token = os.environ['token']
