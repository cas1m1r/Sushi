import requests 
import sqlite3
import pandas
import json
import time
import sys
import os
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


def load_db():
	return sqlite3.connect('phishers.db')

def save_db(db):
	db.commit()
	db.close()

def create_table():
	scammers = load_db()
	# Creating table
	create_table = """ CREATE TABLE phishing_pages (
		            IP TEXT NOT NULL,
		            URL TEXT NOT NULL,
		            LINK TEXT NOT NULL,
		            STATUS INT NOT NULL,
		            COOKIES TEXT NOT NULL
		        ); """
	cursor = scammers.cursor()
	cursor.execute(create_table)
	cursor.close()
	save_db(scammers)

def insert_row(ip, data):
	scammers = load_db()
	cursor = scammers.cursor()
	if len(data.keys()) > 1:
		for link in data.keys():
			d = data[link]
			if 'url' not in d.keys():
				continue
			try:
				cookies = f"[{json.dumps(d['cookies'])}]"
			except KeyError:
				cookies = '[]'
				pass
			try:
				links = f"[{json.dumps(d['links'])}]"
			except:
				links = '[]'
				pass
			row = f"('{ip}', '{d['url']}', '{links}', '{d['status']}', '{cookies}')"
			cmd = f"INSERT INTO phishing_pages VALUES {row}"
			print(f'Trying to run SQL Command:\n{cmd}')
			cursor.execute(cmd)		
	elif len(data.keys()):
		
		d = data[list(data.keys()).pop()]

		try:
			cookies = f"[{json.dumps(d['cookies'])}]"
		except KeyError:
			cookies = '[]'
			pass
		try:
			links = f"[{json.dumps(d['links'])}]"
		except:
			links = '[]'
			pass
		try:
			row = f"('{ip}', '{d['url']}', '{links}', '{d['status']}', '{cookies}')"
			cmd = f"INSERT INTO phishing_pages VALUES {row}"
			print(f'Trying to run SQL Command:\n{cmd}')
			cursor.execute(cmd)
		except:
			pass
	cursor.close()
	save_db(scammers)

def main():
	if not os.path.isfile('phishers.db'):
		create_table()
	if len(sys.argv) > 1:
		data = json.loads(open(sys.argv[1],'r').read())
		for ip in data.keys():
			entry = data[ip]
			insert_row(ip, entry)

if __name__ == '__main__':
	main()
