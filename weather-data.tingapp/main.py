# coding: utf8
import tingbot
from tingbot import screen
from tingbot.graphics import Image
import requests
import time
import pprint

# datetime formats >> https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
options = {
    'location': 'Boston, MA',
    'unit': 'f',
    'date_format': '%d %B',
    'time_format': '%I:%M %p'
}

data = {
    'location': '',
    'temp': '',
    'description': 'Loading data...',
    'when': '',
    'background_image': None,
    'current_time': '',
    'current_date': ''
}

@tingbot.every(minutes=10)
def refresh_data():
    print 'refreshing...'

    r = requests.get('https://query.yahooapis.com/v1/public/yql', params={
        'q': 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="%s") and u="%s"' % (options['location'], options['unit']),
        'format': 'json',
    })

    r.raise_for_status()

    api_data = r.json()
    pprint.pprint(api_data)

    channel = api_data['query']['results']['channel']
    item = channel['item']
    condition = item['condition']
    data['location'] = channel['location']['city']
    data['temp'] = condition['temp'] + u'\u00b0'
    data['description'] = condition['text']

    code = int(condition['code'])
    gif_name = code_to_gif_map[code]
    data['background_image'] = Image.load(gif_name)
    
    data['current_date'] = time.strftime(options['date_format'])
    data['current_time'] = time.strftime(options['time_format']).lower()

def loop():
    if data['background_image']:
        screen.image(data['background_image'])
    else:
        screen.fill(color='black')

    screen.text (
        data['location'],
        xy=(22,30),
        align='left',
        color='white',
        font='HelveticaNeue-Bold.ttf',
        font_size=24,
    )
    screen.text (
        data['temp'],
        xy=(22,160),
        align='left',
        color='white',
        font='HelveticaNeue-Bold.ttf',
        font_size=70,
    )
    screen.text (
        data['description'],
        xy=(22,213),
        align='left',
        color='white',
        font='HelveticaNeue.ttf',
        font_size=22,
    )
    screen.text (
        data['current_date'],
        xy=(300,190),
        align='right',
        font='HelveticaNeue.ttf',
        font_size=22,
        color='white',
    )
    screen.text (
        data['current_time'],
        xy=(300,213),
        align='right',
        font='HelveticaNeue.ttf',
        font_size=22,
        color='white',
    )

code_to_gif_map = {
    0: 'tornado.gif', #  tornado
    1: 'rainstorm.gif', #  tropical storm
    2: 'rainstorm.gif', #  hurricane
    3: 'rainstorm.gif', #  severe thunderstorms
    4: 'rainstorm.gif', #  thunderstorms
    5: 'snow.gif', #  mixed rain and snow
    6: 'rain.gif', #  mixed rain and sleet
    7: 'snow.gif', #  mixed snow and sleet
    8: 'rain.gif', #  freezing drizzle
    9: 'light-rain.gif', #  drizzle
    10: 'rain.gif', #  freezing rain
    11: 'rain.gif', #  showers
    12: 'rain.gif', #  showers
    13: 'snow.gif', #  snow flurries
    14: 'snow.gif', #  light snow showers
    15: 'snow.gif', #  blowing snow
    16: 'snow.gif', #  snow
    17: 'hail.gif', #  hail
    18: 'snow.gif', #  sleet
    19: 'fine.gif', #  dust
    20: 'fog.gif', #  foggy
    21: 'sunny.gif', #  haze
    22: 'fog.gif', #  smoky
    23: 'windy.gif', #  blustery
    24: 'windy.gif', #  windy
    25: 'sunny2.gif', #  cold
    26: 'clouds.gif', #  cloudy
    27: 'low-cloud.gif', #  mostly cloudy (night)
    28: 'low-cloud.gif', #  mostly cloudy (day)
    29: 'clouds.gif', #  partly cloudy (night)
    30: 'clouds.gif', #  partly cloudy (day)
    31: 'fine.gif', #  clear (night)
    32: 'sunny.gif', #  sunny
    33: 'fine.gif', #  fair (night)
    34: 'fine.gif', #  fair (day)
    35: 'hail.gif', #  mixed rain and hail
    36: 'sunny.gif', #  hot
    37: 'rainstorm.gif', #  isolated thunderstorms
    38: 'rainstorm.gif', #  scattered thunderstorms
    39: 'rainstorm.gif', #  scattered thunderstorms
    40: 'rain.gif', #  scattered showers
    41: 'snow.gif', #  heavy snow
    42: 'snow.gif', #  scattered snow showers
    43: 'snow.gif', #  heavy snow
    44: 'cloudy.gif', #  partly cloudy
    45: 'rain.gif', #  thundershowers
    46: 'snow.gif', #  snow showers
    47: 'rainstorm.gif', #  isolated thundershowers
}

# run the app
tingbot.run(loop)
