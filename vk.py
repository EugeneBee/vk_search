#Python 3.7.x
"""
The program requests message parameters from the vk.com community walls through the API.
Loads JSON response data. Saves specific polar messages in a CSV file.
"""
#Import required packages.
import requests
import json
import csv
import io
from datetime import datetime
from time import sleep

#enter your valid vk.com token as per the documentation https://vk.com/dev/api_requests
token = 'afc36XXXXXXXXXXXXXXXXX0bac04d467b92acXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

def write_csv(data):
    """    
    Writes specific fields from the received dictionary to the posts_data.csv file.
    """

    with io.open('posts_data.csv', 'a', encoding="utf-8", errors="ignore") as file:
        write = csv.writer(file)

        #The listed fields of the incoming dictionary are written to the file.
        write.writerow((data['comments'],
                        data['likes'],
                        data['reposts'],
                        data['text']
                        ))

def get_data(post):
    """    
    The function accepts input in the form of a dictionary, on the basis of which it produces a dictionary with the given keys.
    """
    try:
        post_id = post['id']
    except:
        post_id = 'Not_value id'

    try:
        comments = post['comments']['count']
    except:
        likes = 'Not_value comments count'

    try:
        likes = post['likes']['count']
    except:
        likes = 'Not_value likes count'

    try:
        reposts = post['reposts']['count']
    except:
        reposts = 'Not_value reposts count'  

    try:
        text = post['text']
    except:
        text = 'Not_value text'

    data = {
        'id': post_id,
        'comments': comments,
        'likes': likes,
        'reposts': reposts,
        'text': text
    }
    return data

def main():

    #Set the start time of the program.
    start = datetime.now()

    #Enter the values ​​of the variables.
    group_id = '-93172467'
    offset = 0
    date_x = 1539680373
    all_posts = []
    data_posts = []


    while True:
        #The API limit is no more than 3 requests per second, so we set a delay before each iteration of the loop.
        sleep(0.4)
        #The request sent, the form and parameters in accordance with the vk.com API documentation.
        req_ = requests.get('https://api.vk.com/method/wall.get', params = {'owner_id': group_id, 
                                                                        'count': 100, 
                                                                        'offset': offset, 
                                                                        'v': 5.102,
                                                                        'access_token': token})

        #Initial data selection: write the contents of the dictionary with keys into a variable: ['response'] ['items']
        posts = req_.json()['response']['items']
        #Add the received 100 data records to the end of the list of each iteration.
        all_posts.extend(posts)
        #Set the flag according to the time of the last record in the iteration.
        oldes_post_date = posts[-1]['date']
        #Increase the counter and display its value in the console to control the correct execution.
        offset += 100
        print(offset)
        #If the date is less than the set value, we interrupt the cycle.
        if oldes_post_date < date_x: break

    #In the loop, write the data from the list into the file element by element using the function.
    for post in all_posts:
        post_data = get_data(post)
        write_csv(post_data)

    #Set the end time of the program.
    end = datetime.now()

    #To control the correct execution, we deduce the number of entries in the file and the runtime of the program.
    print('Records found: ', len(all_posts))
    print('Program execution time: ', str(end - start))


if __name__ == "__main__":
    main()
