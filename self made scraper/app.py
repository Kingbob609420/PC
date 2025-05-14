from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/scrape-deals', methods=['POST'])
def scrape_deals():
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({"message": "Query is required"}), 400

    try:
        # Example: Scraping a hypothetical deals site
        response = requests.get(f'https://www.example.com/search?q={query}')
        response.raise_for_status()
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')

        deals = []
        for item in soup.select('.deal-item'):
            title = item.select_one('.deal-title').get_text(strip=True)
            description = item.select_one('.deal-description').get_text(strip=True)
            link = item.select_one('a')['href']
            if title and link:
                deals.append({"title": title, "description": description, "link": link})

        return jsonify({"deals": deals})
    except Exception as e:
        print(f"Error scraping deals: {e}")
        return jsonify({"message": "Error fetching deals"}), 500

if __name__ == '__main__':
    app.run(port=5000)
