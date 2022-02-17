import csv
import os
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


def load_message_to_send():
    if not os.path.isfile('message.txt'):
        with open('message.txt', 'w') as f:
            f.write('')
    with open('message.txt', 'r') as f:
        message = f.read().strip()

    return message


def send_messages(client, message, usernames, phone="", min_sleep=60, max_sleep=120):
    if len(message) > 0:
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
                    print(f'Sent message "{message}" to user "{username}" using phone {phone}')
                    sleep_seconds = random.randint(min_sleep, max_sleep)
                    print(f'Waiting {sleep_seconds} seconds for safety')
                    time.sleep(sleep_seconds)
                except PeerFloodError:
                    print(f'{phone} reached Telegram daily limit! Stopping now')
                    break
            else:
                print('Already Sent this message Message. Skipping...')
    else:
        print('You did not defined a message to send to users')
        print('Please open file message.txt and paste the message you need to be sent')


def get_usernames():
    if os.path.isfile('members.csv'):
        try:
            with open('members.csv', 'r') as f:
                csvreader = csv.reader(f)
                usernames = []
                for line in csvreader:
                    if line[0] not in ('username', ''):
                        usernames.append(line[0])
            return usernames
        except Exception as e:
            print(e)
    else:
        print('No group selected. Please select a group to select message from first')
        return []


def make_sure_client_authenticates(phone, api_id, api_hash):
    try:
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
    except Exception as e:
        print(e)


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
    print('Execution ended. You can close this window and re-open it again...')
    while True:
        pass


def print_accounts(accounts):
    for account in accounts:
        print(f'Found {len(accounts)} telegram account(s) saved')
        make_sure_client_authenticates(
            account.phone, account.api_id, account.api_hash)


def ask_to_add_new_account():
    answer = None
    while answer not in ('y', 'n'):
        answer = input('DO you want to add a new account? [y/n]: ').strip().lower()
    if answer == "y":
        print('OK, next add a new account.')
        save_credentials()


def run(account):
    client = TelegramClient(account.phone, account.api_id, account.api_hash)
    client.connect()
    send_messages(client, message=load_message_to_send(),
                  usernames=get_usernames(), phone=account.phone)


def list_accounts():
    accounts = Account.select()
    for account in accounts:
        print(f'{account.id}')
        print(f'Phone: {account.phone}')
        print(f'Api Id - {account.api_id}')
        print(f'Api hash - {account.api_hash}')
        print('')


def delete_account():
    ids = []
    accounts = Account.select()
    for account in accounts:
        print(f'{account.id} - {account.phone}')
        ids.append(str(account.id))

    account_to_delete_id = None
    while account_to_delete_id not in ids:
        account_to_delete_id = input('Wich account do you want to delete? ')
    account = Account.select().where(Account.id == account_to_delete_id).get()
    account.delete_instance()
    print(f'Successfully deleted {account.phone}')

