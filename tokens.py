import requests
import os
from dotenv import load_dotenv
import json # used for testing json() responses mainly json.dumps()
import time

load_dotenv() # reads file from .env file and loads the key:value pairs into the environment
client_id = os.getenv("TWITCH_CLIENT_ID") #os.getenv gets the value from the "CLIENT_ID" KEY and sets to client_id
client_secret = os.getenv("TWITCH_CLIENT_SECRET")

"""
this api is split into 2 apis running on the same security feature
firstly we register the program with twitch and gain client id and client secret 
we then send the request.post() with only the url and params to get our access token
because this is technically two apis the header and data args are sent to the IGDB api
because that is what IGDB uses to work
"""


def main():
    token = get_access_token()
    while True:
        game_name = input("Enter game name: ")
        game_result = search_game(game_name,token)
        if game_result:
            break
        print("game not found")
    print(return_genre(game_result,token))


def get_access_token():
    response = requests.post("https://id.twitch.tv/oauth2/token", #function that accepts (url)-where to send request,(params), query string parameter added to url after ? char.
    #(headers) are extra information that is sent to the server like authorization details, client_id,(data) what information are you requesting
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials" # grant type is what type of authentication is being performed in this case client credentials
        # which the application/program  ie:this program authenticates itself, no user involved
        #grant type : authorization_code requires login through browsers, user input required and is granted permission - login,password
        }
    )
    return response.json()["access_token"] # access_token is a key from the json() conversion of request.post()



def search_game(game_name, access_token):
    retry = 0
    while retry < 3:
        headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}"
    }
        try:
            response = requests.post(
                "https://api.igdb.com/v4/games",
                headers=headers,
                data=f'search "{game_name}"; fields name,genres;',# syntax is custom query language used by this api
                timeout= 2 # in the api doc this syntax is required to operate the api
                #timeout is an arg of the function request.post() that handles if a request is taking a long time

        )
            if response.status_code in [408, 429, 500, 502, 503, 504]:
                time.sleep(2 ** retry)#function of time that pauses the program for 2^of retry attempts, exponential backoff
                print(f'retry attempt {retry}')
                retry += 1
                continue
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.Timeout:
            print("Program timed out")
            continue
    return None

def search_genre(genres_id,access_token):
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.post(
        "https://api.igdb.com/v4/genres",
    headers=headers,
    data= f"fields name; where id = ({','.join(map(str, genres_id))});" # where in api syntax is a filter key
        #','.join(map(str, genres_id - genres_id(also the arg of this function) is going to be a list of id's taken from the search_game() function
        #(map(str, genres_id - maps the value(genres_id) of each index and converts it into a str
        #','.join - joins them all into one comma separated string
        #example [12,13,14] --> "12,13,14"
    )
    return response.json()

def return_genre(game_result,token): # takes the return value of the search_game() as an arg
    all_genres = [] # empty list to hold genre values
    try:
        genre_id = game_result[0]['genres'] #only one thing in the list so we need to index into the value which is a dictionary then index into the value 'genres'
    except KeyError:
        return "Unknown"
    search_result = search_genre(genre_id,token) # calls the search genre function which also returns a list
    for genre in search_result:
        all_genres.append(genre['name'])
    return ','.join(all_genres)


if __name__ == "__main__":
    main()
