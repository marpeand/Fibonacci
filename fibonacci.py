# -*- coding: utf-8 -*-

import tweepy
import time
from datetime import datetime
from os import environ


class FibonacciBot:

    """
    Twitter bot that tweets the fibonacci series every 8 hours (INTERVAL). 
    the bot implements the tweepy module to connect and publish tweets. 

    >...[www.github.com/marpeand]
    >...[www.twitter.com/thefibonaccibot]

    """
    keys = {
        'CONSUMER_KEY':         environ['CONSUMER_KEY'],
        'CONSUMER_SECRET':      environ['CONSUMER_SECRET'],
        'ACCESS_TOKEN':         environ['ACCESS_TOKEN'],
        'ACCESS_TOKEN_SECRET':  environ['ACCESS_TOKEN_SECRET']
    }

    def __init__(self, key=keys):
        self.INTERVAL = 8  # tweets every 8 hours
        self.SLEEP = 60    # check every 60 seconds the time

        self.auth = tweepy.OAuthHandler(key['CONSUMER_KEY'], key['CONSUMER_SECRET'])
        self.auth.set_access_token(key['ACCESS_TOKEN'], key['ACCESS_TOKEN_SECRET'])
        self.api = tweepy.API(self.auth)


    def fibonacci(self, F1,F2):
        """
            This function returns the Fn number
        """
        Fn = F1+F2
        return Fn


    def get_tweets(self):
        """
            It returns the last two tweets
        """

        tweets = self.api.user_timeline('thefibonaccibot',count=2)
        Fone = int(tweets[0].text)
        Ftwo = int(tweets[1].text)

        return Fone,Ftwo


    def get_n(self):
        """
            Get actual 'n'
        """

        profile = self.api.get_user('thefibonaccibot')
        n = profile.statuses_count
        return n


    def time_last_n(self):
        """
            This function returns the last Fn hour (the last tweet hour).
        """

        tweet = self.api.user_timeline('thefibonaccibot', count=1)
        N_time = tweet[0].created_at

        return N_time

    def update(self, f1,f2):
        """
            This function updates the status
        """

        number = self.fibonacci(f1,f2)
        n = self.get_n()

        try:
            self.api.update_status(number)
            print('Status updated, n = {}'.format(n+1))
        except tweepy.TweepError as update_error:
            if update_error.args[0][0]['code'] == 187:
                print('Cant update status, n = {} , n + 1'.format(n))
                self.update(f1,f2+1)
            else:
                print('There is a problemita trying to update...')

    def check_time(self):
        """
            This function checks every 'SLEEP' seconds if the machine time 
            is equal to the next time of the tweet, if they are the same
            the update() function is activated
        """

        while 1:
            Tweet_time = self.time_last_n()
            NOW = datetime.now()

            NOW_hour = NOW.hour      # Server time
            NOW_minute = NOW.minute  # Server minutes

            Next_tweet_hour = Tweet_time.hour + self.INTERVAL  # Next tweet hour

            if Next_tweet_hour > 24:
                Next_tweet_hour -= 24

            if NOW_hour == Next_tweet_hour and NOW_minute == 0:
                f_1,f_2 = self.get_tweets()
                self.update(f_1,f_2)
            else:
                print('Next tweet => {}:00 ({}:{})'.format(Next_tweet_hour,NOW_hour, NOW_minute))  # this line can be commented
                self.get_tweets()

            time.sleep(self.SLEEP)


def main():
    fibonacci = FibonacciBot()
    fibonacci.check_time()


if __name__ == '__main__':
    main()
