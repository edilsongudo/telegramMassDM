import asyncio

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
                   choose_group,
                   run,
                   list_accounts,
                   keep_running)


def core():
  try:
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
        choose_group()

      elif action == '5':
        if len(accounts) > 0:
          loop = asyncio.get_event_loop()
          tasks = []
          for account in accounts:
            tasks.append(loop.create_task(run(account)))
          wait_tasks = asyncio.wait(tasks)
          loop.run_until_complete(wait_tasks)
          loop.close()
        else:
          print('No accounts found')

      print('Bot ended its work.')
      a = input('But press [c] if you want to do continue: ').lower()
      print('')
      if a == 'c':
        continue
      else:
        break

  except Exception as e:
    print(e)
