import logging
import praw
import random
import re
import traceback
import sys


BOT_USERNAME      = 'BOT_USERNAME'
BOT_PASSWORD      = 'BOT_PASSWORD'
BOT_CLIENT_ID     = 'BOT_CLIENT_ID'
BOT_CLIENT_SECRET = 'BOT_CLIENT_SECRET'
BOT_USER_AGENT    = 'BOT_USER_AGENT'
SUBREDDIT         = 'SUBREDDIT'

WIN_CONDITIONS    = {
        'rock': 'scissors',
        'scissors': 'paper',
        'paper': 'rock'
    }  

reddit = praw.Reddit(username=BOT_USERNAME,
                     password=BOT_PASSWORD,
                     client_id=BOT_CLIENT_ID,
                     client_secret=BOT_CLIENT_SECRET,
                     user_agent=BOT_USER_AGENT)


def run():
    for comment in reddit.subreddit(SUBREDDIT).stream.comments(skip_existing=True):
        if '!rps' in comment.body:
            logging.info('Post found!')

            user_choice = parse_user_choice(comment.body)
            bot_choice = random_rps()

            logging.info('Choices parsed, posting game result...')

            msg = result_message(user_choice, bot_choice)
            comment.reply(msg)

            logging.info('Completed!')


def parse_user_choice(text):
    text = text.lower()
    rps_regex = re.compile(r'(?<=\!rps\s)((rock)|(paper)|(scissors))')

    try:
        choice = re.search(rps_regex, text)[0]
    except IndexError:
        choice = None

    return choice


def result_message(user_choice, bot_choice):
    if user_choice == bot_choice:
        header = "**It's a tie!**\n\n"
    elif WIN_CONDITIONS[user_choice] == bot_choice:
        header = '**You win!**\n\n'
    elif WIN_CONDITIONS[bot_choice] == user_choice:
        header = '**You lose!**\n\n'
    else:
        logging.warning('User choice could not be parsed correctly.')
        return "**Sorry, that command wasn't recognized!**\n\n"

    user_choice_text = 'Your choice was: **{}**\n\n'.format(user_choice)
    bot_choice_text = 'My choice was: **{}**'.format(bot_choice)

    return ' '.join([header, user_choice_text, bot_choice_text])

              
def random_rps():
    rps = ['rock', 'paper', 'scissors']

    return random.choice(rps)

      
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    try:
        run()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        traceback.print_exc()