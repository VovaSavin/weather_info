import requests
from bs4 import BeautifulSoup as bs


def take_info_weather() -> list:
    """Возвращает данные о погоде из сайта"""
    try:
        url = "https://pogoda.meta.ua/Kyivska/Kyivskiy/Kyiv/"
        html = requests.get(url).text

        soup = bs(html, "html.parser")
        main = soup.find("main", class_="main")
        div_1 = main.find("div", class_="city__week-wrap")

        div_2 = div_1.select("div", class_="ttt city__day")
        dates = []
        temperature = []
        description = []
        all_data = [dates, temperature, description]

        all_days = []

        for d in div_2:
            ID = d.get('id')
            if ID is not None:
                dates.append(ID)
        iter = 0
        for x in div_2:
            if iter > 0:
                span = x.find("span", class_="min-max")
                span_1 = span.find("span").text
                temperature.append(int(span_1[2:4]))
            iter += 1
        iter = 0
        for x in div_2:
            if iter > 0:
                span = x.find("span", class_="img")
                img = span.find("img")
                description.append(img.get('title'))
            iter += 1
        for y in range(6):
            empty_list = []
            for x in range(3):
                empty_list.append(all_data[x][y])
            all_days.append(tuple(empty_list))
        return all_days
    except requests.exceptions.ConnectionError:
        print("Нет соединения с интернетом...")
