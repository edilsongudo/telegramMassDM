import asyncio
import csv
import os
import random

from models import Account, MessageSent, SleepTime
from scrapers import scrape_members
from telethon.errors.rpcerrorlist import PeerFloodError
from telethon.sync import TelegramClient


def make_sure_an_account_exists():
    accounts = Account.select()
    if len(accounts) == 0:
        print('No account was found! Please enter a new one')
        save_credentials()


def load_message_to_send():
    if not os.path.isfile(
        'message.txt',
    ):
        with open('message.txt', 'w') as f:
            f.write('')
    with open('message.txt', 'r', encoding='utf-8') as f:
        message = f.read().strip()

    return message


async def send_messages(
    client, message, usernames, phone=''):
    sleep_obj = SleepTime().select().get()

    MIN_SLEEP = sleep_obj.min_sleep_seconds
    MAX_SLEEP = sleep_obj.max_sleep_seconds

    if len(message) > 0:
        for username in usernames:
            query = MessageSent.select().where(
                MessageSent.username == username,
                MessageSent.message == message,
            )
            if not query.exists():
                print('Sending Message...')
                try:
                    await client.send_message(username, message)
                    message_record = MessageSent(
                        username=username, message=message
                    )
                    message_record.save()
                    print(
                        f'Sent message "{message}" to user "{username}" using phone {phone}'
                    )
                    sleep_seconds = random.randint(MIN_SLEEP, MAX_SLEEP)
                    print(f'Waiting {sleep_seconds} seconds for safety')
                    await asyncio.sleep(sleep_seconds)
                except PeerFloodError:
                    print(
                        f'{phone} reached Telegram daily limit! Stopping now'
                    )
                    break
            else:
                print('Already sent this message. Skipping...')
    else:
        print('You did not defined a message to send to users')
        print(
            'Please open file message.txt and paste the message you need to be sent'
        )


def get_usernames():
    if os.path.isfile('members.csv'):
        try:
            with open('members.csv', 'r', encoding='utf-8') as f:
                csvreader = csv.reader(f)
                usernames = []
                for line in csvreader:
                    if line[0] not in ('username', ''):
                        usernames.append(line[0])
            return usernames
        except Exception as e:
            print(e)
    else:
        print(
            'No group selected. Please select a group to select message from first'
        )
        return []


def make_sure_client_authenticates(phone, api_id, api_hash):
    try:
        print(f'Checking if {phone} is authenticated...')
        client = TelegramClient(phone, api_id, api_hash)
        client.connect()
        if not client.is_user_authorized():
            print('Just one more step is needed...')
            print(f'Telegram will send a code to {phone}.')
            print(
                f'Please check if you received a code via SMS or telegram app'
            )
            client.send_code_request(phone)
            client.sign_in(
                phone, input(f'Enter the code that Telegram sent to {phone}: ')
            )
        print('OK')
        client.disconnect()
    except Exception as e:
        print(e)


def save_credentials():
    print(
        'HELP: Visit https://my.telegram.org/ to get the api id and the api hash for your account'
    )
    phone = input(
        'Enter the account phone number (with country code): '
    ).strip()
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
            account.phone, account.api_id, account.api_hash
        )


def ask_to_add_new_account():
    answer = None
    while answer not in ('y', 'n'):
        answer = (
            input('DO you want to add a new account? [y/n]: ').strip().lower()
        )
    if answer == 'y':
        print('OK, next add a new account.')
        save_credentials()


async def run(account):
    try:
        client = TelegramClient(account.phone, account.api_id, account.api_hash)
        await client.connect()
        await send_messages(
            client,
            message=load_message_to_send(),
            usernames=get_usernames(),
            phone=account.phone,
        )
    except Exception as e:
        print(e)


def list_accounts():
    accounts = Account.select()
    if len(accounts) > 0:
        for account in accounts:
            print(f'{account.id}')
            print(f'Phone: {account.phone}')
            print(f'Api Id - {account.api_id}')
            print(f'Api hash - {account.api_hash}')
            print('')
    else:
        print('No account saved.')


def delete_account():
    ids = []
    accounts = Account.select()
    if len(accounts) > 0:
        for account in accounts:
            print(f'[{account.id}] - {account.phone}')
            ids.append(str(account.id))

        account_to_delete_id = None
        while account_to_delete_id not in ids:
            account_to_delete_id = input(
                'Wich account do you want to delete? '
            )
        account = (
            Account.select().where(Account.id == account_to_delete_id).get()
        )
        account.delete_instance()
        os.remove(f'{account.phone}.session')
        print(f'Successfully deleted {account.phone}')
    else:
        print('No account saved.')


def choose_group():
    accounts = Account.select()
    if len(accounts) > 0:
        ids = []
        for account in accounts:
            print(f'[{account.id}] - {account.phone}')
            ids.append(str(account.id))
        account_to_use_id = None
        while account_to_use_id not in ids:
            account_to_use_id = input('Wich account do you want to use? ')
        account = Account.select().where(Account.id == account_to_use_id).get()

        print(
            f'Logged in with {account.phone} so you can select a telegram group'
        )
        client = TelegramClient(
            account.phone, account.api_id, account.api_hash
        )
        client.connect()
        scrape_members(client)
        client.disconnect()
    else:
        print('No account saved.')
