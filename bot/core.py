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
                   keep_running)


def core():
    try:
        make_sure_an_account_exists()

        accounts = Account.select()

        for account in accounts:
            print(f'Found {len(accounts)} telegram account(s) saved')
            make_sure_client_authenticates(
                account.phone, account.api_id, account.api_hash)

        answer = None
        while answer not in ('y', 'n'):
            answer = input('DO you want to add a new account? [y/n]: ').strip().lower()
        if answer == "y":
            print('OK, next add a new account.')
            save_credentials()

        print(f'Logged in with {accounts[0].phone} so you can select a telegram group')
        client = TelegramClient(
            accounts[0].phone, accounts[0].api_id, accounts[0].api_hash)
        client.connect()
        scrape_members(client)
        client.disconnect()

        def run(account):
            client = TelegramClient(account.phone, account.api_id, account.api_hash)
            client.connect()
            send_messages(client, message=load_message_to_send(),
                          usernames=get_usernames(), phone=account.phone)

        processes = []
        for account in accounts:
            p = multiprocessing.Process(target=run, args=[account])
            p.start()
            processes.append(p)

        for process in processes:
            process.join()

    except Exception as e:
        print(e)

    keep_running()
