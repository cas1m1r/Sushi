# Sushi
*exploring fresh (raw) phishing domains for threat intelligence*

Running `python3 chum.py` will first visit the OSINT source `https://openphish.com/feed.txt` and download the daily list
of their curated sources of suspicious pages. 

The code will make A Record requests for each domain, and create a dictionary of the phishing pages by IP Address.

Then each of the pages will be visited, and each page will be parsed to look for "malicious" content. 

![sushi_roll](https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fpluspng.com%2Fimg-png%2Fsushi-roll-png-sushi-png-image-576.png&f=1&nofb=1&ipt=6b9c82aba70fc24aef8b869cb36dacd6da60f5405b1dc80eec873b6271cc3942&ipo=images)


## NOTES
**Be careful using this project** as this is exploring potentially active malicious hosts. Pages will not be visited in
a browser, but you would be wise to still be vigilant of how you install or run this.

*As experimental software being developed openly for anyone to use/copy/modify, I am not responsible for what happens 
should you run this code. It is intended to be helpful in documenting malicious actors online.*