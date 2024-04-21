import pandas as pd 
import numpy as np
import pickle

df = pd.read_csv(r'C:\Users\22213\OneDrive\Desktop\recani\recani\word2vec_prac_dataset.csv')

with open(r'C:\Users\22213\OneDrive\Desktop\recani\recani\similarity_matrix.pkl', 'rb') as f:
    similarity_matrix = pickle.load(f)

i = 'y'
arm_1 = 1
arm_2 = 1
arm_3 = 1
epsilon = 10
num_rounds = 0
user_history_dict = {}
already_recommended = []


def explore(anime):
    anime_index = df[df['name_english'] == anime].index[0]
    distances = similarity_matrix[anime_index]
    anime_list = sorted(list(enumerate(distances)), reverse=True, key = lambda x:x[1])[1:4]
    return anime_list


def exploit(user_watched):
    # Find similar shows for each watched show
    similar_shows = []
    for show_index in user_watched:
        similar_shows.extend([(similarity_matrix[show_index, other_show_index], other_show_index) for other_show_index in range(similarity_matrix.shape[0]) if other_show_index != show_index])
    
    # Filter out watched shows
    similar_shows = [(similarity, show_index) for similarity, show_index in similar_shows if show_index not in user_watched]
    
    # Rank similar shows based on similarity scores
    similar_shows.sort(reverse=True)
    
    # Recommend top shows
    recommendations = [show_index for similarity, show_index in similar_shows[:1]]
    
    return recommendations


def UCB(user_feedback):
    global num_rounds, epsilon, arm_1, arm_2, arm_3
    ucb_values = {}
    exploration_constant = 2.0
    
    if len(user_feedback) == 0:
        num_rounds += 1
        return np.random.choice([1,2,3])

    else:

        first_rating = [sub['rating'][0] for sub in user_feedback.values()]
        average_feedback_1 = sum(first_rating) / len(first_rating)
        exploration_term_1 = np.sqrt((2 * np.log(num_rounds)) / arm_1)

        second_rating = [sub['rating'][1] for sub in user_feedback.values()]
        average_feedback_2 = sum(second_rating) / len(second_rating)
        exploration_term_2 = np.sqrt((2 * np.log(num_rounds)) / arm_2)
        
        third_rating = [sub['rating'][2] for sub in user_feedback.values()]
        average_feedback_3 = sum(third_rating) / len(third_rating)
        exploration_term_3 = np.sqrt((2 * np.log(num_rounds)) / arm_3)


        ucb_values[1] = average_feedback_1 + exploration_constant*exploration_term_1
        ucb_values[2] = average_feedback_2 + exploration_constant*exploration_term_2
        ucb_values[3] = average_feedback_3 + exploration_constant*exploration_term_3

        print()
        print(ucb_values[1], ucb_values[2], ucb_values[3], num_rounds)
        print()
        print(arm_1, arm_2, arm_3)
    
    if abs(ucb_values[1]-ucb_values[2] < epsilon/1.5):
        recommended_arm = np.random.choice([1, 2, 3])
    else:
        recommended_arm = max(ucb_values, key=ucb_values.get)

    num_rounds += 1
    epsilon /= 1.5

    if recommended_arm == 1:
        arm_1 += 1
    elif recommended_arm == 2:
        arm_2 += 1
    else:
        arm_3 += 1

    return recommended_arm


def user_history(x):
    global user_history_dict
    user_history_dict[len(user_history_dict) + 1] = x
    print(user_history_dict)


while i == 'y':
    arm = UCB(user_feedback=user_history_dict)
    temp_dict = {'anime':[], 'rating':[]}

    if len(user_history_dict) == 0:
        recommendations = recommend('One Piece')

        already_recommended.append(recommendations[0][0])
        already_recommended.append(recommendations[1][0])
        already_recommended.append(recommendations[2][0])

        for n, i in enumerate(recommendations):
            print(f'{n+1}) ',df.iloc[i[0]].name_english)

        temp_dict['anime'].append(recommendations[0][0])
        temp_dict['anime'].append(recommendations[1][0])
        temp_dict['anime'].append(recommendations[2][0])
        temp_dict['rating'].append(0)
        temp_dict['rating'].append(0)
        temp_dict['rating'].append(0)

        user_history(temp_dict)

        print()
        i = input('Want to continue y/n: ')

    else:

        anime_liked_so_far = [sub['rating'][arm-1] for sub in user_history_dict.values()]

        recommendation = recommend_similar_anime(anime_liked_so_far)

        already_recommended.append(recommendation)

        print(df.iloc[recommendation].name_english)

        if arm == 1:
            temp_dict['anime'].append(recommendation[0])
            temp_dict['anime'].append(None)
            temp_dict['anime'].append(None)
            temp_dict['rating'].append(int(input('Rate anime: ')))
            temp_dict['rating'].append(0)
            temp_dict['rating'].append(0)
        elif arm == 2:
            temp_dict['anime'].append(None)
            temp_dict['anime'].append(recommendation[0])
            temp_dict['anime'].append(None)
            temp_dict['rating'].append(0)
            temp_dict['rating'].append(int(input('Rate anime: ')))
            temp_dict['rating'].append(0)
        else:
            temp_dict['anime'].append(None)
            temp_dict['anime'].append(None)
            temp_dict['anime'].append(recommendation[0])
            temp_dict['rating'].append(0)
            temp_dict['rating'].append(0)
            temp_dict['rating'].append(int(input('Rate anime: ')))

        user_history(temp_dict)

        print()
        i = input('Want to continue y/n: ')
