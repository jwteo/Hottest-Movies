from bs4 import BeautifulSoup
import requests
import pandas as pd

movie_titles = []
release_dates = []
ratings = []
metascores = []
userscores = []

pages = [i for i in range(0,4)]
for page in pages:
    source = requests.get(f'https://www.metacritic.com/browse/movies/score/metascore/year/filtered?page={page}').text
    soup = BeautifulSoup(source, 'lxml')
    for movie in soup.find_all('td', class_="clamp-summary-wrap"):
        #print(movie.prettify())
        movie_title = movie.find('a', class_='title').h3.text
        movie_titles.append(movie_title)

        release_date = movie.find('div', class_='clamp-details').span.text
        release_dates.append(release_date)

        try:
            rating = movie.select('div.clamp-details span')[1].text
            ratings.append(rating)
        except Exception as e:
            ratings.append('None')

        metascore = movie.select('a.metascore_anchor div')[0].text
        metascores.append(metascore)

        user_score = movie.select('a.metascore_anchor div')[2].text
        userscores.append(user_score)

movie_stuff = pd.DataFrame({
    'Movie titles': movie_titles,
    'Release Dates': release_dates,
    'Ratings': ratings,
    'Meta-scores': metascores,
    'User-scores': userscores
})
print(movie_stuff)
movie_stuff.to_csv('movies.csv')
