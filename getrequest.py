import requests
import urllib
import openai
import os


def main():
	gkey = os.environ.get('GOOGLE_CX')

	gcxid = os.environ.get('GOOGLE_CX_ID') 

	url = 'https://www.googleapis.com/customsearch/v1?'

	#demonstrate how to use the 'params' parameter:
	user_inputs = input(
		"Enter some search terms and as output you will get a summary of the first link. \n" +
		"Provide your response in this format: [search terms],[number_of_results_to_try] \n' ").split(',')
	
	search_terms = user_inputs[0]
	number_of_results = int(user_inputs[1])

	set_params = {
	"key": gkey,
	"cx": gcxid, 
	"q": search_terms 
	}

	LLM_responses = []
	search_response = requests.get(url, params = set_params)

	links = []
	
	for i in range(0, number_of_results): 
		link = search_response.json()['items'][i]['link']
		try:
			f = urllib.request.urlopen(link)
		except urllib.error.HTTPError as e:
			print("Error accessing the URL: ", link, "\nError code: ", e.code)
			continue
		links.append(link)
	print ("Now having tried to find ", number_of_results, 
	" we have actually found ", len(links), ". These links are ", links)

	for link in links: 
		f = urllib.request.urlopen(link)
		rawHTML = f.read()
		main_html = get_main_HTML(rawHTML)
		
		if main_html == "Main index or end of main index was not found, try another search method " : 
			print (main_html)
			print ("Please make changes to the code to find other html formats that may be in search results for your keyterm")
		
		else: 
			print ("main_html for the link ", link, " was found, we will now summarize some results for you.")
			LLM_responses = run_GPT_request(main_html, search_terms, LLM_responses)
		i = 0
		for response in LLM_responses: 
			print("At the end of LLM calls, sitting in the ", i, "th index for LLM_responses is ", response)
			i += 1

def get_main_HTML(inputHTML): 
	f2 = open("afile.html", "w")
	decoded_html = inputHTML.decode("utf-8")
	f2.write(decoded_html)
	f2.close()

		
	main_index = decoded_html.find("<main")
	endmain_index = decoded_html.find("</main")

	if main_index == -1 or endmain_index == -1: 
		simple_error = "Main index or end of main index was not found, try another search method "
		print (simple_error)
		return simple_error

	main_html = decoded_html[main_index:endmain_index]
	return main_html
	 

def run_GPT_request(html, searchterms, LLM_responses):
	client = openai.OpenAI()

	# temporary fix: Check to see if the html is too long, if it is, save only the first 10000 characters.

	if len(html) > 10000: 
		html = html[0:10000]

	request_instructions = f"""Please take the following HTML output and summarize the webpage text 
	that has to do with the content for the user's search terms. Do not give an overview of what the page provides, instead 
	interpret the webpage text directly and provide a summary about it's details: {searchterms}. Here is the HTML to
	summarize for those search terms: {html}. 
	If you can not provide a summary of the actual webpage, respond only with a single world - 'unable'.
	 """

	request_messages = [
    {"role": "system", "content": "You are a helpful assistant that is an expert at parsing complicated HTML and extracting the essential/meaningful portions for a given topic."},
    {"role": "user", "content": request_instructions}
    ]
	summary_response = client.chat.completions.create(model="gpt-3.5-turbo-1106", messages=request_messages)
	LLMSummary_Result = summary_response.choices[0].message.content
	if LLMSummary_Result != 'Unable':
		LLM_responses.append(LLMSummary_Result)
	return LLM_responses

if __name__ == "__main__":
    main()	

