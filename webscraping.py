
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_movie_data(url, headers):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    movie_list_items = soup.find_all('li', class_='ipc-metadata-list-summary-item')

    movie_titles = []
    years = []
    movie_times = []
    categories = []
    descriptions = []
    metascores = []
    ratings = []

    for item in movie_list_items:
        title_data = item.find('h3', class_='ipc-title__text')
        if title_data:
            title = title_data.text.strip()
            movie_titles.append(title)

        year_data = item.find('span', class_='sc-b189961a-8 kLaxqf dli-title-metadata-item')
        if year_data:
            year = year_data.text.strip()
            years.append(year)

        time_data = item.find_all('span', class_='sc-b189961a-8 kLaxqf dli-time-metadata-item')
        if time_data and len(time_data) >= 2:
            time = time_data[1].text.strip()
            movie_times.append(time)
        else:
            movie_times.append(None)

        categories_data = item.find_all('span', class_='sc-b189961a-8 kLaxqf dli-title-metadata-item')[-1]
        if categories_data:
            category = categories_data.text.strip()
            categories.append(category)

        description_data = item.find('div', class_='ipc-html-content-inner-div')
        if description_data:
            description = description_data.text.strip()
            descriptions.append(description)

        metascore_data = item.find('span', class_='metacritic-score-box')
        if metascore_data:
            metascore = metascore_data.text.strip()
            metascores.append(metascore)
        else:
            metascores.append(None)

        rating_data = item.find('span', class_='ipc-rating-star--base')
        if rating_data:
            rating = rating_data.text.strip()
            ratings.append(rating)
        else:
            ratings.append(None)

    return movie_titles, years, movie_times, categories, descriptions, metascores, ratings

url = "https://www.imdb.com/search/title/?groups=top_1000&count=100&sort=user_rating,desc"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "max-age=0",
    "Cookie": "session-id=138-0701897-3551105; session-id-time=2082787201l; ubid-main=134-9621333-6174418; ad-oo=0; ci=e30; session-token=dmm4f2V9rJdJ2mWfrboVnsrQCCfixIIQWsY9nsXy9VcRlPx5kDkYKXPF09syU11pjZ2CMbjWB7BMs3bYHUSfx+sDDzI8zI4TMRuGbxQikwvJKHdi5VlEgsbNhInHu2BoQBBOcwf2qNaCmR6wLDyLwmJE7FaUgu9CsgFZdlYGxKi3NcbxDgQqguBB3epbMawS1Se34brYlz5MzVnVTnBnsQBlgz57ZT0QdRJkYw2AKZ+gMjRddPRQ4homTe2bvxCm7Ljmf0ukizTi7yery3CfSfl185XOU6vYrI/ts+7RvlW5W3S0b/S5Aa9/CcZ7PviSZyV3nOKNrRz/t5zHTIfnxr6tTVZ6d9eB; csm-hit=tb:84B9PJ7YPJ1JAVN8HKFC+s-84B9PJ7YPJ1JAVN8HKFC|1716433590622&t:1716433590622&adb:adblk_no",
    "Referer": "https://www.google.com/",
    "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

movie_titles, years, movie_times, categories, descriptions, metascores, ratings = get_movie_data(url, headers)

df = pd.DataFrame({
    "Name": movie_titles,
    "Released year": years,
    "Duration": movie_times,
    "Categories": categories,
    "Description": descriptions,
    "Metascores": metascores,
    "Ratings": ratings
})

print(df.head(5))

df.to_csv("imdb_top100_movie.csv",index=False)



