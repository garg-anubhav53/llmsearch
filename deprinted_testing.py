import requests
import urllib
import openai
import os

def main():
    gkey = os.environ.get('GOOGLE_CX')
    gcxid = os.environ.get('GOOGLE_CX_ID') 
    url = 'https://www.googleapis.com/customsearch/v1?'

    user_prompt = input("Enter some search terms and as output you will get a summary of the first link.")
    
    set_params = {
        "key": gkey,
        "cx": gcxid, 
        "q": user_prompt 
    }

    number_of_results = 5
    response = requests.get(url, params = set_params)
    links = []
    for i in range(0, number_of_results): 
        link = response.json()['items'][i]['link']
        try:
            f = urllib.request.urlopen(link)
            rawHTML = f.read() 
        except urllib.error.HTTPError as e:
            print("Error accessing the URL: ", link, "\nError code: ", e.code)
            continue
        links.append(link)

    print ("Now having tried to find ", number_of_results, 
    " we have actually found ", len(links), ". These links are ", links)    
    
if __name__ == "__main__":
    main()
