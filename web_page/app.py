from flask import Flask, render_template, request, redirect, url_for
import numpy as np

app = Flask(__name__)

# Define anime titles and their unknown ratings
anime_titles = ['Attack on Titan', 'Death Note', 'Naruto', 'One Piece', 'Dragon Ball Z']
num_anime = len(anime_titles)
unknown_ratings = np.random.randint(1, 6, size=num_anime)  # Simulated unknown ratings (1-5)

# Initialize variables for recommendations, user ratings, and already recommended anime
recommendations = [None] * 3
user_ratings = [None] * 3
already_recommended = set()

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Recommendation page route
@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
    global recommendations, user_ratings, already_recommended

    # Generate new recommendations if user submits ratings
    if request.method == 'POST':
        for i in range(3):
            user_ratings[i] = int(request.form.get(f'rating_{i}'))
            already_recommended.add(recommendations[i])

        recommendations = [anime_index for anime_index in range(num_anime) if anime_index not in already_recommended]
        np.random.shuffle(recommendations)
        recommendations = recommendations[:3]

    # Render recommendation page with anime titles and ratings
    return render_template('recommendation.html', anime_titles=[anime_titles[i] for i in recommendations])

if __name__ == '__main__':
    app.run(debug=True)
