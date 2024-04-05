from flask import Flask, render_template, redirect, url_for
import requests

app = Flask(__name__)

# Yelp API credentials
API_KEY = 'FzrkBw0LEKgiFfeRhyuj6YOGYgktay3JzRYyRz1nPw5FHNaHRhkIT3FzArQJiA09HrNfAJgR1kjiPQvC8DmQMcCaoPDbn1boeAakGb4HVqAt0a0ka-v3niIa00cQZnYx'

# Function to fetch black-owned businesses from Yelp API
def get_black_owned_businesses(location):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
    }
    params = {
        'term': 'black owned',
        'location': location,
        'limit': 10
    }
    response = requests.get('https://api.yelp.com/v3/businesses/search', headers=headers, params=params)
    data = response.json()
    businesses = []
    for business in data.get('businesses', []):
        businesses.append({
            'name': business['name'],
            'image': business['image_url'],
            'location': ', '.join(business['location']['display_address'])
        })
    return businesses

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/state/<state>')
def state(state):
    businesses = get_black_owned_businesses(state)
    return render_template('results.html', state=state, businesses=businesses)

if __name__ == '__main__':
    app.run(debug=True)