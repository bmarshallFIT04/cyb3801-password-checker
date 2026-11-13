from pathlib import Path

#location of the common password database
PASSWORD_FILE = Path(__file__).parent / "100k-most-used-passwords-NCSC.txt"


#load common passwords into a set
def load_common_passwords():

    common_passwords = set()

    try:
        with open(PASSWORD_FILE, "r", encoding="utf-8") as file:

            for line in file:

                password = line.rstrip("\r\n")

                if password:
                    common_passwords.add(password)

    except FileNotFoundError:
        raise RuntimeError("Common password database not found.")

    return common_passwords


#load database once when the application starts
COMMON_PASSWORDS = load_common_passwords()


#check whether the entered password is commonly used
def check_common_password(password):

    #search for an exact match in the database
    if password in COMMON_PASSWORDS:

        return (
            "WARNING: This is a commonly used password! "
            "It is vulnerable to dictionary attacks and "
            "common-password brute-force guessing."
        )

    else:

        return (
            "SAFE: Password was not found in the common "
            "password database."
        )