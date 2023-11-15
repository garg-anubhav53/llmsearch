import requests
import urllib
import openai
import os


def main():
	gkey = os.environ.get('GOOGLE_CX')

	gcxid = os.environ.get('GOOGLE_CX_ID') 

	url = 'https://www.googleapis.com/customsearch/v1?'

	#demonstrate how to use the 'params' parameter:
	user_prompt = input("Enter some search terms and as output you will get a summary of the first link.")
	
	set_params = {
	"key": gkey,
	"cx": gcxid, 
	"q": user_prompt 
	}

	response = requests.get(url, params = set_params)

	#print the response (the content of the requested file):
	print("This should be just the first entry", response.json()['items'][0]['link'])

	link = response.json()['items'][0]['link']
	f = urllib.request.urlopen(link)
	rawHTML = f.read()


	main_html = get_main_HTML(rawHTML)
	print("This is the length of main html " , len(main_html))
	
	run_GPT_request(main_html, user_prompt)

def get_main_HTML(inputHTML): 
	f2 = open("afile.html", "w")
	decoded_html = inputHTML.decode("utf-8")
	f2.write(decoded_html)
	f2.close()

		
	main_index = decoded_html.find("<main")
	endmain_index = decoded_html.find("</main")

	if main_index == -1 or endmain_index == -1: 
		simple_error = "Main index or end of main index was not found, try another search method "
		print ("simple_error")
		return simple_error

	main_html = decoded_html[main_index:endmain_index]
	print("This is in main_html at line 49 in get_main_HTML " + main_html)
	return main_html
	 

def run_GPT_request(html, searchterms):
	client = openai.OpenAI()

	request_instructions = f"""Please take the following HTML output and summarize the webpage text 
	that has to do with the content for the user's search terms: {searchterms}. Here is the HTML to
	summarize for those search terms: {html}
	 """

	request_messages = [
    {"role": "system", "content": "You are a helpful assistant that is an expert at parsing complicated HTML and extracting the essential/meaningful portions for a given topic."},
    {"role": "user", "content": request_instructions}
    ]
	summary_response = client.chat.completions.create(model="gpt-3.5-turbo-1106", messages=request_messages)
	LLMSummary_Result = summary_response.choices[0].message.content
	print("This is the answer back from search result: " + LLMSummary_Result)

if __name__ == "__main__":
    main()	

