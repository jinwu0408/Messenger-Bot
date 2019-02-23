import os, sys
from flask import Flask, request
import requests
from pymessenger import Bot, Element
#from pymessager import Messager
from bs4 import BeautifulSoup
page = requests.get('https://www.amctheatres.com/movie-theatres/los-angeles/amc-puente-hills-20/showtimes/all/2019-02-22/amc-puente-hills-20/all')
soup = BeautifulSoup(page.content, 'html.parser')


app = Flask(__name__)

  
PAGE_ACCESS_TOKEN = "EAAEeZAK2nCw8BAFH7jSoWk651S1MFi1JjffLioGOUw7ANxj8D4tZBWYugN4O0LOHbYnoLQfC0EwVZArZB4GZCBq5yZC5hIeViTbntsPRsHAMPzJmj7CPZAOAuUqYu8wWf4BvbEFKC7OAwQgRdf2Ri4nkcu8VMGNJrqFQh77QDQZCU9EPFxg31THZA"
VERIFICATION_TOKEN = "1234"
bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
# Webhook validation
def verify():
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Success!", 200

  
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)
    if data['object'] == 'page':
      for entry in data['entry']:
        for messaging_event in entry['messaging']:
          sender_id = messaging_event['sender']['id']
          if messaging_event.get('message'):
            if messaging_event['message'].get('text'):
              # Retrieve the message
              msg = messaging_event['message']['text'] 
              #movies = soup.findAll('div', attrs={'class':'ShowtimesByTheatre-film'})
              if msg == 'movie' or msg == 'Movie':
                movie_list = ""
                #all the movie
                all_movie = soup.findAll('div', attrs={'class':'ShowtimesByTheatre-film'})
                #loop through each movie
                for div_item in all_movie:
                  #get the movie name
                  title_block = div_item.findChildren('h2')
                  title = str.strip(title_block[0].text)
                  movie_list += (title + ":\n")
                  #get showtime what is valid
                  show_block = div_item.findAll('a', attrs= {'aria-disabled': 'false'})
                  for each_time in show_block:
                    #get the showtime and hyperlink
                    showtime = each_time.getText()
                    hlink = each_time['href']
                    hyperlink = ('www.amctheatres.com/showtimes'+ hlink.split("showtimes",1)[1])
                    #print("hlink is: {}".format(hyperlink))
                    #hyperlink_format = '<a href="{link}">{text}</a>'<a href = hyperlink>showtime</a>
                    movie_list += (showtime + " ")
                    #movie_list += str(hyperlink + "\n")
                    
                  movie_list += "\n\n"
                
                #elements = []
               #element = Element(title="test", image_url="<arsenal_logo.png>", subtitle="subtitle", item_url="http://arsenal.com")
                #elements.append(element)
                # Echo the message
                
                bot.send_text_message(sender_id, movie_list)
                #print(movie_list)
    return 'OK', 200
  
def log(message):
    from pprint import pprint
    #pprint(message)
    sys.stdout.flush()
    
    
if __name__ == "__main__":
  app.run()
