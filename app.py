from flask import Flask, render_template, request
from bot import ask_question
import markdown

app = Flask(__name__, static_folder='static')

# set up our landing page
@app.route('/')
def index():
    return render_template('index.html', question="", chatbot_response="", poster_url="")

# only use this when posting data!
@app.route('/', methods=['GET', 'POST'])
def index_post():
    user_question = request.form['req_question']
    chatbot_response = ask_question(user_question)

    if isinstance(chatbot_response, str):
        chatbot_response = markdown.markdown(chatbot_response) # Convert to HTML first!
        movies = [] # No need for movies here, the HTML is in chatbot_response

    elif isinstance(chatbot_response, list): # Handle the case where the tool *is* called
        movies = chatbot_response
        chatbot_response = "" # Clear the text response since we have movie data

    return render_template('index.html', question=user_question, chatbot_response=chatbot_response, movies=movies)

    if __name__ == '__main__':
        app.run(debug=True)