# Twitch/IGDB Game Genre Finder

A command-line Python app that searches for any video game and returns
its genres using the IGDB API, authenticated through Twitch's 
OAuth2 system.

## Features
- Authenticates with Twitch using OAuth2 client credentials flow
- Searches the IGDB database for any game by name
- Returns the game's genres
- Handles API errors and timeouts with automatic retry 
  (exponential backoff)

## Example Output
Enter game name: Halo
Shooter, Adventure

## Technologies Used
- Python
- [requests](https://pypi.org/project/requests/) library
- [Twitch OAuth2 API](https://dev.twitch.tv/docs/authentication/)
- [IGDB API](https://api-docs.igdb.com/)

## How to Run
1. Register your app at [dev.twitch.tv](https://dev.twitch.tv) to 
   get your `client_id` and `client_secret`
2. Add your credentials to a `.env` file:
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
3. Install dependencies:
pip install requests
4. Run the app:
python tokens.py

## What I Learned
- Implementing OAuth2 client credentials flow
- Working with two APIs that share the same authentication system
- Parsing nested JSON responses
- Handling API errors and timeouts with exponential backoff
