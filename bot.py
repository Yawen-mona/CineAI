from openai import AzureOpenAI
import os
import json
import requests

client = AzureOpenAI(
	api_key = os.getenv("AZURE_KEY"),
	api_version = "2024-10-01-preview",
	azure_endpoint = os.getenv("AZURE_ENDPOINT")
)

# Read TMDB API key
try:
    with open("tmdb_key.txt", "r") as key_file:
        tmdb_key = key_file.read().strip()
    if not tmdb_key:
        raise ValueError("TMDB API key is empty. Please check 'tmdb_key.txt'.")
except FileNotFoundError:
    raise FileNotFoundError("TMDB API key file 'tmdb_key.txt' not found.")

# TMDB genre mapping
genre_map = {
    "action": 28,
    "comedy": 35,
    "drama": 18,
    "horror": 27,
    "romance": 10749,
    "science-fiction": 878,
}

# Define function to fetch movies by genre
def films(genre_name):
    genre_id = genre_map.get(genre_name.lower())
    if not genre_id:
        return [{"title": "Invalid genre selected"}]

    url = f"https://api.themoviedb.org/3/discover/movie?api_key={tmdb_key}&with_genres={genre_id}&sort_by=popularity.desc"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract movie titles and poster URLs
        movies = [
            {
                "title": movie["title"],
                "poster_url": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None,
            }
            for movie in data.get("results", [])
        ]

        # Return the top 5 movies or an error message
        return movies[:5] if movies else [{"title": "No movies found for this genre."}]
    except requests.RequestException as e:
        print(f"Error fetching movies: {e}")
        return [{"title": f"Error fetching movies: {str(e)}"}]

# Define OpenAI functions for movie recommendations
functions = [
    {
        "type": "function",
        "function": {
            "name": "Recommend_film",
            "description": "Find a recommended film for tonight",
            "parameters": {
                "type": "object",
                "properties": {
                    "genre": {
                        "type": "string",
                        "description": "The genre of movies to recommend",
                    },
                },
                "required": ["genre"],
            },
        },
    },
]

# Example conversation messages
messages = [
    {"role": "system", "content": "You are an enthusiastic movie critic who provides detailed movie recommendations."},
    {"role": "user", "content": "Recommend a film for tonight."},
]

# Generate Azure OpenAI completion
response = client.chat.completions.create(
    model="GPT-4",
    messages=messages,
    tools=functions,
    tool_choice="auto",
)

response_message = response.choices[0].message
gpt_tools = response_message.tool_calls if "tool_calls" in response_message else None

# Handle tool calls if provided
if gpt_tools:
    available_functions = {
        "Recommend_film": films,
    }

    # Process tool calls
    messages.append(response_message)
    for gpt_tool in gpt_tools:
        function_name = gpt_tool["function"]["name"]
        function_to_call = available_functions.get(function_name)

        if not function_to_call:
            print(f"Unknown function: {function_name}")
            continue

        # Extract function arguments and execute the function
        function_arguments = json.loads(gpt_tool["function"]["arguments"])
        genre_name = function_arguments.get("genre", "")
        function_response = function_to_call(genre_name)

        # Append function response back to messages
        messages.append(
            {
                "tool_call_id": gpt_tool["id"],
                "role": "tool",
                "name": function_name,
                "content": function_response,
            }
        )

    # Send final message with function results
    second_response = client.chat.completions.create(
        model="GPT-4",
        messages=messages,
    )
    print(second_response.choices[0].message.content)
else:
    print(response.choices[0].message.content)