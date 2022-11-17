import requests

def search_by_key(keyword):
    url = "https://newscatcher.p.rapidapi.com/v1/search"

    querystring = {"q":keyword,"lang":"en","sort_by":"relevancy","page":"1","media":"True"}

    headers = {
	    "X-RapidAPI-Key": "",
	    "X-RapidAPI-Host": "newscatcher.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()

    title=[]
    url=[]
    url_img=[]
    for i in response['articles']:
	    title.append(i['title'])
	    url.append(i['link'])
	    url_img.append(i['media_content'][0])

    return title,url,url_img
