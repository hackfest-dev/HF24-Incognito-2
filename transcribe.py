import argparse

# Parse argument
parser = argparse.ArgumentParser(prog='transcriber')
parser.add_argument('-i', help='Enter the URL of YouTube video')
args = parser.parse_args()

# 1. Read API from text file
f = open("api.txt", "r")
api_key = f.read()

print('1. API is read ...')

