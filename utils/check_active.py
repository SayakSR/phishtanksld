import urllib.request

def check_url(url):	
	try:
		activecode=urllib.request.urlopen(str(url)).getcode()
	except:
		activecode=404
	if(activecode==200):
		return True
	else:
		return False


