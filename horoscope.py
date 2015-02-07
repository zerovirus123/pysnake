import urllib2
from BeautifulSoup import BeautifulSoup
from itertools import takewhile, chain 

horoscope_list = [ "Aries", "Tauros", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

urls = [
	"http://my.horoscope.com/astrology/free-daily-horoscope-aries.html",
	"http://my.horoscope.com/astrology/free-daily-horoscope-taurus.html",
	"http://my.horoscope.com/astrology/free-daily-horoscope-gemini.html",
	"http://my.horoscope.com/astrology/free-daily-horoscope-cancer.html",
	"http://my.horoscope.com/astrology/free-daily-horoscope-leo.html",
	"http://my.horoscope.com/astrology/free-daily-horoscope-virgo.html",
	"http://my.horoscope.com/astrology/free-daily-horoscope-libra.html",
	"http://my.horoscope.com/astrology/free-daily-horoscope-scorpio.html",
	"http://my.horoscope.com/astrology/free-daily-horoscope-sagittarius.html",
	"http://my.horoscope.com/astrology/free-daily-horoscope-capricorn.html",
	"http://my.horoscope.com/astrology/free-daily-horoscope-aquarius.html",
	"http://my.horoscope.com/astrology/free-daily-horoscope-pisces.html"
	]

def getData(horoscope):

    if horoscope == "Aries":
        data = urllib2.urlopen( urls[0] )	
	soup = BeautifulSoup(data)
	for words in soup.findAll(id='textline'):
	    print words.next, words.next_sibling
	
    if horoscope == "Tauros":	
        data = urllib2.urlopen( urls[1] )	
	soup = BeautifulSoup(data)
	for words in soup.findAll(id='textline'):
	    print words.next, words.next_sibling

    if horoscope == "Gemini":
        data = urllib2.urlopen( urls[2] )	
	soup = BeautifulSoup(data)
	for words in soup.findAll(id='textline'):
	    print words.next, words.next_sibling

    if horoscope == "Cancer":
        data = urllib2.urlopen( urls[3] )	
	soup = BeautifulSoup(data)
	for words in soup.findAll(id='textline'):
	    print words.next, words.next_sibling

    if horoscope == "Leo":
        data = urllib2.urlopen( urls[4] )	
	soup = BeautifulSoup(data)
	for words in soup.findAll(id='textline'):
	    print words.next, words.next_sibling

    if horoscope == "Virgo":
        data = urllib2.urlopen( urls[5] )	
	soup = BeautifulSoup(data)
	for words in soup.findAll(id='textline'):
	    print words.next, words.next_sibling

    if horoscope == "Libra":
        data = urllib2.urlopen( urls[6] )	
	soup = BeautifulSoup(data)
	for words in soup.findAll(id='textline'):
	    print words.next, words.next_sibling

    if horoscope == "Scorpio":
        data = urllib2.urlopen( urls[7] )	
	soup = BeautifulSoup(data)
	for words in soup.findAll(id='textline'):
	    print words.next, words.next_sibling

    if horoscope == "Sagittarius":
        data = urllib2.urlopen( urls[8] )	
	soup = BeautifulSoup(data)
	for words in soup.findAll(id='textline'):
	    print words.next, words.next_sibling

    if horoscope == "Capricorn":
        data = urllib2.urlopen( urls[9] )	
	soup = BeautifulSoup(data)
	for words in soup.findAll(id='textline'):
	    print words.next, words.next_sibling

    if horoscope == "Aquarius":
        data = urllib2.urlopen( urls[10])	
	soup = BeautifulSoup(data)
	for words in soup.findAll(id='textline'):
	    print words.next, words.next_sibling

    if horoscope == "Pisces":	
        data = urllib2.urlopen( urls[11] )	
	soup = BeautifulSoup(data)
	for words in soup.findAll(id='textline'):
	    print words.next, words.next_sibling

	
getData



def main():

    invalidChoice = True

    while invalidChoice is True:
       horoscope = raw_input("Enter your horoscope.\n")
       if horoscope in horoscope_list:
		invalidChoice = False
       if invalidChoice is True:
	    print "Invalid Choice. Please Retry"

    getData(horoscope)

main()
