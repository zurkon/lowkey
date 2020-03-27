from __future__ import print_function, unicode_literals

# reGex to validade email input
import re
import os
import platform

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
def GetCommand():
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
def GetUserConfirm():
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
    answers = prompt(questions, style=style)

    # print the answers
    for item in answers:
        print(f"{item}: {answers[item]}")


# System variables
command = ""
exiting = False


# ===============================================================================
# ++++++++++++++++++++++++++++++++  BEGINNING  ++++++++++++++++++++++++++++++++++
# ===============================================================================


# banner = colored(figlet_format("Lowkey", font="slant"), "yellow")
# print(banner)

# description = colored("A Python Command-Line Interface to manage your passwords", "green")
# print(description)


while not exiting:

    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

    banner = colored(figlet_format("Lowkey", font="slant"), "yellow")
    print(banner)

    description = colored("A Python Command-Line Interface to manage your passwords\n", "green")
    print(description)


    command = GetCommand()

    # command choices: 'Get a Service', 'Sign a Service', 'Exit'
    if command == "Sign a Service":
        askServiceInformation()
    elif command == "Exit":
        exiting = GetUserConfirm()
