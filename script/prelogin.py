#!/usr/bin/python
#!-- encoding=utf8 --*
'provide parameters servtime and nonce so that the login is more secure'
import json
import time
import random


def main():
    servtime = int(time.time())
    nonce = random.randint(0, 32768)
    parameters = {'servtime': servtime, 'nonce': nonce}
    print 'Content-Type: text/html\r\n\r\n'
    print json.dumps(parameters)


if __name__ == '__main__':
    main()
