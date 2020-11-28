import click
import json
import os
import requests
import sys
import jwt
import time, sys

from prettytable import PrettyTable

from mysocketctl.ssh import SystemSSH, Paramiko

api_url = "https://api.mysocket.io/"
token_file = os.path.expanduser(os.path.join("~", ".mysocketio_token"))


# For debug
debug = False
if "MYSOCKET_DEBUG" in os.environ:
    if os.environ["MYSOCKET_DEBUG"] == "TRUE":
        try:
            import http.client as http_client

            print("DEBUG ENABLED")
        except ImportError:
            print("unable to import http.client for debug")
        http_client.HTTPConnection.debuglevel = 10
        debug = True


def get_user_id():
    try:
        with open(token_file, "r") as myfile:

            for token in myfile:
                token = token.strip()
                try:
                    data = jwt.decode(token, verify=False)
                except:
                    print("barf on " + token)
                    data = jwt.decode(token, verify=False)
                    continue

                if "user_id" in data:
                    return data["user_id"]

    except IOError:
        print("Could not read file:", token_file)
        print("Please login again")
        sys.exit(1)
    print("No valid token in " + token_file + ". Please login again")


def get_auth_header():
    try:
        with open(token_file, "r") as myfile:

            for token in myfile:
                token = token.strip()
                try:
                    data = jwt.decode(token, verify=False)
                except:
                    print("barf on " + token)
                    data = jwt.decode(token, verify=False)
                    continue

                authorization_header = {
                    "x-access-token": token,
                    "accept": "application/json",
                    "Content-Type": "application/json",
                }
                return authorization_header
    except IOError:
        print("Could not read file:", token_file)
        print("Please login again")
        sys.exit(1)
    print("No valid token in " + token_file + ". Please login again")
    sys.exit(1)


def validate_response(http_repsonse):
    if debug == True:
        print("Server responded with data:")
        print(http_repsonse.text)

    if http_repsonse.status_code == 200:
        return http_repsonse.status_code
    if http_repsonse.status_code == 204:
        return http_repsonse.status_code

    elif http_repsonse.status_code == 401:
        print("Login failed")
    else:
        print(http_repsonse.status_code, http_repsonse.text)

    sys.exit(1)
