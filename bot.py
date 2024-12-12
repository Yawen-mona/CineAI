from openai import AzureOpenAI
import os
import json
import requests

client = AzureOpenAI(
    api_key=os.getenv("AZURE_KEY"),
    api_version="2024-10-01-preview",
    azure_endpoint=os.getenv("AZURE_ENDPOINT")
)


with open('tmdb_key.txt', 'r') as key_file:
    tmdb_key = key_file.read()


messages = [
    {"role": "system", "content": "You are an enthusiastic movie lover.  When providing movie recommendations, always use the Recommend_film tool to get movie details, including poster_path and show poster. Provide a maximum of 5 recommendations"},

]

# Function to fetch movies using TMDb API
def films(query):
        url = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_key}&sort_by=popularity.desc&query={query}"
        
        print(url)
        response = requests.get(url)
        data = response.json()

        movie = [
            {
                "title": movie["title"], 
                "overview": movie.get("overview", "No overview available"),
                "poster_url": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None,
                "vote_average": movie.get("vote_average", 0), #Added vote average
                "release_date": movie.get("release_date", "N/A") #Added release date
            }
            for movie in data.get("results", [])
        ]

        
        return movie[:5]

   
# Define tools/functions
functions = [
    {
        "type": "function",
        "function": {
            "name": "Recommend_film",
            "description": "Find a recommend film based on a specific query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query for the movie search (e.g., Christmas)."
                    }
                },
                "required": ["query"]
            }
        }
    }
]

def ask_question(user_question):
    messages.append({"role": "user", "content": user_question})
# Send the initial request to the chat completion endpoint
    response = client.chat.completions.create(
        model="GPT-4",
        messages=messages,
        tools=functions,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    gpt_tools = response.choices[0].message.tool_calls

    # If the assistant suggests using tools
    if gpt_tools:
        # Map function name to actual Python function
        available_functions = {
            "Recommend_film": films
        }

        # Append the tool's response
        messages.append(response_message)

        for gpt_tool in gpt_tools:
            function_name = gpt_tool.function.name
            function_to_call = available_functions[function_name]

            
            function_parameters = json.loads(gpt_tool.function.arguments)
            function_response = function_to_call(function_parameters.get('query'))

                # Add the tool's response to the conversation
            messages.append(
                    {
                            "tool_call_id": gpt_tool.id,
                            "role": "tool",
                            "name": function_name,
                            "content": json.dumps(function_response)
                    }
            )

                # Get the assistant's second response
            second_response = client.chat.completions.create(
            model="GPT-4",
            messages=messages
            )
            return second_response.choices[0].message.content

    else:
        # If no tools are suggested, print the assistant's initial response
        return response.choices[0].message.content