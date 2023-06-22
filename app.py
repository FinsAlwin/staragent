from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/followers', methods=['POST'])
def get_followers_count():
    data = request.json
    url = data.get('url')

    if url:
        followers_count = extract_followers_count(url)
        return jsonify({'followers_count': followers_count})
    else:
        return jsonify({'error': 'URL parameter is missing.'}), 400

def extract_followers_count(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        meta_tags = soup.find_all('meta', content=lambda c: c and 'Followers' in c)

        for meta_tag in meta_tags:
            content = meta_tag.get('content')
            followers_count = re.search(r'(\d+(?:,\d+)?(?:\.\d+)?(?:[KMBT]| billion| trillion)?)(?= Followers)', content)
            if followers_count:
                return followers_count.group(1)

        return "No followers count found."

    else:
        return f"Failed to retrieve HTML: {response.status_code}"


if __name__ == '__main__':
    app.run()

# if __name__ == '__main__':
#     app.run(host="0.0.0.0")
