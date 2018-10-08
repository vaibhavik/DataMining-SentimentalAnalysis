import tweepy
import csv
import subprocess
import re
from tweepy import OAuthHandler
 
 
consumer_key = 'rBy7eKgumFxFPdrJD0aV6TQrn'
consumer_secret = 'lwWWEnTEUN3PFcm79apWW1B6M0ZdnnP5oCms9H2TW10fWDaYoA'
access_token = '249528847-LMj0lAonamY5UqCUujSbubNYNTSLRwczY1WUqibn'
access_secret = 'jx8Dl8gRDhwQmTK8gB9QnW2fx0eNz5LtEZGJruwRkIIka'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)
ftweet=open("Avengers.csv", "w+")
f = csv.writer(ftweet)
results=api.search(q="Harry Potter and the goblet of fire",include_retweets=False,count=200,lang="en")
for result in results:
    #look for 2 or more repetitions of character and replace with the character itself
    # pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    # res=pattern.sub(r"\1\1", result)
    # res=re.sub(r'(.)\1{2,}', r'\1\1', str(result))    
    f.writerow([result.text.encode('utf-8')])
    #f.writerow([res.unicode('utf-8')])
ftweet.close()
#retcode = subprocess.call("Rscript  python_test1.R", shell=True)
#print retcode
