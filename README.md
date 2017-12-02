# bart-mqtt.py
Get real time departures for specified BART train stations and publish to MQTT. Payload is in JSON.

Change MQTT information and list stations you want to monitor.

# Sample Output
```
BART/Service/Elevator "There is 1 elevator out of service at this time: WARM: Concourse (East) - Walkway"
BART/Service/Advisory "No delays reported."
BART/12TH/Advisory  "No delays reported."
BART/12TH/North/Pittsburg-Bay Point ["1", "22", "42"]
BART/12TH/North/Richmond ["2", "14", "22"]
BART/12TH/South/Daly City ["2", "21", "41"]
BART/12TH/South/SFO-Millbrae ["11", "31", "51"]
BART/12TH/South/Warm Springs ["14", "34", "54"]
BART/LAKE/Advisory  "No delays reported."
BART/LAKE/North/Daly City ["5", "15", "25"]
BART/LAKE/North/Richmond ["19", "39", "59"]
BART/LAKE/South/Dublin-Pleasanton ["11", "31", "51"]
BART/LAKE/South/Fremont ["19", "39", "59"]
BART/LAKE/South/Warm Springs ["16", "36", "56"]
```

# Dependencies
* lxml==4.1.1
* paho-mqtt==1.3.1
* requests==2.18.4
* simplejson==3.13.2
* xmltodict==0.11.0
