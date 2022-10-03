import sys
PY3 = sys.version_info[0] == 3
if PY3:
    from urllib.parse import urlparse, parse_qs, quote, unquote, quote_plus, unquote_plus
else:
    from urlparse import urlparse, parse_qs
    from urllib import quote, unquote, quote_plus, unquote_plus
from bs4 import BeautifulSoup
import requests
import json
import re
from datetime import datetime
import logging
log = logging.getLogger("simpleimdb")


class imdb:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'Upgrade-Insecure-Requests': '1', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1', 'Sec-Fetch-Dest': 'document'}
    def open_url(self,url,headers,post=False,json_post=False,timeout=False):
        if timeout and json_post:
            try:
                r = requests.post(url,headers=headers,json=json_post,timeout=timeout)
            except requests.exceptions.RequestException as e:
                msg = '###########ERROR:###########\nurl: %sreason: %s'%(url,e)
                log.warning(msg)        
        if timeout and post:
            try:
                r = requests.post(url,headers=headers,data=post,timeout=timeout)
            except requests.exceptions.RequestException as e:
                msg = '###########ERROR:###########\nurl: %sreason: %s'%(url,e)
                log.warning(msg)
        elif timeout:
            try:
                r = requests.get(url,headers=headers,timeout=timeout)
            except requests.exceptions.RequestException as e:
                msg = '###########ERROR:###########\nurl: %sreason: %s'%(url,e)
                log.warning(msg)
        elif post:
            try:
                r = requests.post(url,headers=headers,data=post,timeout=timeout)
            except requests.exceptions.RequestException as e:
                msg = '###########ERROR:###########\nurl: %sreason: %s'%(url,e)
                log.warning(msg)
        elif json_post:
            try:
                r = requests.post(url,headers=headers,json=json_post)
            except requests.exceptions.RequestException as e:
                msg = '###########ERROR:###########\nurl: %sreason: %s'%(url,e)
                log.warning(msg)                                
        else:
            try:
                r = requests.get(url,headers=headers)
            except requests.exceptions.RequestException as e:
                msg = '###########ERROR:###########\nurl: %sreason: %s'%(url,e)
                log.warning(msg)
        try:
            html = r.text
        except:
            html = ''        
        if html:
            try:
                html = html.decode('utf-8')
            except:
                pass
        return html    
    def soup(self,html):
        try:
            soup = BeautifulSoup(html, 'html.parser')
        except:
            logging.debug('fails to use beaultifulsoap')
            soup = ''
        return soup
    def scrape_trailer(self,url):
        html = self.open_url(url=url,headers=self.headers)
        try:
            stream = re.findall('{"value":"1080p",.+?,{"mimeType":"video/mp4","url":"(.*?)"',html)[0]
            stream = stream.encode('utf-8').decode('unicode_escape')
        except:
            stream = url
        return stream

    def get_movie(self,imdb,lang='en',timeout=False,trailer=True):
        url = 'https://www.imdb.com/title/' + imdb + '/?ref_=nv_sr_srsg_0' 
        language = {'Accept-Language': lang}
        headers = self.headers
        headers.update(language)
        html = self.open_url(url=url,headers=headers)
        try:
            json_text = re.findall('json">(.*?)<',html)[0]
        except:
            json_text = ''
            logging.debug('scrape fail')
        if json_text:
            json_format = json.loads(json_text)
            title = json_format.get("name")
            description = json_format.get("description")
            thumbnail = json_format.get("image")
            if trailer:
                try:
                    trailer = self.scrape_trailer(json_format.get("trailer").get("embedUrl"))
                except:
                    trailer = ''
            else:
                trailer = ''
            try:
                fanart = json_format.get("trailer").get("thumbnail").get("contentUrl")
            except:
                fanart = ''
            try:
                actors = [i.get("name") for i in json_format.get("actor") if i.get("name") !=None]
            except:
                actors = []
            try:
                director = [i.get("name") for i in json_format.get("director") if i.get("name") !=None]
            except:
                director = []
            try:
                writers = [i.get("name") for i in json_format.get("creator") if i.get("name") !=None]
            except:
                writers = []
            try:
                duration_imdb = json_format.get("duration")
            except:
                duration_imdb = ''
            try:
                hour = duration_imdb.split("PT")[1]
                hour = hour.split('H')[0]
                hour = int(hour) * 60
            except:
                hour = False
            try:
                minute = duration_imdb.split("H")[1]
                minute = minute.split("M")[0]
                minute = int(minute)
            except:
                minute = False
            if hour and minute:
                duration = hour + minute
            else:
                duration = ''
            try:
                rating = json_format.get("aggregateRating").get("ratingValue")
            except:
                rating = ''
            try:
                votes = json_format.get("aggregateRating").get("ratingCount")
            except:
                votes = ''
            contentRating = json_format.get("contentRating") #age
            genre = json_format.get("genre")
            released = json_format.get("datePublished")
            to_dict = {'title': title,
            'description': description,
            'trailer': trailer,
            'thumbnail': thumbnail,            
            'fanart': fanart,
            'actors': actors,
            'director': director,
            'writers': writers,
            'duration': duration,
            'rating': rating,
            'votes': votes,
            'contentRating': contentRating,
            'genre': genre,
            'released': released
            }
        else:
            to_dict = {}
        return to_dict
    
    def get_tvshow(self,imdb,lang='en',timeout=False,trailer=True):
        url = 'https://www.imdb.com/title/' + imdb + '/?ref_=nv_sr_srsg_0'
        language = {'Accept-Language': lang}
        headers = self.headers
        headers.update(language)
        html = self.open_url(url=url,headers=headers)
        soup = self.soup(html)
        duration = ''
        try:
            li = soup.find_all("li", {"class": "ipc-inline-list__item"})
        except:
            li = False
        if li:
            for i in li:
                try:
                    text = (i.text).replace(" ", "")
                    if 'min' in text or 'm' in text:
                        if len(text) == 3:
                            duration += text[:-1]
                        elif len(text) == 5:
                            duration += text[:-3]
                        break
                except:
                    pass
        try:
            json_text = re.findall('json">(.*?)<',html)[0]
        except:
            json_text = ''
            logging.debug('scrape fail')
        if json_text:
            json_format = json.loads(json_text)
            title = json_format.get("name")
            description = json_format.get("description")
            thumbnail = json_format.get("image")
            if trailer:
                try:
                    trailer = self.scrape_trailer(json_format.get("trailer").get("embedUrl"))
                except:
                    trailer = ''
            else:
                trailer = ''
            try:
                fanart = json_format.get("trailer").get("thumbnail").get("contentUrl")
            except:
                fanart = ''
            try:
                actors = [i.get("name") for i in json_format.get("actor") if i.get("name") !=None]
            except:
                actors = []
            try:
                creator = [i.get("name") for i in json_format.get("creator") if i.get("name") !=None]
            except:
                creator = []
            try:
                rating = json_format.get("aggregateRating").get("ratingValue")
            except:
                rating = ''
            try:
                votes = json_format.get("aggregateRating").get("ratingCount")
            except:
                votes = ''
            contentRating = json_format.get("contentRating") #age
            genre = json_format.get("genre")
            released = json_format.get("datePublished")
            to_dict = {'title': title,
            'description': description,
            'trailer': trailer,
            'thumbnail': thumbnail,            
            'fanart': fanart,
            'actors': actors,
            'creator': creator,
            'duration': duration,
            'rating': rating,
            'votes': votes,
            'contentRating': contentRating,
            'genre': genre,
            'released': released
            }
            url = 'https://www.imdb.com/title/'+imdb+'/episodes/?ref_=tt_ov_epl'
            html = self.open_url(url=url,headers=headers)
            if html:
                soup = self.soup(html)
                try:
                    total_seasons = len(soup.find("select", {"id": "bySeason"}).find_all("option"))
                except:
                    total_seasons = 1
                if total_seasons:
                    season_list = []
                    for season in range(1,total_seasons+1):
                        url = 'https://www.imdb.com/title/'+imdb+'/episodes/_ajax?season='+str(season)
                        html = self.open_url(url=url,headers=headers)
                        soup = self.soup(html)
                        div = soup.find_all("div", class_=re.compile("^list_item"))
                        episode_list = []
                        if div:
                            for i in div:
                                title = i.find("a").get("title")
                                try:
                                    img = i.find("img").get("src")
                                except:
                                    img = ''
                                try:
                                    if img:
                                        img = img.split("@")[0]
                                        img = img + '@._V1_.jpg'
                                except:
                                    pass
                                airdate = (i.find("div", {"class": "airdate"}).text).replace("  ", "").replace("\n", "").replace("\r", "") if i.find("div", {"class": "airdate"}) else ''
                                episode = i.find("meta").get("content")
                                description = (i.find("div", {"class": "item_description"}).text).replace("\n", "").replace("\r", "") if i.find("div", {"class": "item_description"}) else ''
                                rating = i.find("span", {"class": "ipl-rating-star__rating"}).text if i.find("span", {"class": "ipl-rating-star__rating"}) else ''
                                votes = (i.find("span", {"class": "ipl-rating-star__total-votes"}).text).replace("(", "").replace(")", "") if i.find("span", {"class": "ipl-rating-star__total-votes"}) else ''
                                episode_list.append({'episode': episode,'title': title, 'description': description, 'thumbnail': img, 'airdate': airdate, 'rating': rating, 'votes': votes})
                            season_list.append({'season': season,'episodes': episode_list})
                    if season_list:
                        to_dict.update({'seasons': season_list})               
        else:
            to_dict = {}
        return to_dict
    
    def new_movies(self,count=25,lang='en',trailer=True,next=False):
        if next:
            url = next
        else:
            url = 'https://www.imdb.com/search/title/?title_type=feature,tv_movie&num_votes=1000,&production_status=released&sort=moviemeter,asc&count=%s&start=1'%str(count)
        language = {'Accept-Language': lang}
        headers = self.headers
        headers.update(language)
        movies = []
        next = False        
        html = self.open_url(url=url,headers=headers)
        soup = self.soup(html)
        h3 = soup.find_all("h3", {"class": "lister-item-header"})
        desc = soup.find("div", {"class": "desc"})
        if h3:
            for i in h3:
                href = i.find("a").get("href")
                try:
                    imdb = href.split("title/")[1]
                    imdb = imdb.split("/")[0]
                except:
                    imdb = False
                if imdb:
                    dict_movie = self.get_movie(imdb=imdb,lang=lang,trailer=trailer)
                    movies.append(dict_movie)
        if desc:
            href = desc.find("a").get("href")
            if href:
                next = 'https://www.imdb.com' + href
        return movies, next

    def movies_in_threaters(self,count=25,lang='en',trailer=True,next=False):
        date = datetime.now()
        day = date.strftime('%d')
        month = date.strftime('%m')
        year = date.strftime('%y')
        year_before = int(year) - 1
        date_before = '%s-%s-%s'%(str(year_before),month,day)
        date_after = '%s-%s-%s'%(year,month,day)
        if next:
            url = next
        else:
            url = 'https://www.imdb.com/search/title/?title_type=feature&num_votes=1000,&release_date=%s,%s&sort=moviemeter,asc&count=%s&start=1'%(str(date_before),str(date_after),str(count))
        movies = []
        next = False
        language = {'Accept-Language': lang}
        headers = self.headers
        headers.update(language)               
        html = self.open_url(url=url,headers=headers)
        soup = self.soup(html)
        h3 = soup.find_all("h3", {"class": "lister-item-header"})
        desc = soup.find("div", {"class": "desc"})
        if h3:
            for i in h3:
                href = i.find("a").get("href")
                try:
                    imdb = href.split("title/")[1]
                    imdb = imdb.split("/")[0]
                except:
                    imdb = False
                if imdb:
                    dict_movie = self.get_movie(imdb=imdb,lang=lang,trailer=trailer)
                    movies.append(dict_movie)
        if desc:
            href = desc.find("a").get("href")
            if href:
                next = 'https://www.imdb.com' + href
        return movies, next

    def movies_most_popular(self,count=25,lang='en',trailer=True,next=False):
        if next:
            url = next
        else:
            url = 'https://www.imdb.com/search/title/?title_type=feature,tv_movie&num_votes=1000,&production_status=released&groups=top_1000&sort=moviemeter,asc&count=%s&start=1'%str(count)
        movies = []
        next = False
        language = {'Accept-Language': lang}
        headers = self.headers
        headers.update(language)               
        html = self.open_url(url=url,headers=headers)
        soup = self.soup(html)
        h3 = soup.find_all("h3", {"class": "lister-item-header"})
        desc = soup.find("div", {"class": "desc"})
        if h3:
            for i in h3:
                href = i.find("a").get("href")
                try:
                    imdb = href.split("title/")[1]
                    imdb = imdb.split("/")[0]
                except:
                    imdb = False
                if imdb:
                    dict_movie = self.get_movie(imdb=imdb,lang=lang,trailer=trailer)
                    movies.append(dict_movie)
        if desc:
            href = desc.find("a").get("href")
            if href:
                next = 'https://www.imdb.com' + href
        return movies, next

    def movies_oscar_winners(self,count=25,lang='en',trailer=True,next=False):
        if next:
            url = next
        else:
            url = 'https://www.imdb.com/search/title/?title_type=feature,tv_movie&production_status=released&groups=oscar_best_picture_winners&sort=year,desc&count=%s&start=1'%str(count)
        movies = []
        next = False
        language = {'Accept-Language': lang}
        headers = self.headers
        headers.update(language)               
        html = self.open_url(url=url,headers=headers)
        soup = self.soup(html)
        h3 = soup.find_all("h3", {"class": "lister-item-header"})
        desc = soup.find("div", {"class": "desc"})
        if h3:
            for i in h3:
                href = i.find("a").get("href")
                try:
                    imdb = href.split("title/")[1]
                    imdb = imdb.split("/")[0]
                except:
                    imdb = False
                if imdb:
                    dict_movie = self.get_movie(imdb=imdb,lang=lang,trailer=trailer)
                    movies.append(dict_movie)
        if desc:
            href = desc.find("a").get("href")
            if href:
                next = 'https://www.imdb.com' + href
        return movies, next

    def new_tvshows(self,count=25,lang='en',trailer=True,next=False):
        date = datetime.now()
        day = date.strftime('%d')
        month = date.strftime('%m')
        year = date.strftime('%y')
        year_before = int(year) - 1
        date_before = '%s-%s-%s'%(str(year_before),month,day)
        date_after = '%s-%s-%s'%(year,month,day)
        if next:
            url = next
        else:
            url = 'https://www.imdb.com/search/title/?title_type=tv_series,mini_series&languages=en&num_votes=10,&release_date=%s,%s&sort=release_date,desc&count=%s&start=1'%(str(date_before),str(date_after),str(count))
        tvshows = []
        next = False
        language = {'Accept-Language': lang}
        headers = self.headers
        headers.update(language)               
        html = self.open_url(url=url,headers=headers)
        soup = self.soup(html)
        h3 = soup.find_all("h3", {"class": "lister-item-header"})
        desc = soup.find("div", {"class": "desc"})
        if h3:
            for i in h3:
                href = i.find("a").get("href")
                try:
                    imdb = href.split("title/")[1]
                    imdb = imdb.split("/")[0]
                except:
                    imdb = False
                if imdb:
                   dict_tvshow = self.get_tvshow(imdb=imdb,lang=lang,trailer=trailer)
                   tvshows.append(dict_tvshow)
        if desc:
            href = desc.find("a").get("href")
            if href:
                next = 'https://www.imdb.com' + href
        return tvshows, next

    def most_popular_tvshows(self,count=25,lang='en',trailer=True,next=False):
        date = datetime.now()
        day = date.strftime('%d')
        month = date.strftime('%m')
        year = date.strftime('%y')
        date_actual = '%s-%s-%s'%(year,month,day)
        if next:
            url = next
        else:
            url = 'https://www.imdb.com/search/title/?title_type=tv_series,mini_series&num_votes=100,&release_date=,%s&sort=moviemeter,asc&count=%s&start=1'%(str(date_actual),str(count))
        tvshows = []
        next = False
        language = {'Accept-Language': lang}
        headers = self.headers
        headers.update(language)               
        html = self.open_url(url=url,headers=headers)
        soup = self.soup(html)
        h3 = soup.find_all("h3", {"class": "lister-item-header"})
        desc = soup.find("div", {"class": "desc"})
        if h3:
            for i in h3:
                href = i.find("a").get("href")
                try:
                    imdb = href.split("title/")[1]
                    imdb = imdb.split("/")[0]
                except:
                    imdb = False
                if imdb:
                   dict_tvshow = self.get_tvshow(imdb=imdb,lang=lang,trailer=trailer)
                   tvshows.append(dict_tvshow)
        if desc:
            href = desc.find("a").get("href")
            if href:
                next = 'https://www.imdb.com' + href
        return tvshows, next               
