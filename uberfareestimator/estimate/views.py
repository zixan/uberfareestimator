from django.shortcuts import render
from pymongo import MongoClient
import requests
import pprint
import re

mobile_agents = ["midp", "j2me", "avantg", "docomo", "novarra", "palmos", 
					"palmsource", "240x320", "opwv", "chtml", "pda", "windows ce", 
					"mmp/", "blackberry", "mib", "symbian", "wireless", "nokia", 
					"hand", "mobi", "phone", "cdm", "up.b", "audio", "SIE-", 
					"samsung", "HTC", "mot-", "mitsu", "sagem", "sony", "alcatel", 
					"lg", "erics", "vx", "NEC", "philips", "mmm", "panasonic", 
					"sharp", "wap", "sch", "rover", "pocket", "benq", "java", "pt", 
					"pg", "vox", "amoi", "bird", "compal", "kg", "voda", "sany", 
					"kdd", "dbt", "sendo", "sgh", "gradi", "jb", "moto", "android",
					"Android", "iPhone"]

def is_mobile(request):
	user_agent = request.META['HTTP_USER_AGENT']
	for mobile_agent in mobile_agents:
		if mobile_agent in user_agent:
			return True
	return False

def is_ipad(request):
	user_agent = request.META['HTTP_USER_AGENT']
	if 'iPad' in user_agent:
		return True
	return False

def home(request):
	context = {
		'price_estimates':price_estimates(request=request),
		'is_mobile':is_mobile(request=request)
	}
	return render(request, 'estimate/index.html', context)

def price_estimates(request):

	if 'startlat' in request.GET and \
		'startlng' in request.GET and \
		'endlat' in request.GET and \
		'endlng' in request.GET and \
		'start_address' in request.GET and \
		'end_address' in request.GET:
		startlat = request.GET['startlat']
		startlng = request.GET['startlng']
		endlat = request.GET['endlat']
		endlng = request.GET['endlng']
		start_address = request.GET['start_address']
		end_address = request.GET['end_address']
	else:
		return {'prices':[], 'start_address':'', 'end_address':'', 'queried':False}

	url = 'https://api.uber.com/v1/estimates/price'
	parameters = {
		'server_token': os.environ.get('server_token'),
		'start_latitude': startlat,
		'start_longitude': startlng,
		'end_latitude': endlat,
		'end_longitude': endlng,
	}
	
    response = requests.get(url, params=parameters)
	data = response.json()
	data['start_address'] = start_address
	data['end_address'] = end_address
	data['queried'] = True
	return data
