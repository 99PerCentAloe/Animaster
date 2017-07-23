import bs4
from urllib.request import urlopen
import html5lib
url = 'https://sovetromantica.com/anime/280-boruto-naruto-next-generations/episode_15-dubbed'
soup = bs4.BeautifulSoup(urlopen(url),"html5lib")
for link in soup.find_all('source'):
    print(link.get('src'))


