import asyncio

from models import Account, SleepTime
from scrapers import scrape_members
from telethon.sync import TelegramClient
from utils import *


def core():
    try:
        accounts = Account.select()

        while True:
            action = False
            print('What do you want to do? ')
            print('[1] - Add a new Telegram account.')
            print('[2] - List Telegram accounts')
            print('[3] - Delete a Telegram account')
            print(
                '[4] - Select wich group the bot will use to send next messages.'
            )
            print('[5] - Start Mass DM')
            print('[6] - Change min and max sleep seconds per DM sent')
            while action not in ('1', '2', '3', '4', '5', '6'):
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

            elif action == '6':
                sleep_obj = SleepTime().select().get()
                MIN_SLEEP = sleep_obj.max_sleep_seconds
                MAX_SLEEP = sleep_obj.min_sleep_seconds
                print(f'Minimum sleep time is set to {MIN_SLEEP}')
                print(f'Maximum sleep time is set to {MAX_SLEEP}')
                print('The greater these values, the best!')
                while True:
                    min_sleep = input('Choose your new minumum sleep time per DM sent (seconds): ')
                    max_sleep = input('Choose your new maximum sleep time per DM sent (seconds): ')
                    if not min_sleep.isnumeric() or not max_sleep.isnumeric():
                        print('Please, type only numbers!')
                        continue
                    if min_sleep > max_sleep:
                        print('Minuimum sleep time cannot be greater than maximum sleep time!')
                        continue
                    if int(max_sleep) - int(min_sleep) < 60:
                        print('The difference beetween maximum sleep time and minum sleep time must be equal or greater than 60 seconds')
                        continue
                    if int(min_sleep) < 120:
                        print('Minuimum sleep time cannot be inferior to 120 seconds')
                        continue
                    break
                sleep_obj.min_sleep_seconds = int(min_sleep)
                sleep_obj.max_sleep_seconds = int(max_sleep)
                sleep_obj.save()
                print('Successfully changed sleep time.')

            print('Bot ended its work.')
            a = input('But press [c] if you want to do continue: ').lower()
            print('')
            if a == 'c':
                continue
            else:
                break

    except Exception as e:
        print(e)
