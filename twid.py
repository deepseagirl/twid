import argparse
import json
import requests
''' TODO
		-v for all output
		format the timestamps a bit
'''
parser = argparse.ArgumentParser(description='twitter user wayback')
parser.add_argument('screen_name', type=str, help='target')
parser.add_argument('-v', help='verbose output (print all capture timestamps)', action='store_true', dest='verbose')

urls = []
user_ids = {}
args = parser.parse_args()
screen_name = args.screen_name
r = requests.get('https://web.archive.org/cdx/search/cdx?filter=mimetype:application/json&fl=timestamp,original&limit=-50&collapse=timestamp:7&url=twitter.com/%s/status/*'% str(screen_name))
search_results = r.text.splitlines()

for line in search_results:
	fields = line.split(" ")
	timestamp = fields[0]
	url = fields[1]
	urls.append((timestamp, url))

if not urls:
	print(" no usable captures found")
	exit()

print(" checking %s captures" % len(urls))
url_f = "https://web.archive.org/web/%s/%s"
for url_entry in urls:
	timestamp = url_entry[0]
	orig_url = url_entry[1]
	j = requests.get(url_f % (timestamp, orig_url))
	if j.text:
		json_entry = json.loads(j.text)
		user_id = json_entry["user"]["id"]
		if user_id not in user_ids:
			user_ids[user_id] = [timestamp]
		else:
			user_ids[user_id].append(timestamp)
print()
for user_id in user_ids:
	timestamps = user_ids[user_id]
	timestamps.sort()
	print("Twitter ID: %s" % user_id)
	print(" - appeared between %s and %s (%s occurences)" % (timestamps[0], timestamps[-1], len(timestamps)))
	if args.verbose:
		print(" - timestamps:\n ", timestamps)
	print()
if user_ids:
	print(" %s user id(s) found" % len(user_ids))
