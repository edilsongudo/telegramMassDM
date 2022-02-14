from telethon.sync import TelegramClient
from scrapers import scrape_members
from utils import (get_usernames,
    send_messages,
    save_credentials,
    make_sure_an_account_exists,
    keep_running)
from models import Account


def core():
    make_sure_an_account_exists()

    accounts = Account.select()

    client = TelegramClient(accounts[0].phone, accounts[0].api_id, accounts[0].api_hash)
    client.connect()
    scrape_members(client)
    client.disconnect()

    for account in accounts:
        client = TelegramClient(account.phone, account.api_id, account.api_hash)
        client.connect()
        send_messages(client, message="Opa, como vai?", usernames=get_usernames())

    keep_running()
