from lxml.html import fromstring
import requests
from urllib.parse import urljoin

BASE_URL = 'https://www.naumen.ru'


class UnsupportedStatusCodeException(Exception):
    pass


def parse_interns():
    url = urljoin(BASE_URL, '/career/trainee/')

    page = requests.get(url=url)
    if page.status_code != 200:
        raise UnsupportedStatusCodeException()

    root = fromstring(page.text)

    result = {}
    for i, city in enumerate(root.xpath('//span[contains(@class, "career-menu-tab")]')):
        careers = root.cssselect(
            f'#career-tab{i+1} > div > div > div.trainee-t-line > span > a')

        interns = []
        for intern in careers:
            about_url = urljoin(BASE_URL, intern.get('href'))

            about_page = requests.get(about_url)
            about_root = fromstring(about_page.text)

            test_url = urljoin(BASE_URL, about_root.cssselect(
                '#steps > div > div > a.btn.btn--default.btn--')[0].get('href'))

            interns.append((intern.text_content(), about_url, test_url))

        result[city.text_content()[:len(city.text_content())-1]] = {
            'count': len(interns),
            'interns': interns,
        }

    return result
