from telethon.sync import TelegramClient
from scrapers import scrape_members
from models import Account
from utils import (get_usernames,
                   send_messages,
                   save_credentials,
                   make_sure_client_authenticates,
                   make_sure_an_account_exists,
                   keep_running)


def core():
    make_sure_an_account_exists()

    accounts = Account.select()

    for account in accounts:
        print(f'Found {len(accounts)} telegram account(s) saved')
        make_sure_client_authenticates(
            account.phone, account.api_id, account.api_hash)

    client = TelegramClient(
        accounts[0].phone, accounts[0].api_id, accounts[0].api_hash)
    client.connect()
    scrape_members(client)
    client.disconnect()

    for account in accounts:
        client = TelegramClient(
            account.phone, account.api_id, account.api_hash)
        client.connect()
        send_messages(client, message="Opa, como vai?",
                      usernames=get_usernames())

    keep_running()
