from processor import *
import multiprocessing
import dns.resolver
import requests 
import json
import time

OFF = '\033[0m'		# Turn off coloring
BLD = '\033[1m'		# Make bold
RED = '\033[31m'	# Red
GRN = '\033[32m'	# Green
YEL = '\033[33m'	# Yellow
NAV = '\033[34m' 	# navy blue
BLU = '\033[36m' 	# cyan/light blue
PRP = '\033[35m'	# Purple

phishfood = 'https://openphish.com/feed.txt'

def clean_name(domain):
	return domain.split('://')[1].split('/')[0]


def get_list():
	r = requests.get(phishfood)
	if r.status_code != 200:
		print(f'[X] Unable to get feed from {phishfood} [STATUS:{r.status_code}]')
		exit()
	badhosts = r.text.split('\n')
	badhosts.pop(-1)  # last entry is an empty line
	return badhosts


def most_pages(phishers:dict):
	most = 0; host = ''
	for h in phishers.keys():
		n = len(phishers[h])
		if n > most:
			host = h  
			most = len(phishers[h])
	return host, most

def lookup_ip(domain):
	domain = clean_name(domain)
	return dns.resolver.resolve(domain, 'A')[0].address

def whos_fishing(badhosts):
	lookups = {}
	domains = {}
	# threads = multiprocessing.Pool(nthreads)
	dns.resolver.Timeout(10)
	for website in badhosts:
		try:
			lookups[website] = lookup_ip(website)
			print(f'{BLD}[$] {BLU}{website}{BLD}->{GRN}{lookups[website]}{OFF}')
			if lookups[website] not in domains.keys():
				domains[lookups[website]] = [website]
			else:
				domains[lookups[website]].append(website)
		except dns.resolver.NXDOMAIN:
			print(f'{BLD}[X] {RED}Domain {YEL}{website}{RED} cannot be resolved{OFF}')
			pass
		except dns.resolver.LifetimeTimeout:
			print(f'{BLD}[X] {RED}Timed Out waiting to resolve Domain {YEL}{website}{OFF}')
			pass
		except dns.resolver.NoAnswer:
			print(f'{BLD}[?] {RED}Did not receive a reply resolving {YEL}{website}{OFF}')
			pass
		except dns.resolver.NoNameservers:
			print(f'{BLD}[?] {RED}Did not receive a reply resolving {YEL}{website}{OFF}')
			pass
		except KeyboardInterrupt:
			print('[~] Quitting')
			exit()
		except:
			print(f'{BLD}[!] {RED}Error resolving {YEL}{website}{OFF}')
			pass
	return lookups, domains

if __name__ == '__main__':
	ld, lt = create_timestamp()
	bad_pages = get_list()
	print(f'{BLD}[+] Downloaded list of {RED}{len(bad_pages)}{OFF}{BLD}' \
		  f' suspicious pages from {GRN}{phishfood}{OFF}')
	
	# look up IP addresses of these suspected phishing pages
	domains, phishers = whos_fishing(bad_pages)

	most_sus, N = most_pages(phishers)
	banner = '='*40
	print(f'{BLD}{banner}{OFF}')
	print(f'{BLD}{YEL}{most_sus}{BLD} is hosting most phishing sites {BLU}[{N} sites]{OFF}')
	print(f'{BLD}{banner}{OFF}')

	phishing_data = {}
	threads = multiprocessing.Pool(25)
	for IP in phishers.keys():
		pages = phishers[IP]
		print(f'{BLD}[~] Processing results from {BLU}{len(pages)}{BLD} pages hosted by {GRN}{IP}{OFF}')
		data = {}
		for site in pages:
			# data[site] = process_page(site)
			try:
				event = threads.apply_async(process_page, (site,))
				data[site] = event.get(5)
			except multiprocessing.TimeoutError:
				pass
		phishing_data[IP] = data

	# save the results
	print(f'{BLD}[{ld} {lt}] {GRN}FINISHED ')
	if not os.path.isdir(os.path.join(os.getcwd(),'data')):
		os.mkdir('data')
	filename = f"data/{'phish_food'}_{ld.replace('/','-')}_{lt.replace(':','_')}.json"
	open(filename,'w').write(json.dumps(phishing_data,indent=2))
	print(f'[+] Data saved to {filename}')
