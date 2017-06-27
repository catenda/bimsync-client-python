import urllib
import urllib2
import webbrowser
import json
import datetime
import glob
import os
import json
import time

API_BASE_URL = 'https://api.bimsync.com/1.0/'
API_BETA_URL = 'https://api.bimsync.com/beta/'
BASE_APP_URL = 'http://localhost:8000/bimsync'
REDIRECT_URL = 'http://localhost:8000/bimsync/code'

# Replace these variables with your app credentials and projectId
CLIENT_ID='aaaa' change_me                    # Put your client id here
CLIENT_SECRET= 'bbbbbb' change_me                # Put your client secret here
CODE = "ccc" change_me
ACCESS_TOKEN = "access_token_here" change_me

#Insert your own project_id
PROJECT_ID = "project_id_guid" change_me
REVISION_ID = ""

def GetAuthorized():	
	a_url = 'https://api.bimsync.com/1.0/oauth/authorize?client_id=' + CLIENT_ID +'&redirect_uri=' + REDIRECT_URL + '&state=1&response_type=code'
	print(a_url) 
	webbrowser.open(a_url)


def getFirst(iterable, default=None):
	if iterable:
		for item in iterable:
			return item
	return default


def getAccessToken(code_):
	url = API_BASE_URL + 'oauth/access_token'
	post_fields = { "grant_type": "authorization_code",
					"code": code_,
					"client_id": CLIENT_ID,
					"client_secret": CLIENT_SECRET}

	request = urllib2.Request(url, urllib.urlencode(post_fields).encode('utf-8'), { "Content-Type": "application/x-www-form-urlencoded"})
	data = urllib2.urlopen(request).read().decode('utf-8')
	return json.loads(data)['access_token']



def getProjects(access_token):
	url = API_BASE_URL + 'projects'
	request = urllib2.Request(url, None, { "Authorization": "Bearer " + access_token})

	data = urllib2.urlopen(request).read().decode('utf-8')
	projects = json.loads(data)
	return projects

def getModelsInProject(access_token, project_id):
	url = API_BASE_URL + 'models' + "?" + "project_id=" + project_id
	request = urllib2.Request(url, None, { "Authorization": "Bearer " + access_token})

	data = urllib2.urlopen(request).read().decode('utf-8')
	models = json.loads(data)
	return models



def getFirstProjectId(access_token):
	for project in getProjects(access_token):
		print(project['name'].encode('utf-8'))
		return project['id']

def getViewer(access_token, projectId):
	url = API_BASE_URL + 'viewer/access?project_id=' + projectId
	request = urllib2.Request(url, "".encode('utf-8'), { "Authorization": "Bearer " + access_token})
	data = urllib2.urlopen(request).read().decode('utf-8')
	viewerToken = json.loads(data)
	return viewerToken['token']

def getViewer2d(access_token, projectId):
	url = API_BETA_URL + 'viewer2d/access?project_ref=' + projectId
	request = urllib2.Request(url, "".encode('utf-8'), { "Authorization": "Bearer " + access_token})
	data = urllib2.urlopen(request).read().decode('utf-8')
	viewer2dToken = json.loads(data)
	return viewer2dToken['url']
	
def makeProject(access_token, project_name):
	url = API_BASE_URL + "projects/new"
	data_dict = {"name": project_name}
	data = json.dumps(data_dict)

	request = urllib2.Request(url, data, { "Authorization": "Bearer " + access_token})
	response = urllib2.urlopen(request).read().decode('utf-8')
	return response

	
def makeModel(access_token, project_id, model_name):
	query = urllib.urlencode({"project_id": project_id})
	url = API_BASE_URL + "models/new"+"?"+query
	data_dict = {"name": model_name}
	data = json.dumps(data_dict)

	request = urllib2.Request(url, data, { "Authorization": "Bearer " + access_token})
	response = urllib2.urlopen(request).read().decode('utf-8')
	return response
	
def uploadModel(access_token, model_id, file_name, comment, data, callback_uri = None):
	query_data = {
	"model_id": model_id,
	"file_name": file_name,
	"comment": "Comment: "+comment,
	#"callback_uri": callback_uri
	}
	query = urllib.urlencode(query_data)
	url = API_BASE_URL + "model/import"+"?"+query
	print("URL: "+ url)

	request = urllib2.Request(url, data, { "Authorization": "Bearer " + access_token})
	request.get_method = lambda: 'PUT'
	response = urllib2.urlopen(request).read().decode('utf-8')
	return response
	
def getViewer3Dtoken(access_token, project_id):
	param = "project_id=" + project_id
	url = API_BASE_URL + "viewer/access"+"?"+param
	request = urllib2.Request(url, "", { "Authorization": "Bearer " + access_token})
	response = urllib2.urlopen(request).read().decode('utf-8')
	return response

def getViewer2Dtoken(access_token, project_id):
	param = "project_id=" + project_id
	url = API_BASE_URL + "viewer/access"+"?"+param
	request = urllib2.Request(url, "", { "Authorization": "Bearer " + access_token})
	response = urllib2.urlopen(request).read().decode('utf-8')
	return response

def getModelExport(access_token, model_id):
	param = "model_id=" + model_id #+ "&revision_id=1"
	url = API_BASE_URL + "revision/export"+"?"+param
	print "===> " + url
	request = urllib2.Request(url, "", { "Authorization": "Bearer " + access_token})
	response = urllib2.urlopen(request).read().decode('utf-8')
	return response

def getObjectsOfType(access_token, project_id, types, per_page, page, attributes = False, definedBy = False):
	data_dict = {"type": types, "attributes": attributes, "definedBy": definedBy} 
	data = json.dumps(data_dict)
	url = API_BASE_URL + 'project/products' + "?" + "project_id=" + project_id + "&page=" + str(page) + "&per_page=" + str(per_page)
	request = urllib2.Request(url, data, { "Authorization": "Bearer " + access_token})

	answer = urllib2.urlopen(request).read().decode('utf-8')
	objects = json.loads(answer)

	return objects


def getPropertiesOfObject(access_token, project_id):
	url = API_BASE_URL + 'models' + "?" + "project_id=" + project_id
	data_dict = {"name": project_name}
	data = json.dumps(data_dict)
	request = urllib2.Request(url, data, { "Authorization": "Bearer " + access_token})

	answer = urllib2.urlopen(request).read().decode('utf-8')
	properties = json.loads(answer)
	return properties

def niceModelName(originalWithPathAndExtension):
	return os.path.basename(originalWithPathAndExtension) 

def uploadIfcFolderToNewModels(folderPathWithFilter):
	"""
	#TODO: make next upload wait for previous to finish by asking for status by upload-token
	#folderPathWithFilter ser slik ut "d:/diverse_store_filer/Campus_Aas_CONFIDENTIAL/Mappe2--Campus_Aas_BIM-files/*.ifc"
	"""
	filene = glob.glob(folderPathWithFilter)

	for f in filene:
		#create a model
		pent_navn = niceModelName(f)
		print pent_navn	
		model_guid_jsonstring = makeModel(ACCESS_TOKEN, PROJECT_ID, pent_navn)
		model_json = json.loads(model_guid_jsonstring)
		model_id = model_json["id"]
		print "model_id = " + model_id

		#upload a file	
		ifc_data = open(f, 'r').read()	
		print uploadModel(ACCESS_TOKEN, model_id, pent_navn, "", ifc_data)
		time.sleep(25*60) #every 25 minutes


#GetAuthorized()
#ACCESS_TOKEN = getAccessToken(CODE)
#print("\nAccess token: " + ACCESS_TOKEN)


per_page = 50
page = 1
types = [ "IfcDoor", "IfcWall" ]
objects = getObjectsOfType(ACCESS_TOKEN, PROJECT_ID, types, per_page, page, True, True)
print json.dumps(objects, indent=4, sort_keys=True)

