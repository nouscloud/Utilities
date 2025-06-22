# Cognito Admin UI Tool

This is a simple Python GUI tool to authenticate and reset AWS Cognito user accounts using the AWS CLI and Cognito APIs.

## Features
- Sign in a Cognito user using Admin Initiate Auth flow
- Reset a Cognito user's password using Admin Set User Password
- Load credentials and configuration from `.env` file
- Save tokens to both `.json` and `.txt` formats
- UI built with Tkinter

## Requirements

- Python 3.x
- AWS CLI installed and configured
- AWS profile with appropriate permissions
- `boto3`, `tkinter`, and `python-dotenv` Python packages

## Setup

1. Clone the repo or extract the zip:
   ```bash
   git clone <repo-url>
   cd cognito_admin_ui_project
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your `.env` file:
   ```bash
   cp .env.sample .env
   # Then edit .env to add real credentials and values
   ```

4. Run the tool:
   ```bash
   python cognito_env_configurable_ui.py
   ```

## Notes

- The tool uses AWS CLI underneath. Make sure you're authenticated using `aws sso login` or `aws configure`.
- Tokens are saved to `auth_tokens.json` and `auth_tokens.txt` in the script folder.
- Do **not** commit `.env` or token files to version control (see `.gitignore`).

## License

MIT License
