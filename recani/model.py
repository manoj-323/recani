import pandas as pd
import numpy as np
import pickle

df = pd.read_csv(r'C:\Users\22213\OneDrive\Desktop\recani\recani\data and model\test_data_pre_processed.csv')

with open(r'C:\Users\22213\OneDrive\Desktop\recani\recani\data and model\similarity_matrix.pkl', 'rb') as f:
    similarity_matrix = pickle.load(f)

round_no = 0
arm1_t = 1
arm2_t = 1
arm3_t = 1

user_history_dict = {
    'already_recommended' : [],
    'arm1' : {'anime':[], 'rating':[], 't': 1},
    'arm2' : {'anime':[], 'rating':[], 't': 1},
    'arm3' : {'anime':[], 'rating':[], 't': 1}
}

def user_history(temp_dict, arm):
    global user_history_dict, round_no
    round_no += 1
    if len(temp_dict) == 2:
        user_history_dict['already_recommended'].extend(temp_dict['anime'])
        user_history_dict[f'arm{arm}']['anime'].extend(temp_dict['anime'])
        user_history_dict[f'arm{arm}']['rating'].extend(temp_dict['rating'])
    else:
        for i in range(3):
            user_history_dict['already_recommended'].extend(temp_dict[f'arm{i+1}']['anime'])
            user_history_dict[f'arm{i+1}']['anime'].extend(temp_dict[f'arm{i+1}']['anime'])
            user_history_dict[f'arm{i+1}']['rating'].extend(temp_dict[f'arm{i+1}']['rating'])
    print('your history: ', user_history_dict)
    print(round_no)


def UCB():
    global user_history_dict, round_no
    ucb_values = {}
    for i in range(3):
        t = user_history_dict[f'arm{i+1}']['t']
        ratings = user_history_dict[f'arm{i+1}']['rating']
        average_rating = sum(ratings) / len(ratings)
        exploration_term = np.sqrt(2*(np.log(round_no))/t)
        ucb_values[i+1] = average_rating + exploration_term
    
    print('ucb_values: ',ucb_values)
    
    return max(ucb_values, key=ucb_values.get)

def recommend(arm):
    global user_history_dict
    similar_anime = []
    anime_list = []

    for shown in user_history_dict[f'arm{arm}']['anime']:
        distances = similarity_matrix[shown]
        anime_list.extend(sorted(list(enumerate(distances)), reverse=True, key = lambda x:x[1])[1:10])

    similar_anime.extend(sorted(anime_list, reverse=True, key = lambda x:x[1]))
    anime_list = []
    anime_list.extend([i[0] for i in similar_anime])
    recommendations = [i for i in similar_anime if i not in user_history_dict['already_recommended']][:3]
    
    return recommendations

while True:
    temp_dict = {
        'anime' : [],
        
        'rating' : []
    }
    user_input = {
    'arm1' : {'anime':[20], 'rating':[2],},
    'arm2' : {'anime':[224], 'rating':[4],},
    'arm3' : {'anime':[1], 'rating':[5],}
    }

    if round_no == 0:
        user_history(user_input, 0)

    else:
        arm = UCB()

        for i in range(1,4):
            if arm == i:
                user_history_dict[f'arm{i}']['t'] += 1

        recommendations = recommend(arm)
        recommendations = [i[0] for i in recommendations]
        print(recommendations)

        for i in range(3):
            print(i, ') ', df.iloc[recommendations[i]].name_english)

        for i in recommendations:
            print(i)
            temp_dict['anime'].append(i)
            temp_dict['rating'].append(int(input(f'Rate anime: ')))

        user_history(temp_dict, arm)


    i = input('Want to continue(y/n):')
    if i == 'n':
        break

