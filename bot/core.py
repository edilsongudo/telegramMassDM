import multiprocessing
from telethon.sync import TelegramClient
from scrapers import scrape_members
from models import Account
from utils import (get_usernames,
                   send_messages,
                   save_credentials,
                   load_message_to_send,
                   make_sure_client_authenticates,
                   make_sure_an_account_exists,
                   print_accounts,
                   delete_account,
                   ask_to_add_new_account,
                   run,
                   list_accounts,
                   keep_running)


def core():
    try:
        make_sure_an_account_exists()
        accounts = Account.select()

        while True:
            action = False
            print('What do you want to do? ')
            print('[1] - Add a new Telegram account.')
            print('[2] - List Telegram accounts')
            print('[3] - Delete a Telegram account')
            print('[4] - Select wich group the bot will use to send next messages.')
            print('[5] - Start Mass DM')
            while action not in ('1', '2', '3', '4', '5'):
                action = input('Enter: ')

            if action == '1':
                 save_credentials()

            if action == '2':
                 list_accounts()

            if action == '3':
                 delete_account()

            if action == '4':
                print(f'Logged in with {accounts[0].phone} so you can select a telegram group')
                client = TelegramClient(
                    accounts[0].phone, accounts[0].api_id, accounts[0].api_hash)
                client.connect()
                scrape_members(client)
                client.disconnect()

            elif action == '5':
                processes = []
                for account in accounts:
                    p = multiprocessing.Process(target=run, args=[account])
                    p.start()
                    processes.append(p)
                for process in processes:
                    process.join()

            print('')
            a = input('Do you want to continue? ').lower()
            print('')
            if a == 'y':
                continue
            elif a == 'n':
                break

    except Exception as e:
        print(e)
