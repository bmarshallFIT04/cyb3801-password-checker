# -----------------------------------------------------------------
# Checks if a password has appeared in a documented data breach
# >>>> Data is retrieved from the Have I Been Pwned API
# Password is hashed with SHA-1 before sending
# >>>> Only the first 5 characters of the hash are sent - full password never leaves the server
# >>>> Padding is used to prevent password guesses based on the response size
# Result: {"is_compromised": bool, "message": str}
# >>>> is_compromised: True if the password has been found in a data breach, False otherwise
# >>>> message: Compromised or Not found in any known data breaches
# -----------------------------------------------------------------

import hashlib
import requests

# Have I Been Pwned (HIBP) "Pwned Passwords" range API
HIBP_API = "https://api.pwnedpasswords.com/range/"

# Check if a password has been compromised using the Have I Been Pwned
def check_compromised_password(password):
    try:
        leak_count = get_leak_count(password)
    except requests.RequestException:
        # Check cannot be completed - Network errors
        return result(None, "Could not reach Have I Been Pwned - https://api.pwnedpasswords.com/range - try again later")

    # Password has been found in a data breach
    if leak_count > 0:
        return result(
            True,
            f"COMPROMISED - This password has appeared in {leak_count:,} "
            "data breaches!"
        )

    # Password has not been found in any data breaches
    return result(False, "Not found in any known data breaches.")

# Get the number of times a password has appeared in data breaches
def get_leak_count(password):
    # Hash the password with SHA-1 per the HIBP requirements
    hashed_pass = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

    # Split the hash for security
    pass_prefix = hashed_pass[:5]  # Sent to HIBP
    pass_suffix = hashed_pass[5:]  # Used to check against the returned data

    # Ask HIBP for the list of hashes that start with the prefix
    # Each line should match the format "suffix:count"
    response = requests.get(
        HIBP_API + pass_prefix,
        headers={"Add-Padding": "true", "User-Agent": "password-checker"},
        timeout=5
    )
    
    # Check if the reply had an error status
    response.raise_for_status()

    # Check each line to see if the suffix matches any of the returned hashes
    for line in response.text.splitlines():
        returned_suffix, count = line.split(":")
        if returned_suffix == pass_suffix:
            return int(count)

    # No matching hash found - the password has not been compromised
    return 0

# Return the final result as a dictionary
def result(is_compromised, message):
    return {"is_compromised": is_compromised, "message": message}
