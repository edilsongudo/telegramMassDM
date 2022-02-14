import csv
import random
import time
from telethon.errors.rpcerrorlist import PeerFloodError


def send_messages(client, message, usernames, min_sleep=30, max_sleep=45):
    for username in usernames:
        try:
            client.send_message(username, message)
            print(f'Sent message "{message}" to user "{username}"')
            sleep_seconds = random.randint(min_sleep, max_sleep)
            print(f'Waiting {sleep_seconds} seconds for safety')
            time.sleep(sleep_seconds)
        except PeerFloodError:
            print('You reached Telegram daily limit! Stopping now')
            break


def get_usernames():
    with open('members.csv', 'r') as f:
        csvreader = csv.reader(f)
        usernames = []
        for line in csvreader:
            if line[0] not in ('username', ''):
                usernames.append(line[0])
    return usernames


def keep_running():
    print('Execution ended. You can close this window...')
    while True:
        pass


# def add_accounts():
#     while True:
#         ammount_of_credentials = int(input('How many accounts do you want to add?'))
#         credentials = []
#         for i in range(ammount_of_credentials):
#             phone = input('Enter the account phone number (with country code): ').strip()
#             api_id = input('Enter the account api id: ').strip()
#             api_hash = input('Enter the account api_hash: ').strip()

#             account = {}
#             account['api_id'] = api_id
#             account['api_hash'] = api_hash
#             account['phone'] = phone
#             credentials.append(account.copy())

#             with open(os.path.join(os.getcwd(), 'multiconfig.json'), 'w') as config_file:
#                 json.dump(credentials, config_file, indent=2)
