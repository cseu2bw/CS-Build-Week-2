import requests
import json

__URL_INIT = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/'
TOKEN = 'c932989216c6ac25c7d6ae99558dd6b24fd3af18'
def game():
    response = requests.get(__URL_INIT, headers={'Authorization': TOKEN})
    # response = requests.urlopen(req)
    # page = response.read()
    print(response.status_code)
    # print(json.loads(response.content.decode('utf-8')))


game()