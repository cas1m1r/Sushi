# Sushi
*exploring fresh (raw) phishing domains for threat intelligence*

Running `python3 chum.py` will first visit the OSINT source `https://openphish.com/feed.txt` and download the daily list
of their curated sources of suspicious pages. 

The code will make A Record requests for each domain, and create a dictionary of the phishing pages by IP Address.

Then each of the pages will be visited, and each page will be parsed to look for "malicious" content. 

![sushi_roll](https://github.com/cas1m1r/Sushi/blob/main/sushi.png?raw=true)

## Organization 
Adding a component to collect/organize the data collected each day by using sqlite. Once you do this
it makes searching through the database much easier. For example, below you can see how you might
find pages specifically targeting a domain by searching through the URL field:
![sqlite](https://github.com/cas1m1r/Sushi/blob/main/rolled_up.jpg?raw=true)

## NOTES
**Be careful using this project** as this is exploring potentially active malicious hosts. Pages will not be visited in
a browser, but you would be wise to still be vigilant of how you install or run this.

*As experimental software being developed openly for anyone to use/copy/modify, I am not responsible for what happens 
should you run this code. It is intended to be helpful in documenting malicious actors online.*