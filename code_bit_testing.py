import requests
import urllib
import openai
import os

search_terms = ''
number_of_results = 0

def main():
	gkey = os.environ.get('GOOGLE_CX')

	gcxid = os.environ.get('GOOGLE_CX_ID') 

	url = 'https://www.googleapis.com/customsearch/v1?'

	#demonstrate how to use the 'params' parameter:
	user_inputs = input(
		"Enter some search terms and as output you will get a summary of the first link. /n" +
		"Provide your response in this format: [search terms],[number_of_results_to_try] /n").split(',')
	
	search_terms = user_inputs[0]
	number_of_results = user_inputs[1]

if __name__ == "__main__":
    print(main())
    


