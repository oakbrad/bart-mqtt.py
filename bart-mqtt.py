#
# http://api.bart.gov/docs/overview/index.aspx
#
# Publish real time estimates for specified train stations
# Payload in JSON format
#
# Thanks to this for the  example!
# https://github.com/rdhyee/consuming-apis-with-python/blob/master/BART.py
#


import requests
import urllib
from lxml.etree import fromstring
import xmltodict
import simplejson as json
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

#
# SETUP
#
# Get yr own  http://api.bart.gov/api/register.aspx
BART_API_KEY = "MW9S-E7SL-26DU-VV8V"
# MQTT Authorization
mqtt_host = "localhost"
MQTT_AUTH = {
    'username':'XXX',
    'password':'XXX'
}
# Stations checked by abbreviation
# https://api.bart.gov/docs/overview/abbrev.aspx
myStations = ["12th","lake","16th"]


def etd(orig, dir="n", key=BART_API_KEY):
    url = "http://api.bart.gov/api/etd.aspx?" +  \
            urllib.urlencode({'cmd':'etd',
                              'orig':orig,
                              'key':key,'dir':dir})
    # print url
                                                                  
    r = requests.get(url)
    return r.content

def bsa(orig="all", key=BART_API_KEY):
    url = "http://api.bart.gov/api/bsa.aspx?" +  \
            urllib.urlencode({'cmd':'bsa',
                              'orig':orig,
                              'key':key})
    # print url
                                                                  
    r = requests.get(url)
    return r.content

def elev(key=BART_API_KEY):
    url = "http://api.bart.gov/api/bsa.aspx?" +  \
            urllib.urlencode({'cmd':'elev',
                              'key':key})
    # print url
                                                                  
    r = requests.get(url)
    return r.content

#
# Get service information
#
response = xmltodict.parse(elev())
bartElevator = response['root']['bsa']['description']
topic = "BART/Service/Elevator"
payload = json.dumps(bartElevator)
publish.single(topic,payload=payload,hostname=mqtt_host,client_id="bartbot",auth=MQTT_AUTH,port=1883,protocol=mqtt.MQTTv311)
#print topic + " " + payload

response = xmltodict.parse(bsa())
bartService = response['root']['bsa']['sms_text']
payload = json.dumps(bartService)
topic = "BART/Service/Advisory"
publish.single(topic,payload=payload,hostname=mqtt_host,client_id="bartbot",auth=MQTT_AUTH,port=1883,protocol=mqtt.MQTTv311)
#print topic + " " + payload

northDepartures = []
southDepartures = []

for station in myStations:
    response = xmltodict.parse(etd(station,"n"))
    northbound = response['root']['station']['etd']
    thisStation = response['root']['station']['abbr']
    response = xmltodict.parse(etd(station,"s"))
    southbound = response['root']['station']['etd']
    response = xmltodict.parse(bsa(station))
    thisAdvisory = response['root']['bsa']['sms_text']

    topic = "BART/" + thisStation + "/Advisory "
    payload = json.dumps(thisAdvisory)
#    print "BART/" + thisStation + "/Advisory " + payload
    publish.single(topic,payload=payload,hostname=mqtt_host,client_id="bartbot",auth=MQTT_AUTH,port=1883,protocol=mqtt.MQTTv311)

    for train in northbound:
       thisTrain = train['destination'].replace("/","-") 
    
       thisDeparture = []
       for departure in train['estimate']:
           thisDeparture.append(departure['minutes']) 
           payload = json.dumps(thisDeparture) 
           
           time = departure['minutes']
	   if "Leaving" not in time: northDepartures.append(time)

#           print "BART/" + thisStation + "/North/" + thisTrain + " " + payload
       topic = "BART/" + thisStation + "/North/" + thisTrain
       publish.single(topic,payload=payload,hostname=mqtt_host,client_id="bartbot",auth=MQTT_AUTH,port=1883,protocol=mqtt.MQTTv311)

    northDepartures = list(set(northDepartures))
    northDepartures = [int(x) for x in northDepartures]
    northDepartures.sort()
    allpayload = json.dumps(northDepartures)
    alltopic = "BART/" + thisStation + "/North/All"
    publish.single(alltopic,payload=allpayload,hostname=mqtt_host,client_id="bartbot",auth=MQTT_AUTH,port=1883,protocol=mqtt.MQTTv311)
    northDepartures = []

    for train in southbound:
       thisTrain = train['destination'].replace("/","-")

       thisDeparture = []
       for departure in train['estimate']:
           thisDeparture.append(departure['minutes']) 
           payload = json.dumps(thisDeparture)

           time = departure['minutes']
           if "Leaving" not in time: southDepartures.append(time)
 
#       print "BART/" + thisStation + "/South/" + thisTrain + " " + payload
       topic = "BART/" + thisStation + "/South/" + thisTrain
       publish.single(topic,payload=payload,hostname=mqtt_host,client_id="bartbot",auth=MQTT_AUTH,port=1883,protocol=mqtt.MQTTv311)

    # Format list
    # Remove duplicates
    southDepartures = list(set(southDepartures))
    # Make all integers
    southDepartures = [int(x) for x in southDepartures]
    # Sort high to low
    southDepartures.sort()
    # Convert to JSON
    allpayload = json.dumps(southDepartures)
    alltopic = "BART/" + thisStation + "/South/All"
    publish.single(alltopic,payload=allpayload,hostname=mqtt_host,client_id="bartbot",auth=MQTT_AUTH,port=1883,protocol=mqtt.MQTTv311)
    southDepartures = []

