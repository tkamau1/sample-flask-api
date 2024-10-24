from flask import Flask, jsonify, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Define a route to scrape metadata
@app.route('/scrape', methods=['GET'])
def scrape_metadata():
    url = request.args.get('url')
    if url:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Basic metadata
            title = soup.title.string if soup.title else 'No title'
            description = soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else 'No description'
            thumbnail = soup.find('meta', {'property': 'og:image'})['content'] if soup.find('meta', {'property': 'og:image'}) else 'No thumbnail'

            # Open Graph metadata
            og_title = soup.find('meta', {'property': 'og:title'})['content'] if soup.find('meta', {'property': 'og:title'}) else 'No OG title'
            og_description = soup.find('meta', {'property': 'og:description'})['content'] if soup.find('meta', {'property': 'og:description'}) else 'No OG description'
            og_image = soup.find('meta', {'property': 'og:image'})['content'] if soup.find('meta', {'property': 'og:image'}) else 'No OG image'
            og_url = soup.find('meta', {'property': 'og:url'})['content'] if soup.find('meta', {'property': 'og:url'}) else 'No OG URL'
            og_type = soup.find('meta', {'property': 'og:type'})['content'] if soup.find('meta', {'property': 'og:type'}) else 'No OG type'

            # Twitter Card metadata
            twitter_title = soup.find('meta', {'name': 'twitter:title'})['content'] if soup.find('meta', {'name': 'twitter:title'}) else 'No Twitter title'
            twitter_description = soup.find('meta', {'name': 'twitter:description'})['content'] if soup.find('meta', {'name': 'twitter:description'}) else 'No Twitter description'
            twitter_image = soup.find('meta', {'name': 'twitter:image'})['content'] if soup.find('meta', {'name': 'twitter:image'}) else 'No Twitter image'
            twitter_card = soup.find('meta', {'name': 'twitter:card'})['content'] if soup.find('meta', {'name': 'twitter:card'}) else 'No Twitter card'

            # Additional metadata
            keywords = soup.find('meta', {'name': 'keywords'})['content'] if soup.find('meta', {'name': 'keywords'}) else 'No keywords'
            author = soup.find('meta', {'name': 'author'})['content'] if soup.find('meta', {'name': 'author'}) else 'No author'
            published_time = soup.find('meta', {'property': 'article:published_time'})['content'] if soup.find('meta', {'property': 'article:published_time'}) else 'No published time'
            modified_time = soup.find('meta', {'property': 'article:modified_time'})['content'] if soup.find('meta', {'property': 'article:modified_time'}) else 'No modified time'

            return jsonify({
                'title': title,
                'description': description,
                'thumbnail': thumbnail,
                'og_title': og_title,
                'og_description': og_description,
                'og_image': og_image,
                'og_url': og_url,
                'og_type': og_type,
                'twitter_title': twitter_title,
                'twitter_description': twitter_description,
                'twitter_image': twitter_image,
                'twitter_card': twitter_card,
                'keywords': keywords,
                'author': author,
                'published_time': published_time,
                'modified_time': modified_time,
            })
        else:
            return jsonify({'error': 'Failed to fetch the webpage'}), 400
    return jsonify({'error': 'URL parameter is missing'}), 400

# Define the index route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
