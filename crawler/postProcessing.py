#!/usr/bin/python2.7
'''
    assign random lat long to a username based on a defined point
'''
import csv
import requests
import json
from time import sleep
import random


def main(docu):
    lat = 0
    long = 0
    f = open(docu)
    r = csv.reader(f)
    x = r.next()
    x.append('lat')
    x.append('long')
    bigcounter = 1000
    waitCounter = 0
    all=[]
    all.append(x)
    for item in r:
        if item[16] == '':
            #default to Taipei
            item[16] = 'taipei'
            lat = 25.0329636
            long = 121.5654268
        else:
            url = 'http://maps.googleapis.com/maps/api/geocode/json?address=' + item[16]
            response = requests.get(url)
            newDict = json.loads(response.text)
            if newDict['status'] == 'ZERO_RESULTS':
                #geocode cant get lat/long, so we are defaulting to taipei too
                item[16] = 'taipei'
                lat = 25.0329636
                long = 121.5654268
            else:
                try:
                    lat = newDict['results'][0]['geometry']['location']['lat']
                    long = newDict['results'][0]['geometry']['location']['lng']
                except:
                    item[16] = 'taipei'
                    lat = 25.0329636
                    long = 121.5654268
        #adding some randomness to the location
        randlat = (float(random.randint(0,50))/float(random.randint(100,1000))) * pow(-1,random.randint(1,2))
        randlong = (float(random.randint(0, 50))/float(random.randint(100, 1000))) * pow(-1,random.randint(1,2))
        item.append(lat + randlat)
        item.append(long + randlong)
        all.append(item)
        #counter to add a little wait to avoid api limit
        if waitCounter > 5:
            print('done with 7 more, sleeping to not appear botty... ' + str(bigcounter) + ' more to go!')
            sleep(30)
            waitCounter = 0
        else:
            waitCounter = waitCounter + 1
        bigcounter = bigcounter - 1

    with open('output.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile)
        for item in all:
            spamwriter.writerow(item)
    print(all)


if __name__ == '__main__':
        main('profiles1.csv')




