from __future__ import print_function, unicode_literals

# reGex to validade email input
import re

# System features
import os
import platform

# Project modules
import cryptodata
import json

# Copy service info to  user's clipboard
import pyperclip

# Modules for Better CLI Display
from pyfiglet import figlet_format
from termcolor import colored

# Modules for CLI user's info request
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError

# Style form PyInquirer
style = style_from_dict(
    {
        Token.QuestionMark: "#E91E63 bold",
        Token.Selected: "#673AB7 bold",
        Token.Pointer: "#673AB7 bold",
        Token.Instruction: "",  # default
        Token.Answer: "#2196f3 bold",
        Token.Question: "",
    }
)



# Validator Classes for PyInquirer validate
class EmailValidator(Validator):
    emailPattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$)"

    def validate(self, email):
        if len(email.text):
            if re.match(self.emailPattern, email.text):
                return True
            else:
                raise ValidationError( message="Invalid email", cursor_position=len( email.text ) )
                # raise ValidationError( message="Invalid email" )
        else:
            raise ValidationError( message="You can't leave this blank", cursor_position=len( email.text ) )


class EmptyValidator(Validator):
    def validate(self, value):
        if len(value.text):
            return True
        else:
            raise ValidationError( message="You can't leave this blank", cursor_position=len( value.text ) )



# PyInquirer Select Option List
def getCommand():
    questions = [
        {
            "type": "list",
            "name": "command",
            "message": "What do you want to do?",
            "choices": ['Get a Service', 'Sign a Service', 'Exit']
        }
    ]

    # prompt returns a Dict with user's answers
    choice = prompt(questions, style=style)
    return choice["command"]


# PyInquirer Confirm Exit
def getUserConfirm():
    questions = [
        {
            "type": "confirm",
            "message": "Do you want to exit?",
            "name": "exit",
            "default": False,
        }
    ]
    # prompt returns a Dict with user's answers
    choice = prompt(questions, style=style)
    return choice["exit"]


# PyInquirer Service Questions
def askServiceInformation():
    questions = [
        {
            "type": "input", 
            "name": "service", 
            "message": "Service Name:",
            "validate": EmptyValidator
        },
        {
            "type": "input", 
            "name": "email", 
            "message": "Service Email:", 
            "validate": EmailValidator
        },
        {
            "type": "password",
            "name": "password", 
            "message": "Service Password",
            "validate": EmptyValidator
        },
    ]

    # prompt returns a Dict with user's answers
    service = prompt(questions, style=style)

    status = saveServiceData(service)

    print(colored(status, "green"))
    input("Press any key to Continue...")

# Ask User to select a service and copy service info to clipboard
def selectService():
    services_data = []
    service_options = []
    with open("data.json") as json_file:
        encrypted_services_data = json.load(json_file)

    for item in encrypted_services_data:
        services_data.append(cryptodata.decrypt_service(item))

    for service in services_data:
        service_options.append(service["service"])

    questions = [
        {
            "type": "list",
            "name": "service",
            "message": "Select a Service:",
            "choices": service_options
        }
    ]

    # prompt returns a Dict with user's answers
    choice = prompt(questions, style=style)
    
    # After user select a service, find that service's info...
    for service in services_data:
        if service["service"].lower() == choice["service"].lower():
            # And pass it to clipboard
            pyperclip.copy(service["password"])
            print( colored(f"\nService Password copied to the Clipboard...\n", "green") )

    input("Press any key to Continue...")


# Encrypt and Save service data
def saveServiceData(service):
    # Open data file
    with open("data.json") as json_file:
        services_data = json.load(json_file)
    
    services_data.append(cryptodata.encrypt_service(service, cryptodata.generateSecret()))

    # ReWrite data file with new service included
    with open("data.json", "w") as json_file:
        json.dump(services_data, json_file, indent=4)

    return "Service Registered"


# System variables
command = ""
exiting = False


# ===============================================================================
# ++++++++++++++++++++++++++++++++  BEGINNING  ++++++++++++++++++++++++++++++++++
# ===============================================================================


while not exiting:

    # Clear the terminal
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

    # Prompt the Lowkey logo and Description
    banner = colored(figlet_format("Lowkey", font="slant"), "yellow")
    print(banner)

    description = colored("A Python Command-Line Interface to manage your passwords\n", "green")
    print(description)

    # Get user command
    command = getCommand()

    # command choices: 'Get a Service', 'Sign a Service', 'Exit'
    if command == "Get a Service":
        selectService()
    elif command == "Sign a Service":
        askServiceInformation()
    elif command == "Exit":
        exiting = getUserConfirm()

# If user wants exit, let's clear the terminal...
if exiting:
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
