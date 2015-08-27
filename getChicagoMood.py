import io
import json
import sys, os
from ConfigParser import SafeConfigParser
from twitter import *
from time import sleep
import logging
import math
from collections import Counter


def getPublicData(searchTag,outfolder,api):
	print "fetching data for"+ searchTag
	
	counts=Counter()
	n_tweets=0
	refresh_url=""
	days={"Mon":0,"Tue":0,"Wed":0,"Thu":0,"Fri":0}
   	try:

        	tweets=api.search.tweets(q="#Chicago#Food")
        	print "Total Tweets"+str(len(tweets['statuses']))
        	while(len(tweets['statuses'])>0):
		        	refresh_url=tweets["search_metadata"]["refresh_url"]
		        	print refresh_url
	       	
			        for tweet in tweets['statuses']:
			        	day=str((tweet["created_at"])[0:4]).strip()
			        	if days[day]==0:
			        		days[day]=+1
			        	else:
			        		days[day]=days[day]+1	
			        tweets=api.search.tweets(q=refresh_url)
			        print "Total Tweets"+str(len(tweets['statuses']))
	        print days
	        	

	except TwitterHTTPError as e:
	        if e.e.code == 401: # Not authorized
	            print("Not Authorized - Check your Twitter settings.\n Exiting.")
	            logging.error(str(e))
	            sys.exit()
	        elif e.e.code == 404: # Not found
	            logging.info("Oops, %s has no tweets or the account info is wrong. Moving on." % user)
	

if __name__ == '__main__' :
    config = SafeConfigParser()
    script_dir = os.path.dirname(__file__)
    config_file = os.path.join(script_dir, 'config/settings.cfg')
    config.read(config_file)
    
    
    logfile = config.get('files','logfile')
    outfolder = config.get('files','outfolder')
    searchTag="#Chicago #Food"
	
    # connect to the API using OAuth credentials
    api = Twitter(api_version='1.1', auth=OAuth(config.get('twitter', 'access_token'),
                         config.get('twitter', 'access_token_secret'),
                         config.get('twitter', 'consumer_key'),
                         config.get('twitter', 'consumer_secret')))
    getPublicData(searchTag,outfolder,api)





    