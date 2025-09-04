from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)

print("Loading model...")
model = joblib.load('anime_knn_model.pkl')
anime_pivot = joblib.load('anime_pivot.pkl')
print("Model loaded successfully.")

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/recommend')
def recommend():
    anime_title = request.args.get('title')
    try:
        # Get index of anime from pivot table
        # Get the row of data and reshaping it
        anime_index = np.where(anime_pivot.index == anime_title)[0][0]
        row_of_data = anime_pivot.iloc[anime_index, :].values.reshape(1, -1)
        distances, indices = model.kneighbors(row_of_data, n_neighbors=6)

        # Get a list of the titles of the recommended anime
        recommended_anime = []
        for i in range(1, len(indices.flatten())):
            recommended = anime_pivot.index[indices.flatten()[i]]
            recommended_anime.append(recommended)

        return jsonify(recommended_anime)
    except IndexError:
        return jsonify({"error": f"Anime '{anime_title}' not found. It might be too niche or spelled incorrectly."}), 404

if __name__ == '__main__':
    app.run(debug=True)