import tkinter as tk
from tkinter import messagebox
import subprocess
import json
import os
from dotenv import load_dotenv

# Load configuration from .env file
load_dotenv()

def reset_user_password():
    profile = profile_entry.get()
    user_pool_id = user_pool_id_entry.get()
    username = username_entry.get()
    new_password = temp_password_entry.get()

    if not all([profile, user_pool_id, username, new_password]):
        messagebox.showerror("Error", "Profile, Pool ID, Username, and Password are required for reset.")
        return

    try:
        subprocess.run([
            "aws", "cognito-idp", "admin-set-user-password",
            "--profile", profile,
            "--user-pool-id", user_pool_id,
            "--username", username,
            "--password", new_password,
            "--permanent"
        ], check=True)

        messagebox.showinfo("Success", f"Password for '{username}' reset successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Reset Error", e.stderr if e.stderr else str(e))

def run_cognito_admin_flow():
    profile = profile_entry.get()
    user_pool_id = user_pool_id_entry.get()
    client_id = client_id_entry.get()
    username = username_entry.get()
    password = temp_password_entry.get()
    email = email_entry.get()

    if not all([profile, user_pool_id, client_id, username, password, email]):
        messagebox.showerror("Error", "All fields are required for login.")
        return

    try:
        result = subprocess.run([
            "aws", "cognito-idp", "admin-initiate-auth",
            "--profile", profile,
            "--user-pool-id", user_pool_id,
            "--client-id", client_id,
            "--auth-flow", "ADMIN_NO_SRP_AUTH",
            "--auth-parameters", f"USERNAME={username},PASSWORD={password}"
        ], check=True, capture_output=True, text=True)

        tokens = json.loads(result.stdout).get("AuthenticationResult", {})
        token_str = json.dumps(tokens, indent=2)

        with open("auth_tokens.json", "w") as f_json:
            f_json.write(token_str)

        with open("auth_tokens.txt", "w") as f_txt:
            for k, v in tokens.items():
                f_txt.write(f"{k}: {v}\n")

        messagebox.showinfo("Success", "Tokens saved to auth_tokens.json and auth_tokens.txt")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("AWS CLI Error", e.stderr if e.stderr else str(e))

# UI Setup
root = tk.Tk()
root.title("Cognito Admin Auth & Reset Tool (.env Configurable)")

fields = [
    ("AWS CLI Profile", "profile_entry", os.getenv("AWS_PROFILE", "default")),
    ("User Pool ID", "user_pool_id_entry", os.getenv("USER_POOL_ID", "")),
    ("App Client ID", "client_id_entry", os.getenv("APP_CLIENT_ID", "")),
    ("Username", "username_entry", os.getenv("COGNITO_USERNAME", "")),
    ("Password", "temp_password_entry", os.getenv("COGNITO_PASSWORD", "")),
    ("Email", "email_entry", os.getenv("COGNITO_EMAIL", "")),
]

for i, (label_text, var_name, default_value) in enumerate(fields):
    label = tk.Label(root, text=label_text)
    label.grid(row=i, column=0, padx=5, pady=5, sticky="e")
    entry = tk.Entry(root, show="*" if "password" in var_name else "")
    entry.insert(0, default_value)
    entry.grid(row=i, column=1, padx=5, pady=5)
    globals()[var_name] = entry

submit_button = tk.Button(root, text="Sign In with Password", command=run_cognito_admin_flow)
submit_button.grid(row=len(fields), column=0, pady=10)

reset_button = tk.Button(root, text="Reset User Password", command=reset_user_password)
reset_button.grid(row=len(fields), column=1, pady=10)

root.mainloop()
