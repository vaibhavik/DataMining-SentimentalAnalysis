from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import render
import mongoengine
import urllib2
from json import JSONDecoder,JSONEncoder
from dm.models import *
import unicodedata
import subprocess
import tweepy
import csv
import subprocess
import re
from tweepy import *
imge={}

def index(request):
	
	return render(request, 'ok.html', {})

def try2(request):
	movies_all=MovieOmdb.objects.all()
	i=0
	dic={}
	year=1995
	ob_ids=[]
	name=[]
	ratings=[]
	for x in movies_all:
		year_c=int(x.year)
		if(year_c<year):
			continue
		else:
			rat=float(unicodedata.normalize('NFKD', x.imdbrating).encode('ascii','ignore'))
			ratings.append(rat)
			name.append(str(unicodedata.normalize('NFKD', x.title).encode('ascii','ignore')))
	

	ratings.sort(reverse=True)
	i=0
	imge2={}
	i=0
	mov1=MovieOmdb.objects.all()
	for x in mov1:
		if(i>3):
			break
		else:
			imge2[i]=str(unicodedata.normalize('NFKD', x.poster).encode('ascii','ignore'))
			i+=1
	
	for x in range(0,3):
		 mov1=MovieOmdb.objects(imdbrating=str(ratings[x]))
		 for y in mov1:
			rat=str(unicodedata.normalize('NFKD', y.imdbrating).encode('ascii','ignore'))
			if rat in name:
				img=str(unicodedata.normalize('NFKD', y.poster).encode('ascii','ignore'))
				imge[i]=img
				i+=1
			else:
				continue
	return render_to_response('base2.html',{'imge':imge2})
   
   
   
   
def show_main(request):
	#{"Year":{"$gt":"2013"}}
	movies_all=MovieOmdb.objects.all()
	i=0
	dic={}
	year=1995
	ob_ids=[]
	name=[]
	ratings=[]
	for x in movies_all:
		year_c=int(x.year)
		if(year_c<year):
			continue
		else:
			rat=float(unicodedata.normalize('NFKD', x.imdbrating).encode('ascii','ignore'))
			ratings.append(rat)
			name.append(str(unicodedata.normalize('NFKD', x.title).encode('ascii','ignore')))
	

	ratings.sort(reverse=True)
	i=0
	
	
	for x in range(0,3):
		 mov1=MovieOmdb.objects(imdbrating=str(ratings[x]))
		 for y in mov1:
			rat=str(unicodedata.normalize('NFKD', y.imdbrating).encode('ascii','ignore'))
			if rat in name:
				img=str(unicodedata.normalize('NFKD', y.poster).encode('ascii','ignore'))
				imge[i]=img
				i+=1
			else:
				continue
	return render_to_response('base.html',{'imge':imge}	)


def addmovieomdb(request):
	#name=str(request.POST['movname'])
	url="http://www.omdbapi.com/?t=How+to+train+your+Dragon&y=&plot=short&r=json"
	kundli = urllib2.urlopen(url).read()
	dic	 = JSONDecoder().decode(kundli)
	dic['twitterR']="4.3"
	kundlies = MovieOmdb.objects.create(
		title=dic['Title'],
	 	year=dic['Year'],
	 	genre=dic['Genre'],
	 	actors=dic['Actors'],
	 	poster=dic['Poster'],
	 	imdbrating=dic['imdbRating'],
	 	twitterrating=dic['twitterR']

	 	)
	kundlies.save()
	return render_to_response('ok.html',{'kundli':url})

def try1(request):
		
        return render_to_response('praj1.html')


def gettweets(request):
	movname = str(request.POST['movname'])

	consumer_key = 'rBy7eKgumFxFPdrJD0aV6TQrn'
	consumer_secret = 'lwWWEnTEUN3PFcm79apWW1B6M0ZdnnP5oCms9H2TW10fWDaYoA'
	access_token = '249528847-LMj0lAonamY5UqCUujSbubNYNTSLRwczY1WUqibn'
	access_secret = 'jx8Dl8gRDhwQmTK8gB9QnW2fx0eNz5LtEZGJruwRkIIka'
	 
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	 
	api = tweepy.API(auth)
	ftweet=open("F:\DM project\Python Script\ww.csv", "w+")
	f = csv.writer(ftweet)
	results=api.search(q=movname,count=200)
	for result in results:	
	    #look for 2 or more repetitions of character and replace with the character itself
	    # pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
	    # res=pattern.sub(r"\1\1", result)
	    # res=re.sub(r'(.)\1{2,}', r'\1\1', str(result))    
	    f.writerow([result.text.encode('utf-8')])
	    #f.writerow([res.unicode('utf-8')])
	ftweet.close()


	return

def getrating(request):
	retcode = subprocess.call("Rscript  F:\DM project\Python Scripts\stemming.R", shell=True)
	imge={}
	imge[0]=retcode

	return render_to_response('praj2.html',{'imge':imge})
def getname(request):
	global gen
	global act
	name1=str(request.POST['txtName'])
	#mov1=MovieOmdb.objects(title=str(name))
	#name1="Inception"
	mov1=MovieOmdb.objects(title=str(name1))

	imge={}
	i=0
	for y in mov1:
		 	img=str(unicodedata.normalize('NFKD', y.poster).encode('ascii','ignore'))
		 	imge[i]=img
		 	rat=float(unicodedata.normalize('NFKD', y.imdbrating).encode('ascii','ignore'))
		 	imge[i+1]=rat
		 	act=str(unicodedata.normalize('NFKD', y.actors).encode('ascii','ignore'))
		 	imge[i+2]=act
		 	gen=str(unicodedata.normalize('NFKD', y.genre).encode('ascii','ignore'))
		 	twr=float(unicodedata.normalize('NFKD', y.twitterrating).encode('ascii','ignore'))
		 	year=str(unicodedata.normalize('NFKD', y.year).encode('ascii','ignore'))
		 	imge[i+3]=gen
		 	imge[i+4]=twr
		 	imge[i+5]=year
		 	
		 	
		 	i+=1
	return render_to_response('movied.html',{'imge1':imge})
def recommend(request):
	mov_genre =  gen
	mov_act = act
	mov_genre = mov_genre.split(',')
	name_actor=[]
	ratings_actor=[]
	name_genre=[]
	ratings_genre=[]
	mov_act = mov_act.split(',')
	for ma in mov_act:
		mov1=MovieOmdb.objects(actors=str(ma))
		for x in mov1:
			gen=str(unicodedata.normalize('NFKD', x.genre).encode('ascii','ignore'))
			if(gen==mg):
				rat=float(unicodedata.normalize('NFKD', x.imdbrating).encode('ascii','ignore'))
				ratings_actor.append(rat)
				name_actor.append(str(unicodedata.normalize('NFKD', x.title).encode('ascii','ignore')))
	for mg in mov_genre:
		mov1=MovieOmdb.objects(genre=str(mg))
		for x in mov1:
			act=str(unicodedata.normalize('NFKD', x.actors).encode('ascii','ignore'))
			if act in mov_act:
				rat=float(unicodedata.normalize('NFKD', x.imdbrating).encode('ascii','ignore'))
				ratings_actor.append(rat)
				name_actor.append(str(unicodedata.normalize('NFKD', x.title).encode('ascii','ignore')))
			else:
				rat=float(unicodedata.normalize('NFKD', x.imdbrating).encode('ascii','ignore'))
				ratings_genre.append(rat)
				name_genre.append(str(unicodedata.normalize('NFKD', x.title).encode('ascii','ignore')))
	ratings_actor.sort(reverse=True)
	ratings_genre.sort(reverse=True)
	imge={}
	i=0
	mov1=MovieOmdb.objects(imdbrating=str(ratings_actor[x]))
	for y in mov1:
		rat=str(unicodedata.normalize('NFKD', y.imdbrating).encode('ascii','ignore'))
		if rat in name:
			img=str(unicodedata.normalize('NFKD', y.poster).encode('ascii','ignore'))
			imge[i]=img
			i+=1
		else:
			continue
	ratings_actor.pop(0)
	for _ in range(0,2):
		if(ratings_actor[0]>ratings_genre[0]):
			rating=ratings_actor[0]
			ratings_actor.pop(0)
		else:
			rating=ratings_genre[0]
			ratings_genre.pop(0)
		mov1=MovieOmdb.objects(imdbrating=str(rating))
		for y in mov1:
			rat=str(unicodedata.normalize('NFKD', y.imdbrating).encode('ascii','ignore'))
			if rat in name:
				img=str(unicodedata.normalize('NFKD', y.poster).encode('ascii','ignore'))
				imge[i]=img
				i+=1
			else:
				continue
	return render_to_response('praj2.html',{'imge':imge}	)
	
# Create your views here.