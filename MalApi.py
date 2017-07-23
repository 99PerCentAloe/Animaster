import requests

response = requests.get('https://myanimelist.net/api/anime/search.xml?q=bleach')

print(response)