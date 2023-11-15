import openai
import search_service
import os
# Initialize OpenAI API
openai.api_key = os.environ['OPENAI_API_KEY']

def main():

    client = openai.OpenAI()

    # Get user input
    user_prompt = input("Enter your query about a topic or website: ")

    # Use OpenAI GPT to generate a query for llmsearch
    extraction_prompt = f"""I have a plugin that can extract information from the web. 
    Based on the user's query '{user_prompt}', what should I search for on the web? 
    Respond with just a single option for search terms and nothing else, 
    since I will directly use your response for searching the web with no other edits."""

    extraction_messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": extraction_prompt}
    ]

    searchterms_response = client.chat.completions.create(model="gpt-3.5-turbo", messages=extraction_messages, max_tokens=100)
    extraction_query = searchterms_response.choices[0].message.content
    # Search the web using llmsearch's from_gpt function

    print("This is what is in extraction_query: " + extraction_query)

    search_results = search_service.run_chat(extraction_query, search_level="full")  # You can choose between "quick" and "full" for search_level
    print("This is what is in search results: " + search_results)


    # Extract the most relevant result (for simplicity, we're taking the first result)
    relevant_content = search_results[0]['response']

    # Use GPT to generate an answer based on the extracted content and user's initial prompt
    answer_prompt = f"The user asked: '{user_prompt}'. The extracted content from the web is: '{relevant_content}'. How should I respond?"
    answer_response = client.chat.completions.create(model="gpt-3.5-turbo", messages=extraction_messages, max_tokens=100)
    answer = answer_response.choices[0].message.content

    # Print the answer
    print(f"Answer: {answer}")

if __name__ == "__main__":
    main()