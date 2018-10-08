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
import operator
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
			try:
				rat=float(unicodedata.normalize('NFKD', x.imdbrating).encode('ascii','ignore'))
			except:

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
			try:
				rat=float(unicodedata.normalize('NFKD', x.imdbrating).encode('ascii','ignore'))
				ratings.append(rat)
				name.append(str(unicodedata.normalize('NFKD', x.title).encode('ascii','ignore')))
			except:
				continue

	ratings.sort(reverse=True)
	i=0
	
	imge={}
	for x in range(0,3):
		 mov1=MovieOmdb.objects(imdbrating=str(ratings[x]))
		 for y in mov1:
			rat=str(unicodedata.normalize('NFKD', y.imdbrating).encode('ascii','ignore'))
			title = str(unicodedata.normalize('NFKD', y.title).encode('ascii','ignore'))
			if title in name:
				img=str(unicodedata.normalize('NFKD', y.poster).encode('ascii','ignore'))
				imge[i]=img
				i+=1
			else:
				continue
	return render_to_response('base.html',{'imge':imge}	)


def addmovieomdb(request):
	name=str(request.POST['movname'])
	name=name.split()
	temp=""
	for x in range(0,len(name)-1):
		temp+=name[x]+"+"
	temp+=name[len(name)-1]


	url="http://www.omdbapi.com/?t="+temp+"&y=&plot=short&r=json"
	kundli = urllib2.urlopen(url).read()
	dic	 = JSONDecoder().decode(kundli)
	dic['twitterR']=str(request.POST['twrate'])
	if(dic['imdbRating']=="N/A"):
		dic['imdbRating']="5"
	kundlies = MovieOmdb.objects.create(
		title=dic['Title'].lower(),
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
	ftweet=open("ww.csv", "w+")
	f = csv.writer(ftweet)
	results=api.search(q=movname,count=200,lang="en")
	for result in results:	
	    #look for 2 or more repetitions of character and replace with the character itself
	    # pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
	    # res=pattern.sub(r"\1\1", result)
	    # res=re.sub(r'(.)\1{2,}', r'\1\1', str(result))    
	    f.writerow([result.text.encode('utf-8')])
	    #f.writerow([res.unicode('utf-8')])
	ftweet.close()


	return render_to_response('praj1.html')

def getrating(request):
	

	retcode =str( subprocess.check_output("Rscript stemming.R", shell=True))
	imge={}
	res=retcode.split()[1]
	imge[0]=float(res)

	return render_to_response('praj2.html',{'imge':imge})
def getname(request):
	global gen
	global act
	name1=str(request.POST['txtName'])
	#mov1=MovieOmdb.objects(title=str(name))
	name1="Harry Potter and the Goblet of Fire"
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
	#gen="Animation"
	#act="Jack Black"
	name1 = request.POST['movieName'].lower()
	mov1=MovieOmdb.objects(title=str(name1))

	imge11={}
	i=0
	for y in mov1:
			titles = str(unicodedata.normalize('NFKD', y.title).encode('ascii','ignore'))
		 	img=str(unicodedata.normalize('NFKD', y.poster).encode('ascii','ignore'))
		 	imge11[i]=img
		 	rat=float(unicodedata.normalize('NFKD', y.imdbrating).encode('ascii','ignore'))
		 	imge11[i+1]=rat
		 	act=str(unicodedata.normalize('NFKD', y.actors).encode('ascii','ignore'))
		 	imge11[i+2]=act
		 	gen=str(unicodedata.normalize('NFKD', y.genre).encode('ascii','ignore'))
		 	twr=float(unicodedata.normalize('NFKD', y.twitterrating).encode('ascii','ignore'))
		 	year=str(unicodedata.normalize('NFKD', y.year).encode('ascii','ignore'))
		 	imge11[i+3]=gen
		 	imge11[i+4]=float(twr+rat)/2
		 	imge11[i+5]=year
		 	imge11[i+6]=titles		 	
		 	i+=1

			
#test by kd ends
	try:
		mov_genre=gen
	except:
		return render_to_response('error.html',{'imge':"No Movie Found!!!!!"})
	mov_act = act
	mov_genre = mov_genre.split(',')
	name_actor=[]
	ratings_actor=[]
	name_genre=[]
	ratings_genre=[]
	rat_act={}
	rat_genre={}
	mov_act = mov_act.split(',')
	for mg in mov_genre:
		mov1=MovieOmdb.objects()
		for x in mov1:
			if name1==str(unicodedata.normalize('NFKD', x.title).encode('ascii','ignore')):
				continue
			gen=str(unicodedata.normalize('NFKD', x.genre).encode('ascii','ignore'))
			gen=gen.split(",")
			if mg in gen:
				act=str(unicodedata.normalize('NFKD', x.actors).encode('ascii','ignore'))
				act = act.split(',')
				if act[0] in mov_act:
					rat=float(unicodedata.normalize('NFKD', x.imdbrating).encode('ascii','ignore'))
					rat1=float(unicodedata.normalize('NFKD', x.twitterrating).encode('ascii','ignore'))
					rat=(rat+rat1)/2
					ratings_actor.append(rat)
					name_mov=str(unicodedata.normalize('NFKD', x.title).encode('ascii','ignore'))
					rat_act[name_mov]=float(rat)
				else:
					rat=float(unicodedata.normalize('NFKD', x.imdbrating).encode('ascii','ignore'))
					rat1=float(unicodedata.normalize('NFKD', x.twitterrating).encode('ascii','ignore'))
					rat=(rat+rat1)/2
					ratings_genre.append(rat)
					name_mov=str(unicodedata.normalize('NFKD', x.title).encode('ascii','ignore'))
					name_genre.append(name_mov)
					rat_genre[name_mov]=int(rat)
	ratings_actor.sort(reverse=True)
	ratings_genre.sort(reverse=True)
	try:
		act_first=max(rat_act.iteritems(), key=operator.itemgetter(1))[0]
	except:
		act_first=""
	try:
		genre_first=max(rat_genre.iteritems(), key=operator.itemgetter(1))[0]
	except:
		genre_first=""
	imge={}
	i=0
	j=3
	mov1=MovieOmdb.objects(title=act_first)
	for y in mov1:
		img=str(unicodedata.normalize('NFKD', y.poster).encode('ascii','ignore'))
		imge[i]=img
		i+=1
		imge[j]=str(unicodedata.normalize('NFKD', y.title).encode('ascii','ignore'))
		j+=1
	k=1
	try:
		del rat_act[act_first]
	except:
		k=0
	if(k==1):
		ran=2
	else:
		ran=3
	for _ in range(0,ran):
		try:
			act_first=max(rat_act.iteritems(), key=operator.itemgetter(1))[0]
			act_first_rat=max(rat_act.iteritems(), key=operator.itemgetter(1))[1]
		except:
			act_first=""
			act_first_rat=-1
		try:
			genre_first=max(rat_genre.iteritems(), key=operator.itemgetter(1))[0]
			genre_first_rat=max(rat_genre.iteritems(), key=operator.itemgetter(1))[1]
		except:
			genre_first=""
			genre_first_rat=-1
		
		if(act_first_rat>genre_first_rat):
			mov1=MovieOmdb.objects(title=act_first)
			for y in mov1:
				img=str(unicodedata.normalize('NFKD', y.poster).encode('ascii','ignore'))
				imge[i]=img
				i+=1
				imge[j]=str(unicodedata.normalize('NFKD', y.title).encode('ascii','ignore'))
				j+=1
			del rat_act[act_first]
		else:
			mov1=MovieOmdb.objects(title=genre_first)
			for y in mov1:
				img=str(unicodedata.normalize('NFKD', y.poster).encode('ascii','ignore'))
				imge[i]=img
				i+=1
				imge[j]=str(unicodedata.normalize('NFKD', y.title).encode('ascii','ignore'))
				j+=1
			del rat_genre[genre_first]
	
	new_imge={}
	new_imge[0]=imge11
	new_imge[1]=imge	
	return render_to_response('main.html',{'imge':new_imge})
		
# Create your views here.