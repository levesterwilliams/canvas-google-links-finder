import os
import json
import unittest
from unittest.mock import patch, mock_open
from auth import load_json_file, get_cred_json, get_cred_env_var, get_token, headers


class TestAuth(unittest.TestCase):

    # --- load_json_file tests ---
    def test_load_json_file_valid(self):
        mock_data = '{"token": "abc123"}'
        with patch("builtins.open", mock_open(read_data=mock_data)):
            result = load_json_file("fake.json")
        self.assertEqual(result["token"], "abc123")

    def test_load_json_file_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            load_json_file("missing.json")

    def test_load_json_file_invalid_json(self):
        with patch("builtins.open", mock_open(read_data="{bad_json:}")):
            with self.assertRaises(RuntimeError):
                load_json_file("bad.json")

    # --- get_cred_json tests ---
    @patch("auth.load_json_file", return_value={"prod": "abc123"})
    def test_get_cred_json_valid(self, mock_loader):
        result = get_cred_json("cred.json")
        self.assertEqual(result["prod"], "abc123")

    def test_get_cred_json_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            get_cred_json("missing.json")

    def test_get_cred_json_invalid_json(self):
        with patch("builtins.open", mock_open(read_data="{bad_json:}")):
            with self.assertRaises(RuntimeError):
               get_cred_json("bad.json")

    # --- get_cred_env_var tests ---
    @patch.dict(os.environ, {"CANVAS_API_CRED": json.dumps({"prod": "envtoken"})})
    def test_get_cred_env_var_valid(self):
        result = get_cred_env_var()
        self.assertEqual(result["prod"], "envtoken")

    @patch.dict(os.environ, {}, clear=True)
    def test_get_cred_env_var_missing(self):
        with self.assertRaises(RuntimeError):
            get_cred_env_var()

    @patch.dict(os.environ, {"CANVAS_API_CRED": "invalid-json"})
    def test_get_cred_env_var_invalid_json(self):
        with self.assertRaises(RuntimeError):
            get_cred_env_var()

    # --- get_token tests ---
    @patch("auth.get_cred_env_var", return_value={"prod": "envtoken"})
    def test_get_token_env_var(self, mock_env):
        result = get_token()
        self.assertEqual(result["prod"], "envtoken")

    @patch("auth.get_cred_json", return_value={"prod": "filetoken"})
    def test_get_token_json_file(self, mock_json):
        result = get_token("cred.json")
        self.assertEqual(result["prod"], "filetoken")

    # --- headers tests ---
    def test_headers_valid(self):
        token = {"prod": "abc123"}
        result = headers(token, "prod")
        self.assertEqual(result["Authorization"], "Bearer abc123")

    def test_headers_missing_key(self):
        token = {"test": "abc123"}
        with self.assertRaises(KeyError):
            headers(token, "prod")


if __name__ == "__main__":
    unittest.main()
