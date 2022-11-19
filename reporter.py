from dotenv import load_dotenv
from processor import *
import time
import sys
import os

load_dotenv()

API = os.environ["KEY"]
api = f'https://api.abuseipdb.com/api/v2/report'

def load_db(database):
	return sqlite3.connect(database)

def look_for_scammers(term):
	db = load_db('phishers.db')
	hosts = []
	results = search_by_url(db, term)
	for result in results:
		ip = result[0]
		url = result[1]
		if ip not in hosts:
			print(f'{ip} is hosting {url}')
			hosts.append(ip)
	print(f'[+] Found {len(results)} pages searching for {term} hosted by {len(hosts)} IPs')
	# check if user wants to report hosts
	if input('Do you want to report These Hosts?').upper()=='Y':
		options = open('abuse_categories.txt','r').read()
		category = input(f'Enter a category:\n{options}\n')
		comment = input('Enter Comment for Report(s): ')
		for addr in hosts:
			report_addr(addr, int(category), comment)
			time.sleep(3) # dont want to thrash their api!

def report_addr(ip,cat,comment):
	cmd =  f'curl {api} --data-urlencode "ip={ip}" -d categories={cat}'
	cmd += f' --data-urlencode "comment={comment}"'
	cmd += f' -H "Key: {API}"'
	cmd += f' -H "Accept: application/json"'
	os.system(cmd)
	print(f'[+] {ip} has been reported to AbuseIPDB')

if __name__ == '__main__':
	default_category = f'15'
	default_comment = f'Naughty'
	if len(sys.argv) > 1:
		ip = sys.argv[1]
	if len(sys.argv) > 2:
		default_category = int(sys.argv[2])
	if len(sys.argv) > 3:
		default_comment = ' '.join(sys.argv[3:])
	# report the address to AbuseIPdb
	report_addr(ip, default_category, default_comment)