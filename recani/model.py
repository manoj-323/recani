import pandas as pd
import numpy as np
import pickle

# Load dataset and similarity matrix
df = pd.read_csv(r'C:\Users\22213\OneDrive\Desktop\recani\recani\word2vec_prac_dataset.csv')
with open(r'C:\Users\22213\OneDrive\Desktop\recani\recani\similarity_matrix.pkl', 'rb') as f:
    similarity_matrix = pickle.load(f)

# Initialize variables for three arms
num_rounds = 0
arm_rewards = np.zeros((3, len(df)))
arm_pulls = np.ones((3, len(df)))
already_recommended = [set() for _ in range(3)]  # Three sets to track recommended anime for each arm

# Exploration function for each arm
def explore(arm):
    anime_index = np.random.choice(range(len(df)))
    return anime_index

# Exploitation function using UCB1 algorithm for each arm
def exploit(arm):
    epsilon = 0.1  # Epsilon-greedy parameter
    ucb_values = np.zeros(len(df))
    for anime_index in range(len(df)):
        if arm_pulls[arm][anime_index] == 0:
            ucb_values[anime_index] = np.inf  # Set UCB1 value to infinity for unexplored arms
        else:
            exploration_term = np.sqrt(2 * np.log(num_rounds + 1) / arm_pulls[arm][anime_index])  # Add 1 to avoid log(0)
            ucb_values[anime_index] = arm_rewards[arm][anime_index] / arm_pulls[arm][anime_index] + exploration_term

    if np.random.random() < epsilon:
        return np.random.choice(range(len(df)))  # Explore randomly
    else:
        return np.argmax(ucb_values)  # Exploit based on UCB1 values

# Update statistics after each iteration for each arm
def update_statistics(arm, anime_index, reward):
    global num_rounds, arm_rewards, arm_pulls
    num_rounds += 1
    arm_rewards[arm][anime_index] += reward
    arm_pulls[arm][anime_index] += 1

# Main loop for parallel arms
while True:
    recommendations = []
    for arm in range(3):
        anime_index = explore(arm) if np.random.random() < 0.1 else exploit(arm)  # Exploration with 10% probability
        while anime_index in already_recommended[(arm + num_rounds) % 3]:  # Ensure diversity in recommendations
            anime_index = explore(arm)
        recommendations.append(anime_index)
        already_recommended[(arm + num_rounds) % 3].add(anime_index)
    
    anime_names = [df.iloc[index].name_english for index in recommendations]
    print(f'Recommended anime for each arm: {anime_names}')

    # Simulate user feedback (assuming user provides ratings)
    ratings = []
    for _ in range(3):
        rating = input('Rate anime (0-5) for this arm: ')
        while not rating.isdigit() or int(rating) < 0 or int(rating) > 5:
            print('Invalid rating! Please enter a number between 0 and 5.')
            rating = input('Rate anime (0-5) for this arm: ')
        ratings.append(int(rating))

    for arm, anime_index in enumerate(recommendations):
        update_statistics(arm, anime_index, ratings[arm])

    # Optionally, you can check if the user wants to continue
    continue_response = input('Want to continue? (y/n): ')
    if continue_response.lower() != 'y':
        break
