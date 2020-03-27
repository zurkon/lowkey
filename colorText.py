from __future__ import print_function, unicode_literals

from pyfiglet import figlet_format
from termcolor import colored

from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError

style = style_from_dict(
    {
        Token.QuestionMark: "#E91E63 bold",
        Token.Selected: "#673AB7 bold",
        Token.Instruction: "",  # default
        Token.Answer: "#2196f3 bold",
        Token.Question: "",
    }
)

emailPattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$)"

banner = colored(figlet_format("Lowkey", font="slant"), "yellow")
print(banner)

description = colored("A Python Command-Line Interface to manage your passwords", "green")
print(description)


questions = [
    {"type": "input", "name": "service", "message": "Service Name:"},
    {"type": "input", "name": "email", "message": "Service Email:"},
    {"type": "password", "name": "password", "message": "Service Password"},
]

answers = prompt(questions, style=style)
for item in answers:
    print(f"{item}: {answers[item]}")
