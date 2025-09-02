import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import joblib
import os

print("--- Starting Anime Collaborative Filtering Model Training ---")

#Load the Datasets
anime_path = os.path.join('data', 'anime.csv')
ratings_path = os.path.join('data', 'rating.csv')

anime = pd.read_csv(anime_path)
ratings = pd.read_csv(ratings_path)
print("Datasets loaded successfully.")

# Preprocess and Merge Data
# Rename columns
anime.rename(columns={'anime_id': 'anime_id', 'name': 'anime_title'}, inplace=True)
ratings.rename(columns={'anime_id': 'anime_id', 'rating': 'user_rating'}, inplace=True)

# Merge ratings with anime information
df = ratings.merge(anime, on='anime_id')

# Handle missing ratings
df = df[df['user_rating'] != -1]

# For a reliable model, filter out noise.
# Count ratings per user and per anime
user_rating_counts = df['user_id'].value_counts()
anime_rating_counts = df['anime_title'].value_counts()

# Filter to users who have rated at least 200 anime, and anime that have at least 50 ratings.
filtered_df = df[
    (df['user_id'].isin(user_rating_counts[user_rating_counts >= 50].index)) &
    (df['anime_title'].isin(anime_rating_counts[anime_rating_counts >= 10].index))
]
print(f"Data filtered. New shape: {filtered_df.shape}")

# Create the User-Item Matrix
# Rows = anime titles, Columns = user IDs, Values = ratings
anime_pivot = filtered_df.pivot_table(index='anime_title', columns='user_id', values='user_rating').fillna(0)
print("Pivot table created.")

# Create Sparse Matrix and Train k-NN Model
anime_sparse = csr_matrix(anime_pivot.values)

model = NearestNeighbors(metric='cosine', algorithm='brute')
model.fit(anime_sparse)
print("k-NN model trained successfully.")

# 5. Save the Trained Artifacts
# Save the model and the pivot table for our API to use.
joblib.dump(model, 'anime_knn_model.pkl')
joblib.dump(anime_pivot, 'anime_pivot.pkl')
print("--- Model and pivot table have been saved successfully! ---")