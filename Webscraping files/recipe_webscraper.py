#THIS ONLY WORKS FOR ALLRECIPES.COM

#you need to download unirest, beautifulsoup, requests, and json if you dont have them
#pip install beautifulsoup4 
#pip install BeautifulSoup
#pip install jsonschema
#pip install requests
#pip install Unirest 
import unirest 
from bs4 import BeautifulSoup
import requests
import json

urlstack=['http://allrecipes.com/recipes/']#change this and lines 35+42 if you want to parse a different website
out_file=''#change to name of file
visitedsites=[]
recipes={}

while len(urlstack)>0 and len(recipes)<100:
	#get a url
    url=urlstack.pop()
    #we've visited this url now
    visitedsites.append(url)

    #if its a recipe parse it
    if 'allrecipes.com/recipe/' in url:
        element = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/extract?forceExtraction=false&url="+url,
        headers={
            "X-Mashape-Key": ""#get the key from the account
        })
        if element.body['extendedIngredients']!=None and element.body['instructions']!=None and element.body['imageUrls']!=None:
            recipes[str(element.body['title'])]=[element.body['extendedIngredients'],element.body['instructions'],element.body['imageUrls']]

    #scrape the page for other links
    if(len(urlstack)<50 and 'allrecipes.com' in url and 'account' not in url):#Website specific
        soup=BeautifulSoup(requests.get(url).text)
        souper=soup.find_all('a')
        for link in souper:
            text=link.get('href')
            if text!=None:
                if'http://' not in text:
                    text='http://allrecipes.com'+text#website specific
                if text not in visitedsites:
                    urlstack.append(text)
#                print(text)
    print(str(len(visitedsites))+' sites visited.')
    print(str(len(recipes))+' parsed.')

#dump it into a json            
with open(out_file,'w') as recipe_json:
    json.dump(recipes,recipe_json)
