#!/usr/bin/python3

import json
import requests
import threading
from requests.auth import HTTPDigestAuth
import pprint

pp = pprint.PrettyPrinter()

# envoy-s host IP
host = '192.168.1.100'
# envoy installer password
password = '<INSTALLER PASSWORD>'

user = 'installer'
auth = HTTPDigestAuth(user, password)
marker = b'data: '

# curl --digest --user installer:27B2339b http://192.168.1.148/stream/meter

def scrape_stream():
	while True:
		try:
			url = 'http://%s/stream/meter' % host
			stream = requests.get(url, auth=auth, stream=True, timeout=5)
			for line in stream.iter_lines():
				if line.startswith(marker):
					data = json.loads(line.replace(marker, b''))
					#pp.pprint(data)
					prod=data['production']['ph-a']['p']+data['production']['ph-b']['p']+data['production']['ph-c']['p']
					cons=data['total-consumption']['ph-a']['p']+data['total-consumption']['ph-b']['p']+data['total-consumption']['ph-c']['p']
					net=data['net-consumption']['ph-a']['p']+data['net-consumption']['ph-b']['p']+data['net-consumption']['ph-c']['p']
					print(f"{data['total-consumption']['ph-a']['v'] :3.0f}V/{data['total-consumption']['ph-b']['v'] :3.0f}V/{data['total-consumption']['ph-c']['v'] :3.0f}V {data['total-consumption']['ph-a']['i'] :4.1f}A/{data['total-consumption']['ph-b']['i'] :4.1f}A/{data['total-consumption']['ph-c']['i'] :4.1f}A Power {prod:5.0f}W-{cons:5.0f}W={net:5.0f}W (Prod-Cons=Net)")

		except requests.exceptions.RequestException as e:
			print('Exception fetching stream data: %s' % e)

def main():
	stream_thread = threading.Thread(target=scrape_stream)
#	stream_thread.setDaemon(True)
	stream_thread.start()

if __name__ == '__main__':
	main()
