import csv
import random
import time
from telethon.errors.rpcerrorlist import PeerFloodError
from models import MessageSent, Account
from telethon.sync import TelegramClient


def make_sure_an_account_exists():
    accounts = Account.select()
    if len(accounts) == 0:
        print("No account was found! Please enter a new one")
        save_credentials()


def send_messages(client, message, usernames, min_sleep=30, max_sleep=45):
    for username in usernames:
        query = MessageSent.select().where(MessageSent.username ==
                                           username, MessageSent.message == message)
        if not query.exists():
            print('Sending Message...')
            try:
                client.send_message(username, message)
                message_record = MessageSent(
                    username=username, message=message)
                message_record.save()
                print(f'Sent message "{message}" to user "{username}"')
                sleep_seconds = random.randint(min_sleep, max_sleep)
                print(f'Waiting {sleep_seconds} seconds for safety')
                time.sleep(sleep_seconds)
            except PeerFloodError:
                print('You reached Telegram daily limit! Stopping now')
                break
        else:
            print('Already Sent this message Message. Skipping...')


def get_usernames():
    with open('members.csv', 'r') as f:
        csvreader = csv.reader(f)
        usernames = []
        for line in csvreader:
            if line[0] not in ('username', ''):
                usernames.append(line[0])
    return usernames


def make_sure_client_authenticates(phone, api_id, api_hash):
    print(f'Checking if {phone} is authenticated...')
    client = TelegramClient(phone, api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        print('Just one more step is needed...')
        print(f'Telegram will send a code to {phone}.')
        print(f'Please check if you received a code via SMS or telegram app')
        client.send_code_request(phone)
        client.sign_in(phone, input(f'Enter the code that Telegram sent to {phone}: '))
    print('OK')
    client.disconnect()


def save_credentials():
    print("HELP: Visit https://my.telegram.org/ to get the api id and the api hash for your account")
    phone = input(
        'Enter the account phone number (with country code): ').strip()
    api_id = int(input('Enter the account api id: ').strip())
    api_hash = input('Enter the account api_hash: ').strip()
    make_sure_client_authenticates(phone, api_id, api_hash)
    account = Account(phone=phone, api_id=api_id, api_hash=api_hash)
    account.save()
    print('Account saved')


def keep_running():
    """Keep GUI Window Open when program reaches the final line"""
    print('Execution ended. You can close this window...')
    while True:
        pass
