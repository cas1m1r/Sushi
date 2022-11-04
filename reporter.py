from dotenv import load_dotenv
from processor import *
import sys
import os

load_dotenv()

API = os.environ["KEY"]
api = f'https://api.abuseipdb.com/api/v2/report'


def report_addr(ip,categories,comment):
	cat = ''
	for c in categories:
		cat += f'{c},'
	cmd =  f'curl {api} --data-urlencode "ip={ip}" -d categories={c}'
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
