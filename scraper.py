import requests
from bs4 import BeautifulSoup


def scraper():
    website = "https://strikeout.im/"
    r = requests.get(website)

    soup = BeautifulSoup(r.content, 'lxml')
    print(soup.prettify())


if __name__ == '__main__':
    scraper()
