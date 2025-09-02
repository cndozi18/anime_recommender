import joblib
import numpy as np

print("--- Loading Anime Model and Data ---")
model = joblib.load('anime_knn_model.pkl')
anime_pivot = joblib.load('anime_pivot.pkl')
print("--- Load Complete ---")


def get_recommendations(anime_title, num_recommendations=5):
    """
    Finds anime similar to a given anime title using the k-NN model.
    """
    try:
        # Find the numerical index of the anime in our pivot table
        anime_index = np.where(anime_pivot.index == anime_title)[0][0]
        
        # Get the distances and indices of the nearest neighbors
        distances, indices = model.kneighbors(anime_pivot.iloc[anime_index, :].values.reshape(1, -1), n_neighbors=num_recommendations + 1)
        
        print(f"\nRecommendations for '{anime_title}':")
        
        # Loop through the indices, skipping the first one (which is the anime itself)
        for i in range(1, len(distances.flatten())):
            recommended_anime = anime_pivot.index[indices.flatten()[i]]
            print(f"{i}. {recommended_anime}")

    except IndexError:
        print(f"\nError: Anime '{anime_title}' not found. It might be too niche or spelled incorrectly.")
    except Exception as e:
        print(f"An error occurred: {e}")


# --- Test the function with some famous anime ---
get_recommendations("Death Note", 6)
get_recommendations("Cowboy Bebop", 6)
get_recommendations("Fullmetal Alchemist: Brotherhood", 6)
get_recommendations("Naruto", 6)
get_recommendations("One Piece", 6)