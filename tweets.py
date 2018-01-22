from tweepy import Stream,OAuthHandler
from tweepy.streaming import StreamListener
from textblob import TextBlob
import time,re,sys

#Consumer Key,Consumer Secret,Access Token,Access Secret
ckey="yLgqgy1LkPeFn0PuTTvEIQUjx"
csecret="TkAjNoo4xtv0d2N5JK9JrDbuXRXkY8FCgPbGLByfSwGjHbfZow"
atoken="4357099632-OY13X4oLoJKVIvywUWOBBJ1MDTMqQkAenERshZG"
asecret="aWnDL2rbXqVWkGn74IEJGCY7X7QXQzlGdfXEuX5DCNtIG"

pos = neg = neu = count = 0
startTime = time.time()

#calculating the sentiment of the tweet
try:
    def tweetSenti(tweet):
        global pos, neg, neu
        analysis = TextBlob(clean_tweet(tweet))
        senti = analysis.sentiment.polarity
        if senti > 0:
            print();print ('positive');print("Polarity: ", round(senti*10)); pos+=1
        elif senti == 0:
            print();print('neutral');print("Polarity: ", round(senti*10)); neu+=1
        else:
            print();print('negative');print("Polarity: ", round(senti*10)); neg+=1
except KeyboardInterrupt:
    keyInterrupt();
    
#Removing symbols from the tweets
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

#Interrupt function
def keyInterrupt():
    global count,pos,neg,startTime;
    print();print("---Time Elapsed: %s seconds ---" % (time.time() - startTime));
    print("Total No of Tweets received: {}".format(count))
    print("Positive tweets percentage: {} %" .format(100*pos/count))
    print("Negative tweets percentage: {} %" .format(100*neg/count))

    sys.exit(0)

#Listener Class
class listener(StreamListener):
        def on_data(self, data):
            global count,startTime
            try:
                tweet = data.split(',"text":"')[1].split(',"source"')[0]
                print();print(tweet); count+=1;
                tweetSenti(clean_tweet(tweet))
                
                saveThis = str(time.time())+ ":::" + tweet
                saveFile1 = open('tweetsDB.csv', 'a')
                saveFile1.write(saveThis)
                saveFile1.write('\n\n')
                saveFile1.close()

                saveFile2 = open('twitterDB.csv','a')
                saveFile2.write(data)
                saveFile2.close()
                return True
            
            except KeyboardInterrupt:
                keyInterrupt();            
            except BaseException as e:
                print('Failed: ', str(e))
                
        def on_error(self, status):
            print (status)
        
#Connecting to twitter and authorization            
try: 
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    twitterStream = Stream(auth, listener())
except:
    print('Error: Authentication Failed')

try:
    twitterStream.filter(track=["india"])
except KeyboardInterrupt:
    keyInterrupt();
