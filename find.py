#!/usr/bin/python2.7
#
# Assignment3 Interface
# Name: Dhruv Misra 
#

from pymongo import MongoClient
import os
import sys
import json
import re
import math

def FindBusinessBasedOnCity(cityToSearch, saveLocation1, collection):
	docs = collection.find({"city": re.compile(cityToSearch, re.IGNORECASE)})
	f = open(saveLocation1,'w')
	for doc in docs:
		s1=doc['name'].upper()
		s2=doc['full_address'].replace('\n',' ').upper()
		s3=doc['city'].upper()
		s4=doc['state'].upper()
		s = s1+'$'+s2+'$'+s3+'$'+s4+'\n'
		f.write(s)

def FindBusinessBasedOnLocation(categoriesToSearch, myLocation, maxDistance, saveLocation2, collection):
	R = 3959
	lat1 = math.radians(float(myLocation[0]))
	lon1 = math.radians(float(myLocation[1]))
	docs = collection.find({})
	f = open(saveLocation2,'w')
	
	for doc in docs:
		lat2 = 0
		lon2 = 0
		lat2 = math.radians(float(doc['latitude']))
		lon2 = math.radians(float(doc['longitude']))
		name = doc['name']
		category = doc['categories']
		phi = math.radians(lat2-lat1)
		lam = math.radians(lon2-lon1)
		a = math.sin(phi/2) * math.sin(phi/2) + math.cos(lat1) * math.cos(lat2) * math.sin(lam/2) * math.sin(lam/2)
		c = math.degrees(2 * math.atan2(math.sqrt(a),math.sqrt(1-a)))
		d = R*c
		
		flag = 0
		for i in category:
			if i in categoriesToSearch:
				flag = 1
				break
		
		if d<=maxDistance and flag == 1:
			name = name.encode('utf-8').upper()
			f.write(name+'\n')
