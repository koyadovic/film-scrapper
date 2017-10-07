from lxml import html, etree
import requests
import urllib.parse
import re


url_mejortorrent = "http://www.mejortorrent.com"
url_imdb = "http://www.imdb.com/country/es"

def clean_html(raw_html):
  clean_regex = re.compile('<.*?>')
  clean_text = re.sub(clean_regex, '', raw_html)
  return clean_text

# source film page as imdb
page = requests.get(url_imdb)
tree = html.fromstring(page.content)

# get the top list of films
top_films_spain_list = tree.xpath('//td[@class="title"]/a/text()')

results = {}

for film_name in top_films_spain_list:
    # With this we will store all torrent links found for the film
    results[film_name] = []
    print("Buscando enlaces para {}.".format(film_name))

    # construct the query
    query_parameters = {
        'sec'   : 'buscador',
        'valor' : '{}'.format(film_name)
    }
    encoded_query = urllib.parse.urlencode(query_parameters)
    url = url_mejortorrent + "/secciones.php?" + encoded_query

    # search
    torrent_page = requests.get(url)
    tree = html.fromstring(torrent_page.content)

    # get results
    anchors = tree.xpath('//tr[2]//td[1]/a')
    for anchor in anchors:

        # ñapa
        if anchors.index(anchor) == 0:
            continue

        text = clean_html(etree.tostring(anchor, pretty_print=True).decode("utf-8"))
        href = anchor.attrib['href']

        # clean the text
        clean_regexes = ['[\"\'\n]*', '\.?\s*$', '^\s*']
        for r in clean_regexes:
            clean_r = re.compile(r)
            text = re.sub(clean_r, '', text)

        results[film_name].append({
            "name": text,
            "url": url_mejortorrent + href
        })

print("Results:\n{}".format(results))
