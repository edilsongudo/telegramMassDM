from telethon.sync import TelegramClient
from scrapers import scrape_members
from config import api_id, api_hash, phone
from utils import get_usernames, send_messages, keep_running

def core():
    client = TelegramClient(phone, int(api_id), api_hash)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))

    scrape_members(client)
    send_messages(client, message="Opa, como vai?", usernames=get_usernames())
    keep_running()
