from configparser import ConfigParser
import os


def save_initial_credentials():
    print("No account was found! Please enter a new one")
    print("HELP: Visit https://my.telegram.org/ to get the api id and the api hash for your account")

    phone = input('Enter the account phone number (with country code): ').strip()
    api_id = input('Enter the account api id: ').strip()
    api_hash = input('Enter the account api_hash: ').strip()
    content = f"""
[account]
api_id = {api_id}
api_hash = {api_hash}
phone = {phone}
"""
    with open('config.ini', 'w') as f:
        f.write(content)


if not os.path.isfile('config.ini'):
    save_initial_credentials()

config = ConfigParser()
config.read('config.ini')

api_hash = config['account']['api_hash']
phone = config['account']['phone']
api_id = config['account']['api_id']
