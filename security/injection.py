import re

# Maximum allowed password length to prevent DoS / memory exhaustion attacks
MAX_PASSWORD_LENGTH = 128

# Common injection signatures (evaluated strictly as inert string patterns, never executed)
SQLI_PATTERNS = [
    r"('|\")\s*(OR|AND)\s+('|\")?\d+('|\")?\s*=\s*('|\")?\d+",  # e.g., ' OR '1'='1
    r";\s*(DROP|DELETE|UPDATE|INSERT|SELECT|UNION|ALTER)\b",    # e.g., ; DROP TABLE users
    r"--\s*$",                                                  # SQL inline comment termination
]

XSS_PATTERNS = [
    r"<\s*script\b",                                            # <script> tags
    r"javascript\s*:",                                          # javascript: URI scheme
    r"\bon(error|load|click|mouseover|focus)\s*=",              # inline HTML event handlers
    r"<\s*(img|iframe|svg|object|embed)\b",                     # common HTML injection tags
]

CMDI_PATTERNS = [
    r"[;&|`]\s*(ls|cat|rm|whoami|id|pwd|wget|curl|bash|sh|nc|python)\b",  # shell command chaining
    r"\$\([^)]+\)",                                             # $(command) substitution
]


def validate_input(password):
    """
    Gatekeeper validation before any downstream processing occurs.
    Returns (is_valid: bool, error_message: str or None).
    """
    if not isinstance(password, str):
        return False, "Invalid input type: password must be a text string."

    if len(password) == 0:
        return False, "Invalid input: password cannot be empty."

    if len(password) > MAX_PASSWORD_LENGTH:
        return False, f"Invalid input: password exceeds maximum length of {MAX_PASSWORD_LENGTH} characters."

    # Block null bytes and non-printable ASCII control characters
    if "\x00" in password or any(ord(ch) < 32 for ch in password):
        return False, "Invalid input: password contains disallowed null bytes or control characters."

    return True, None


def check_injection(password):
    """
    Evaluates the password string strictly as inert data and reports whether
    malicious injection payloads were detected and safely neutralized.
    Returns a plain string for display in #injection.textContent.
    """
    is_valid, error_msg = validate_input(password)
    if not is_valid:
        return f"BLOCKED: {error_msg}"

    detected_threats = []

    if any(re.search(pattern, password, re.IGNORECASE) for pattern in SQLI_PATTERNS):
        detected_threats.append("SQL Injection")

    if any(re.search(pattern, password, re.IGNORECASE) for pattern in XSS_PATTERNS):
        detected_threats.append("Cross-Site Scripting (XSS)")

    if any(re.search(pattern, password, re.IGNORECASE) for pattern in CMDI_PATTERNS):
        detected_threats.append("OS Command Injection")

    if detected_threats:
        threats_list = ", ".join(detected_threats)
        return (
            f"WARNING (NEUTRALIZED): Malicious {threats_list} payload detected. "
            "Input was safely treated as plain data—no code or queries were executed."
        )

    return "SAFE: Input validated (length and encoding OK) and treated strictly as plain data."
