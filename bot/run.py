import os

if not os.path.isdir(os.path.join(os.getcwd(), 'telegramBot')):
    os.mkdir('telegramBot')

os.chdir('telegramBot')

if __name__ == "__main__":
    from models import MessageSent
    from core import core
    from utils import keep_running
    core()
    keep_running()
