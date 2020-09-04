import GetOldTweets3 as got
import pandas as pd
from datetime import date
import time
import threading
from telegram.ext import Updater, CommandHandler


updater = Updater(BOT_TOKEN, use_context=True)
username = TWITTER_USERNAME

def send_tweets_to_telegram(update, context):
	print('Sending to user ...')
	for tweet in push_tweets:
		update.message.reply_text(tweet)
	print('Tweets sent')


def retrieve_tweets():
	print('Retrieving new tweets ...')
	tweetCriteria = got.manager.TweetCriteria().setUsername(username).setSince(date.today().strftime('%Y-%m-%d'))
	tweets = got.manager.TweetManager.getTweets(tweetCriteria)
	for tweet in tweets:
		new_tweets.add(tweet.text)
	print('Completed retrieveal')

def init():
	global old_tweets
	global new_tweets
	global push_tweets
	old_tweets = {''}
	new_tweets = {''}
	print('Before while loop')
	while(True):
		retrieve_tweets()
		print('Check difference')
		#print(new_tweets)
		#print(old_tweets)
		print('New len:',len(new_tweets))
		print('Old len',len(old_tweets))
		if(len(new_tweets) > len(old_tweets)):
			print('God the updated tweets')
			push_tweets = new_tweets - old_tweets
			old_tweets = new_tweets
		time.sleep(20)


threading.Thread(target=init).start()
time.sleep(10)
print('After 10')
updater.dispatcher.add_handler(CommandHandler('hello', send_tweets_to_telegram))
threading.Thread(target=updater.start_polling).start()
