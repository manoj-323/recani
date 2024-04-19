import pandas as pd 
import numpy as np
import pickle

df = pd.read_csv(r'C:\Users\22213\OneDrive\Desktop\recani\recani\word2vec_prac_dataset.csv')

with open(r'C:\Users\22213\OneDrive\Desktop\recani\recani\similarity_matrix.pkl', 'rb') as f:
    similarity_matrix = pickle.load(f)

def recommend(anime):
    anime_index = df[df['name_english'] == anime].index[0]
    distances = similarity_matrix[anime_index]
    anime_list = sorted(list(enumerate(distances)), reverse=True, key = lambda x:x[1])[1:4]
    return anime_list



def update(self, anime, feedback):
    # Update user feedback for the recommended anime
    if anime in self.user_feedback:
        self.user_feedback[anime]['sum_feedback'] += feedback
        self.user_feedback[anime]['num_feedback'] += 1
    else:
        self.user_feedback[anime] = {'sum_feedback': feedback, 'num_feedback': 1}



def recommend_anime(self):
    # UCB1 exploration-exploitation strategy
    exploration_constant = 2.0  # You can adjust this exploration constant
    ucb_values = {}
    for anime, feedback_info in self.user_feedback.items():
        if feedback_info['num_feedback'] == 0:
            # If no feedback received, explore by default
            ucb_values[anime] = float('inf')
        else:
            average_feedback = feedback_info['sum_feedback'] / feedback_info['num_feedback']
            exploration_term = np.sqrt((2 * np.log(self.num_rounds)) / feedback_info['num_feedback'])
            ucb_values[anime] = average_feedback + exploration_constant * exploration_term
    
    # Select the anime with the highest UCB value
    recommended_anime = max(ucb_values, key=ucb_values.get)
    self.num_rounds += 1
    return recommended_anime


user_history_dict = {}
def user_history(x):
    global user_history_dict
    user_history_dict[len(user_history_dict) + 1] = x
    print(user_history_dict)

num_rounds = 0
i = 'y'

while i == 'y':
    recommendations = recommend('One Piece')
    temp_dict = {'anime':[], 'rating':[]}

    temp_dict['anime'].append(recommendations[0][0])
    temp_dict['anime'].append(recommendations[1][0])
    temp_dict['anime'].append(recommendations[2][0])

    for i in recommendations:
        print(df.iloc[i[0]].name_english)

    temp_dict['rating'].append(int(input('Rate anime 1: ')))
    temp_dict['rating'].append(int(input('Rate anime 2: ')))
    temp_dict['rating'].append(int(input('Rate anime 3: ')))

    user_history(temp_dict)

    print()
    i = input('Want to continue y/n: ')