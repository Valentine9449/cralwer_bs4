import json

import requests
from bs4 import BeautifulSoup

headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 '
				  '(KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
	'Referer': 'https://www.sex.com/'
}
dom = 'https://www.lyricsmode.com/'
urls = []
spisok = []
data = []
enter_value = input("enter name of band: ").split()
enter_value = "+".join(enter_value).lower()

url = f"https://www.lyricsmode.com/search.php?search={enter_value}"


def get_urls(url):
	for i in range(1, 10):

		req = requests.get(f'{url}+&p={i}&per-page=50', headers=headers)
		soup = BeautifulSoup(req.text, 'lxml')

		link = soup.find_all(class_='lm-list__cell lm-list__cell-title')

		for items in link:
			for a in items.find_all('a'):
				spisok.append(dom + a['href'])
		return spisok


def clear_title(song_name, band_name):
	carbage = [band_name, "-", "–", "lyrics"]
	for shit in carbage:
		if shit in song_name:
			song_name = song_name.replace(shit, "")

	song_name = song_name.split()
	song_name = ' '.join(song_name)
	return song_name


def clear_lyrics(song_lyrics):
	for character in ["Explain", "Request", "×"]:
		if character in song_lyrics:
			song_lyrics = song_lyrics.replace(character, "").strip()
	return song_lyrics


def parse():
	list_of_urls = get_urls(url=url)
	for items in list_of_urls:
		res = requests.get(items, headers=headers)
		soup = BeautifulSoup(res.text, "lxml")
		name = soup.find("div", class_="article_info").find("span").text

		title = soup.find("div", class_="article_info").find("h1").text
		title = clear_title(song_name=title, band_name=name)

		object_lyrics = soup.find("div", class_='js-new-text-select').text
		object_lyrics = clear_lyrics(object_lyrics)
		data.append(
			{
				"title": title,
				"author": name,
				"lyrics": object_lyrics
			}
		)
		print(data)


if __name__ == "__main__":
	parse()
