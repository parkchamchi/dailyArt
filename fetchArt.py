#Fetch art from the Metropolitan Museum of Art API

import urllib.request as urlreq
import json
import random

apiurl = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
	
#This version only fetches European paintings
def fetchArt():
	#Get the objectID generator
	itr = getObjectIDGenerator()

	#Get the random art
	for objectID in itr:
		url = apiurl + "/%d" % objectID
		
		try:
			conn = urlreq.urlopen(url)
			art = json.loads(conn.read().decode("utf-8"))
		except:
			continue
		
		if (checkArt(art)):
			break

	return art

def getObjectIDGenerator():
	filename = "lib/objects"

	#try to open the json
	try:
		with open(filename, "r") as file:
			obj_json = json.load(file)
	except: #can't open it, make a new one
		print("Connecting the API for the first time.\nMay take some time...")

		#11 is departmentId for "European Paintings"
		#This hardcoding can be removed by manipulating
		#	https://collectionapi.metmuseum.org/public/collection/v1/departments
		#...but this seems sufficient.
		url = apiurl + "?departmentIds=%d" % 11

		conn = urlreq.urlretrieve(url, filename) #save it...
		with open(filename, "r") as file:
			obj_json = json.load(file) #and open it

	#The generator
	def objectIDGenerator():
		while True:
			yield obj_json["objectIDs"][random.randrange(0, obj_json["total"])]

	return objectIDGenerator()

def checkArt(art):
	if art["primaryImage"] == "":
		return False

	return True