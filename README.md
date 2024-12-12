# CineAI - Movie Recommendations Web Application

This project is a **movie recommendation web application** built with Python, Flask, and OpenAI's Azure GPT-4 API. The application allows users to ask for movie recommendations based on specific queries (e.g., genres, themes, or keywords) and receive suggestions with rich details, including movie posters, overviews, ratings, and release dates.

------

## Features

- **AI-Driven Recommendations**: Powered by OpenAI's GPT-4 and TMDb API for high-quality movie suggestions.
- **Interactive User Interface**: A user-friendly web interface for entering queries and browsing movie results.
- Detailed Movie Information
  - Title
  - Overview
  - Poster Image
  - User Rating
  - Release Date

------

## Technologies Used

- Overview
  - Python 3.x
  - Flask Framework
  - Azure OpenAI GPT-4 API
  - TMDb API (The Movie Database)
- Libraries
  - `requests` (for TMDb API integration)
  - `openai` (for  AI chatbot response)
  - `flask` (for  flask format)
  - `markdown` (for rendering chatbot responses)
- Other
  - Static files for custom CSS styling

------

## 📋 Prerequisites

1. **API Keys**:

- Azure OpenAI API key and endpoint
- TMDb API key

1. **Python 3.x**
2. **pip** (Python package manager)
3. **Virtual environment** 

------

## 🚀Installation

1. Clone the repository:

   ```
   git clone https://github.com/Yawen-mona/CineAI
   ```

2. Set up a virtual environment :

   ```
   pip install virtualenv venv
   On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Add Keys:

- Create a file named `tmdb_key.txt` in the root folder and paste your TMDb API key.

- Set the following environment variables:

  ```
  set AZURE_KEY=your_azure_api_key
  set AZURE_ENDPOINT=your_azure_api_endpoint
  ```

5. Add TMDb API Key:

```bash
# Create tmdb_key.txt and add your key
"your_tmdb_api_key" > tmdb_key.txt
```

------

## 💻Usage

1. Run the Flask app:

   ```
   flask run
   ```

2. Open your browser and navigate to:

   ```
   http://127.0.0.1:5000/
   ```

3. Enter your query (e.g., "Christmas movies") in the search box and submit.

4. View the recommended movies along with details and posters.

------

## 📁Folder Structure

```
graphqlCopy codemovie-recommendations/
├── app.py                 # Flask application entry point
├── bot.py                 # GPT-4 & TMDb API logic
├── templates/
│   ├── index.html         # Main HTML page
├── static/
│   ├── css/
│   │   ├── style.css      # Styling for the app
├── tmdb_key.txt           # TMDb API Key 
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

------

## API Details

### TMDb API

- **Endpoint**: `https://api.themoviedb.org/3/search/movie`
- Parameters
  - `api_key`: Your TMDb API key
  - `query`: Search term for movies
  - `sort_by`: Sorts results by popularity

### Azure OpenAI API

- Used for processing user queries and identifying when to fetch movie data using the TMDb API.



## 👏Overview

- **OpenAI**: For providing cutting-edge AI models.
- **TMDb**: For the movie database and API.
- **Flask**: For the lightweight and versatile framework.

Enjoy exploring movie recommendations with this app! 🎥✨