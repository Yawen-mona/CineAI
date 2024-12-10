from flask import Flask, render_template, request
from bot import films

app = Flask(__name__, static_folder='static')


@app.route('/')
def index():
    return render_template('index.html', question='', chatbot_response='', poster_url='')

@app.route('/recommend', methods=['POST'])
def recommend_movie():
    genre = request.form['genre'].strip()  # Get genre from the form
    if not genre:
        return render_template(
            'index.html',
            genre=genre,
            chatbot_response="Error: Please select a valid genre.",
            poster_url=''
        )

    # Get movie recommendations based on the selected genre
    chatbot_response = films(genre)
    return render_template('index.html', question=genre, chatbot_response=chatbot_response, poster_url='')



# Error handling
@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', message="Page not found"), 404

if __name__ == '__main__':
    app.run(debug=True)
