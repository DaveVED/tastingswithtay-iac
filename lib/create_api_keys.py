#!/usr/bin/env python3

import argparse
import secrets


def generate_api_key(client, length=64):
    """Generate a secure API key with the specified length."""
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    api_key = "".join(secrets.choice(alphabet) for i in range(length))
    return f"{client}_{api_key}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", required=True, help="Name of the client")
    args = parser.parse_args()

    api_key = generate_api_key(args.client)
    print(api_key)


if __name__ == "__main__":
    main()
