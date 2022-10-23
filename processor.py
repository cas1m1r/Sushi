import requests 
import json
import time
import re

OFF = '\033[0m'
BLD = '\033[1m'
RED = '\033[31m'
BLU = '\033[32m'
YEL = '\033[33m'
GRN = '\033[34m'
PRP = '\033[35m'


def create_timestamp():
    date = time.localtime(time.time())
    mo = str(date.tm_mon)
    day = str(date.tm_mday)
    yr = str(date.tm_year)

    hr = str(date.tm_hour)
    min = str(date.tm_min)
    sec = str(date.tm_sec)

    date = mo + '/' + day + '/' + yr
    timestamp = hr + ':' + min + ':' + sec
    return date, timestamp

def process_page(website):
	results = {}
	try:
		scary = requests.get(website)
	except:
		print(f'[!] Error Processing {website}')
		return results
	response_size = len(scary.text)
	# build a dict for result
	results['url'] = website
	results['status'] = scary.status_code
	results['page_size'] = response_size
	results['cookies'] = scary.cookies.items()
	try:
		scary.close()
	except: 
		print(f'[!] Error Processing {website}')
		return results
	# Extract links
	links = []
	ai = [i.start() for i in re.finditer('href="', scary.text)]
	for index in ai:
		try:
			links.append(bad_page.text[index:].split('>')[0].split('href=')[1])
		except:
			pass
	if len(links):
		print(f'[+] {len(links)} links found on {website}')
	if len(results['cookies']):
		print(f'[+] {website} added cookies:{json.dumps(results["cookies"])}')
	results['links'] = links
	return results
