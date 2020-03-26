import requests
import hashlib
import sys

# Request data to the PWNED API
def Request_API_data(five_chars):
    url = "https://api.pwnedpasswords.com/range/" + five_chars
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f"Error fetching: {response.status_code}, check the api and try again...")
    return response


# If you password has been PWNED, get how many times it was Leaked.
def Get_Pass_Leaks_Count(hashes, hash_to_check):
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def Pwned_API_check(password):
    sha1pass = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    # Stores the first 5 characters of Hashed Password
    first5_char = sha1pass[:5]
    # Stores the Hashes after 5 characters
    tail = sha1pass[5:]
    response = Request_API_data(first5_char)
    return Get_Pass_Leaks_Count(response, tail)


# Pass how many passwords you want on Command Line and the program will check each one of them
def main(args):
    for password in args:
        count = Pwned_API_check(password)
        if count:
            print(f"{password} was found {count} times... you should probably change your password!")
        else:
            print(f"{password} was NOT found. Carry On!")
    return "Done!"


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
