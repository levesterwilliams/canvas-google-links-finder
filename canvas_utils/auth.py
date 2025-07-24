#
# Author: Levester Williams
# Date: 20 July 2025
# auth.py
#
"""
Provides utility functions for handling Canvas API credentials and
generating HTTP headers for authenticated API requests.

Functions
---------
load_json_file(json_file: str) -> dict
    Loads credentials from an external JSON file.

get_cred_json(json_file_path: str) -> dict
    Retrieves API credentials from a JSON file and handles related errors.

get_cred_env_var() -> dict
    Retrieves API credentials from an environment variable (CANVAS_API_CRED)
    and validates that the JSON structure is correct.

get_token(path: str = None) -> dict
    Gets the API token from either an environment variable or a JSON file.

headers(token: dict, server_type: str) -> dict
    Generates HTTP headers for Canvas API requests based on the provided
    server type.

Usage
-----
Example 1: Load from environment variable
    >>> from auth import get_token, headers
    >>> token = get_token()
    >>> request_headers = headers(token, "prod")

Example 2: Load from JSON file
    >>> from auth import get_token, headers
    >>> token = get_token("credentials.json")
    >>> request_headers = headers(token, "test")

Notes
------
- Client-facing functions: get_token() and headers()
- Environment variable `CANVAS_API_CRED` must be a JSON string if used.
- JSON files must be valid and contain expected keys for server types
  (e.g., "prod", "test").
- Functions exit the program (`sys.exit(1)`) if critical errors occur,
  such as missing credentials or invalid JSON.
"""

import json
import os
import sys

def load_json_file(json_file: str) -> dict:
    """Loads credentials from an external JSON file.

    Parameters:
    -----------
    json_file (str): Path to the JSON file.

    Returns:
    --------
    dict: Dictionary containing the loaded credentials, or None if an
    error occurs.

    Notes:
    ------
    If error occurs in opening the JSON file, the function raise an error
    exception for client/caller to handle.
    """
    try:
        with open(json_file, 'r') as file:
            credentials = json.load(file)
            return credentials
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"Failed to load credentials due to missing file {json_file}.") \
            from e
    except json.JSONDecodeError as e:
        raise RuntimeError(f"The JSON file {json_file} contains invalid JSON")\
            from e
    except Exception as e:
        raise RuntimeError("Error in loading credentials") from e



def get_cred_json(json_file_path: str) -> dict:
    """
    Retrieves an API credentials from a JSON file.

    Parameters:
    -----------
    json_file_path : A path to a JSON file.

    Returns:
    --------
    dict : An API token from either an environment variable or a json file.
    """
    return load_json_file(json_file_path)


def get_cred_env_var() -> dict:
    """Gets the API token from an environment variable.

    Parameters:
    -----------
    self : none

    Returns:
    --------
    dict : An API token.

    Raises:
    -------
    KeyError
        If the key-value pair does not exist.
    json.JSONDecodeError
        If JSON is invalid.
    TypeError
        If type is not a JSON string
    Exception
        If an error occurs.
    """
    env_value = os.getenv('CANVAS_API_CRED')
    if env_value is None:
        raise RuntimeError("Environment variable CANVAS_API_CRED is "
                           "missing.")
    try:
        return json.loads(env_value)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            "Environment variable CANVAS_API_CRED contains invalid JSON.") \
            from e

def get_token(path: str = None) -> dict:
    """Gets the API token from either an environment variable or a json
    file.

    Parameters:
    -----------
    path : str, optional
        Path to JSON file containing the token. If client does not provide path,
        token will be loaded from environment variable `CANVAS_API_TOKEN`.

    Returns:
    --------
    dict : An API token.
    """
    return get_cred_json(path) if path else get_cred_env_var()


def headers(token: dict, server_type: str) -> dict:
    """Generates HTTP headers for Canvas API calls.

    Parameters
    ----------
    token : dict
        Credentials dictionary.
    server_type : str
        Key in the token dictionary representing the desired token.

    Returns
    -------
    dict
        HTTP headers.
    """
    headers = None
    try:
        headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer {}'.format(token[server_type])}
    except KeyError as e:
        raise KeyError(f"Token dictionary does not contain server type "
               f"'{server_type}'.") from e
    return headers