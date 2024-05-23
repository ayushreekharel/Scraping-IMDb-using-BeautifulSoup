
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
    ''' 1.Open Google Chrome.
        2.Go to the IMDb website (https://www.imdb.com/).
        3.Right-click anywhere on the page and select "Inspect" from the context menu.
        4.In the developer tools, go to the "Network" tab.
        5.Refresh the page (press F5).
        6.It will show the list and you shoul click on the first one. You will see response header, request header. You need request header.

  '''  
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



