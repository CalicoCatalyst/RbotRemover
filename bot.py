import praw
import argparse
import logging
import time


def scan(reddit, subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    for comment in subreddit.stream.comments():
        if 'remindme' in comment.body.lower() or '!remindme' in comment.body.lower() or 'remindmebot' in comment.body.lower():
            x = exists_in_thread(comment)
            if x is not None and comment.id != x:
                comment.mod.remove()


def exists_in_thread(comment_to_check):
    submission = comment_to_check.submission
    for comment in submission.comments.list():
        body = comment.body.lower()
        if isinstance(comment, praw.models.MoreComments):
            # See praw docs on MoreComments
            continue
        if not comment or comment.author is None:
            # If the comment or comment author was deleted, skip it
            continue
        if ('remindme' in body or '!remindme' in body or 'remindmebot' in body) and (comment.id != comment_to_check.id):
            return comment.id
        else:
            return None


def main():
    parser = argparse.ArgumentParser(description='Bot To Add Titles To Images')
    parser.add_argument('-d', '--debug', help='Enable Debug Logging', action='store_true')
    parser.add_argument('-l', '--loop', help='Enable Looping Function', action='store_true')
    parser.add_argument('interval', help='time (in seconds) to wait between cycles', type=int)

    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

    # logging.info('Bot initialized, processing the last %s submissions/messages every %s seconds' % (args.limit,
    #                                                                                               args.interval))
    logging.debug('Debug Enabled')

    r = praw.Reddit(client_id="",
                    client_secret="",
                    username="",
                    password="",
                    user_agent='Automated Remindmebot removal')
    sub = "jailbreak"
    try:
        if not args.loop:
            scan(r, sub)
            logging.info('Checking Complete, Exiting Program')
            exit(0)
        while True:
            scan(r, sub)
            logging.info('Checking Complete')
            time.sleep(args.interval)
    except KeyboardInterrupt:
        logging.debug("KeyboardInterrupt Detected, Cleaning up and exiting...")
        print("Cleaning up and exiting...")
        exit(0)


if __name__ == '__main__':
    main()
