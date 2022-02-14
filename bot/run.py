import os
from models import MessageSent

if not os.path.isdir(os.path.join(os.getcwd(), 'telegramBot')):
    os.mkdir('telegramBot')
os.chdir('telegramBot')

if __name__ == "__main__":
    from core import core
    core()
