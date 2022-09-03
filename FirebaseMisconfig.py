#!/usr/bin/python3
import os
import sys
import ntpath
import time
import re
from urllib.parse import urlparse
from certifi import contents 
import urllib3
import hashlib
from icecream import ic
ic.configureOutput("DEBUG ‣ ")

rootDir=os.path.expanduser("~")+"/.SourceCodeAnalyzer/" #ConfigFolder ~/.SourceCodeAnalyzer/
projectDir=""
apkFilePath=""
apkFileName=""
firebaseProjectList=[]
inScoprUrls=[]
apkHash=""
apktoolPath="./Dependencies/apktool_2.3.4.jar"

def isNewInstallation():
	if (os.path.exists(rootDir)==False):
		print("new installation detected")
		os.mkdir(rootDir)
		return True
	else:
		return False

def isValidPath(apkFilePath):
	global apkFileName
	print("Checking if the APK file path is valid.")
	if (os.path.exists(apkFilePath)==False):
		print("Incorrect APK file path found. Please try again with correct file name.")
		exit(1)
	else:
		print("APK File Found.")
		apkFileName=ntpath.basename(apkFilePath)

def reverseEngineerApplication(apkFileName):
	global projectDir
	print("Initiating APK Decompilation Process.")
	projectDir=rootDir+apkFileName+"_"+hashlib.md5().hexdigest()
	if (os.path.exists(projectDir)==True):
		print("The same APK is already decompiled. Skipping decompilation and proceeding with scanning application.")
		return projectDir
	os.mkdir(projectDir)
	print("Decompiling the APK file using APKtool.")
	result=os.system("java -jar "+apktoolPath+" d "+"--output "+'"'+projectDir+"/apktool/"+'"'+' "'+apkFilePath+'"'+'>/dev/null')
	if (result!=0):
		print("Apktool failed with exit status "+str(result)+". Please Try Again.")
		exit(1)
	print("Successfully decompiled the application. Proceeding with enumeraing firebase peoject names from the application code.")

def findFirebaseProjectNames():
	global firebaseProjectList
	regex='https*://(.+?)\.firebaseio.com'
	
	for dir_path, dirs, file_names in os.walk(rootDir + apkFileName + "_" + hashlib.md5().hexdigest()):
		for file_name in file_names:
			fullpath = os.path.join(dir_path, file_name)
			with open(fullpath, 'rb') as f:
				contents = f.read()
				temp = re.findall(regex, str(contents))
				if (len(temp) != 0):
					firebaseProjectList += temp
					print("Firebase Instance(s) Found")
		
	if (len(firebaseProjectList) == 0):
		print("No Firebase Project Found. Taking an exit!\nHave an nice day.")
		exit(0)

def printFirebaseProjectNames():
	print("Found " + str(len(firebaseProjectList)) + " Project References in the application. Printing the list of Firebase Projects found.")
	for projectName in firebaseProjectList:
		print(projectName)
	# extracting firebase project name here
	print(type(firebaseProjectList))

def scanInstances():
	print("Scanning Firebase Instance(s)")
	for str in firebaseProjectList:		
		url = 'https://' + str + '.firebaseio.com/.json'
		try:
			# NOT using python requests bcoz it has certain disadvantages w.r.t certificate management for HTTPS URLs 
			http = urllib3.PoolManager()
			response = http.request('GET', url)
			ic(response.status)
		except urllib3.HTTPError as err:
			if(err.code==401):
				print("Secure Firebase Instance Found: " + str)
				continue
			if(err.code==404):
				print("Project does not exist: " + str)
				continue     
			else:
				print("Unable to identify misconfiguration for: ")
				continue
		except urllib3.URLError as err:
			print("Facing connectivity issues. Please Check the Network Connectivity and Try Again.")
			continue
		print("Misconfigured Firebase Instance Found: " + str)


if (len(sys.argv)<3):
	print("Please provide the required arguments to initiate scanning.")
	print("Usage: python3 FirebaseMisconfig.py [options]")
	print("\t-p/--path <apkPathName>")
	print("\t-f/--firebase <commaSeperatedFirebaseProjectName>")
	print("Please try again!!") 
	exit(1);
if (sys.argv[1]=="-p" or sys.argv[1]=="--path"):
	apkFilePath=sys.argv[2];
	isNewInstallation()
	isValidPath(apkFilePath)
	reverseEngineerApplication(apkFileName)
	findFirebaseProjectNames()
	printFirebaseProjectNames()
	scanInstances()
if (sys.argv[1]=="-f" or sys.argv[1]=="--firebase"):
	firebaseProjectList=sys.argv[2].split(",")
	isNewInstallation()
	scanInstances()

