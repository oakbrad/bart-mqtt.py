# bart-mqtt.py
Get real time departures for specified BART train stations and publish to MQTT. Payload is in JSON.

Change MQTT information and list stations you want to monitor.

# Sample Output
```
BART/LAKE/North/Daly City ["9", "18", "29"]
BART/LAKE/North/Richmond ["3", "23", "43"]
BART/LAKE/South/Dublin-Pleasanton ["15", "35", "55"]
BART/LAKE/South/Fremont ["3", "24", "45"]
BART/LAKE/South/Warm Springs ["Leaving", "20", "40"]
BART/16TH/North/Dublin-Pleasanton ["15", "35"]
BART/16TH/North/Fremont ["6", "27", "44"]
BART/16TH/North/Pittsburg-Bay Point ["9", "28", "48"]
BART/16TH/North/Richmond ["Leaving", "20", "40"]
BART/16TH/South/Daly City ["3", "6", "10"]
BART/16TH/South/SFO-Millbrae ["13", "33", "53"]
```

# Dependencies
* lxml==4.1.1
* paho-mqtt==1.3.1
* requests==2.18.4
* simplejson==3.13.2
* xmltodict==0.11.0
