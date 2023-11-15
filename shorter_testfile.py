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

    number_of_results = 3
    response = requests.get(url, params = set_params)

    print("This should be just the first entry", response.json()['items'][0]['link'])

    for i in range(0, number_of_results): 
        print ("We will check the ", i, "th result from the for loop now")
        link = response.json()['items'][i]['link']
        print("This is the link found at the ", i, "th index of the json: ", link, "/n We will now try to open it.")
        try:
            print ("We have entered the try block for iteration ", i)
            f = urllib.request.urlopen(link)
            print ("Made it past url open for iteration ", i)
            rawHTML = f.read() 
            print ("Made it past url reading for iteration ", i)
        except urllib.error.HTTPError as e:
            print("Error accessing the URL: ", link, "\nError code: ", e.code)
        print ("For iteration ", i, " we have made it to line 32, end of for loop, and should go to next iteration")
if __name__ == "__main__":
    main()


