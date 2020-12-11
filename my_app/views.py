from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote_plus
from . import models

BASE_CRAIGSLIST_URL = 'https://sandiego.craigslist.org/d/for-sale/search/sss?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, "base.html")


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listing = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listing:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'data:image/jpeg;base64,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'
        final_postings.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings
    }
    return render(request, "my_app/new_search.html", stuff_for_frontend)
