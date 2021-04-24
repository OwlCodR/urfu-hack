from lxml.html import fromstring
import requests

BASE_URL = 'https://www.naumen.ru'


class UnsupportedStatusCodeException(Exception):
    pass


def parse_interns():
    url = BASE_URL + '/career/trainee/'

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
            interns.append(
                (intern.text_content(), BASE_URL + intern.get('href')))

        result[city.text_content()[:len(city.text_content())-1]] = {
            'count': len(interns),
            'interns': interns
        }

    return result


if __name__ == '__main__':
    print(parse_interns())
