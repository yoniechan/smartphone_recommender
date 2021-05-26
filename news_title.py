import requests
from bs4 import BeautifulSoup

# pip install requests
# pip install bs4

def getAllCategoryLinks():
    returnMap = {}
    r = requests.get('https://www.blocktempo.com/')
    soup = BeautifulSoup(r.text, 'html.parser')
    menus = soup.select('ul[class="sub-menu"] li')
    for menu in menus:
        returnMap[menu.get_text()] = menu.select('a')[0].get('href')
    return returnMap

def crawl(categoryName, categoryLink):
    f = open(categoryName+'.csv', 'a', encoding="utf8")
    r = requests.get(categoryLink)
    soup = BeautifulSoup(r.text, 'html.parser')
    page_number = int(soup.select('a[class="page_number"]')[-1].get_text())
    for page in range(1, page_number+1):
        r = requests.get(categoryLink+'page/'+str(page))
        soup = BeautifulSoup(r.text, 'html.parser')
        postElements = soup.select('article[class="jeg_post jeg_pl_lg_2 format-standard"]')
        for post in postElements:
            title = post.select('h3[class="jeg_post_title"]')[0].get_text().replace('\n', '')
            publishDate = post.select('div[class="jeg_meta_date"]')[0].get_text()
            author = post.select('div[class="jeg_meta_author"] a')[0].get_text()
            #print(title+','+publishDate+','+author)
            f.write(publishDate+','+author+','+title+'\n')
            f.flush()
    f.close()

returnMap = getAllCategoryLinks()
for key in returnMap.keys():
    crawl(key, returnMap[key])