#packages
import os
import openai
import time
import json
import timeit
live = False

#clear funct -- clears terminal
def clear():
	try:
		os.system('clear')
	except:
		os.system('cls')

#requester funct -- sends request to OpenAI with prompt
# --prompt = prompt arg

def openBackupDataset():
	toReturn = []
	for n in range(1,8):
		with open(f'backupDataset/d{n}.json') as file:
			 toReturn.append(json.load(file))

	return toReturn

def closeBackupDataset():
	for n in range(1,8):
		with open(f'backupDataset/d{n}.json') as file:
			file.close()
		
def sendRequest(prompt):

	try:
		# V magic code written by OpenAI V -- (code found @ https://platform.openai.com/playground)
		return openai.Completion.create(
		  model="text-davinci-003",
		  prompt=prompt,
		  temperature=0.7,
		  max_tokens=256,
		  top_p=1,
		  frequency_penalty=0,
		  presence_penalty=0
		)
	except openai.error.ServiceUnavailableError:
		quit("Server is currently unavailible. Code 0.")
	except openai.error.RateLimitError:
		quit("Rate limited. Code 1.")
	except openai.error.Timeout:
		quit("Server timed out. Code 2.")
	except openai.error.AuthenticationError:
		quit("API key could not be verified. Code 3.")
	except:
		quit("Server raised unknown error. Code 4.")

def getDataset():

	prompts = [
		['retail store name, cannot be an existing company:',0],
		["product sold in a retail store and it's price:",1],
		["product sold in a retail store and it's price:",1],
		["product sold in a retail store and it's price:",1],
		["product sold in a retail store and it's price:",1],
		["product sold in a retail store and it's price:",1],
		["list of operating hours for a retail store for monday to friday:",2]
	]

	dataset = []
	
	c = 0
	for i in prompts:
		c += 1
		timeit.Timer
		print("\nSending request to server...")
		dataset.append(sendRequest(i[0]))
		print(f"Response recieved! ({c}/7)\n")
	
	return dataset
		
#optable -- holds possible operations
optable = [
	['Display products','return("opt1")'],
	['Display store hours','return("opt2")'],
	['Display request metadata','return("opt3")'],
	['Quit','return("opt4")']
]

#input funct -- menu selection
def getInput(opTable):

	#begin input loop
	while True:
		
		c = 0 #print menu
		for i in opTable:
			c += 1
			print(f"{c}. {i[0]}")
		print("----------------------")
		
		try:
			uInput = int(input("Enter an option's number to select it\n")) #if input can't be int'd
		except:
			clear()
			for i in [5,4,3,2,1]: #display error & countdown to menu return
				print("TypeError -- Use numbers only.")
				print(f"Returning to menu in {i}...")
				time.sleep(1)
				clear()
			continue #restart input loop

		if uInput > c or uInput < 1: #if input out of range
			clear()
			for i in [5,4,3,2,1]: #display error & countdown to menu return
				print("Out of range -- Option selected is not an option.")
				print(f"Returning to menu in {i}...")
				time.sleep(1)
				clear()
			continue #restart input loop
		break

	return uInput

def awaitReturnKey():
	print("Enter any key to return...")
	input("")

def menu(opType,inputData):

	clear()
	if opType == 0:
		for i in inputData['products']:
			print(i)
		print("")
		awaitReturnKey()

	elif opType == 1:
		print(inputData['hours'])
		print("")
		awaitReturnKey()

	elif opType == 2:

		if live == False:
			print("V THIS DATASET IS PRE-GENERATED (IT DID NOT COST ANYTHING) V")
			print("------------------------------------------------------------")
		print(f'Total tokens used for this dataset: {inputData["tokensUsed"]}')
		print(f"Total cost of the dataset (USD): ${inputData['tokensUsed'] * 0.00002}")
		print("Request tracking IDs:")
		for i in inputData['trackingIDs']:
			print(i)
		print("")
		awaitReturnKey()

	elif live == True:
		print(f'Total tokens used for this dataset: {inputData["tokensUsed"]}')
		print(f"Total cost of the dataset (USD): ${inputData['tokensUsed'] * 0.00002}")
		print("Request tracking IDs:")
		for i in inputData['trackingIDs']:
			print(i)
		print("")
		awaitReturnKey()

	elif opType == 3:
		print("About this app-\nThis app uses OpenAI's language-generation model, Davinci, to write random store names, products, and hours.\n")
		awaitReturnKey()

	elif opType == 4:
		quit("Exitted")
		
#dataset creator funct -- assigns variables to outside sources
def local():
	dataset = openBackupDataset() #sets dataset to files all files from .\backupDataset

	#holds variables for later use
	processedData = {
		"name":"",
		"products":[],
		"hours":"",
		"tokensUsed":0,
		"trackingIDs":[]
	}

	
	c = 0 #used to track which response we are processing
				#this assigns it in the proper spot in processedData
	
	for i in dataset: #loop through .\backupDataset

		#count up tokens for each response
		processedData['tokensUsed'] += int(i['usage']['total_tokens'])
		processedData['trackingIDs'].append(i['id']) #store tracking IDs
		
		c +=1 #tally up the response position tracker
		if c == 1: #if we're on the first response,
			processedData['name'] = i['choices'][0]['text'] #it's a name, put it in the name section
		elif c > 1 and c < 7: #if it's between 2 and 6,
			processedData['products'].append(i['choices'][0]['text']) #it's a product-price pair, put it in the products section
		elif c > 6: #if it's after 6,
			processedData['hours'] = i['choices'][0]['text'] #it's store hours, put it in the hours section

	closeBackupDataset() #removes all the files from memory
	
	#V Menu V

	menuOptable = [ #sets up an optable
		['Display product list','menu(0,processedData,False)'],
		['Display store hours','menu(1,processedData,False)'],
		['Display request metadata','menu(2,processedData,True),'],
		['Display info','menu(3,None,False)'],
		['Quit','menu(4,None,False)']
	]

	while True:
		clear()
		print(str.upper(processedData['name']))
		print("----------------------")
		print("Options:")
		print('-----------------------')
		exec(menuOptable[getInput(menuOptable)-1][1])
		

def live():
	clear()
	openai.api_key = input("ENTER API KEY: ")

	dataset = getDataset() #sets dataset to files all files from .\backupDataset

	#holds variables for later use
	processedData = {
		"name":"",
		"products":[],
		"hours":"",
		"tokensUsed":0,
		"trackingIDs":[]
	}

	
	c = 0 #used to track which response we are processing
				#this assigns it in the proper spot in processedData
	
	for i in dataset: #loop through .\backupDataset

		#count up tokens for each response
		processedData['tokensUsed'] += int(i['usage']['total_tokens'])
		processedData['trackingIDs'].append(i['id']) #store tracking IDs
		
		c +=1 #tally up the response position tracker
		if c == 1: #if we're on the first response,
			processedData['name'] = i['choices'][0]['text'] #it's a name, put it in the name section
		elif c > 1 and c < 7: #if it's between 2 and 6,
			processedData['products'].append(i['choices'][0]['text']) #it's a product-price pair, put it in the products section
		elif c > 6: #if it's after 6,
			processedData['hours'] = i['choices'][0]['text'] #it's store hours, put it in the hours section

	closeBackupDataset() #removes all the files from memory
	
	#V Menu V

	menuOptable = [ #sets up an optable
		['Display product list','menu(0,processedData)'],
		['Display store hours','menu(1,processedData)'],
		['Display request metadata','menu(2,processedData)'],
		['Display info','menu(3,None)'],
		['Quit','menu(4,None)']
	]

	while True:
		clear()
		print(str.upper(processedData['name']))
		print("----------------------")
		print("Options:")
		print('-----------------------')
		exec(menuOptable[getInput(menuOptable)-1][1])

initOptable = [
	['Use local dataset','local()'],
	['Use live dataset','live()']
]

def starter():
		exec(initOptable[getInput(initOptable)-1][1])

if __name__ == "__main__":
	starter()

