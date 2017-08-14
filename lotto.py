#lotto.py
#script to check lotto results from tickets.txt to results posted on masslottery.com
#script will check Mega Millions, Powerball, Lucky for life, and Megabucks Doubler
#the script should run after midnight to check previous day since some games update at 11:45pm.
#does not check for sundays results(monday morning) as these games do not draw on sunday.

import json
import urllib.request
import datetime, logging, sys

outMsg = '\nLotto Results\n '   #output Message
loopCount = 0                   
match = 0
ball = 0

logging.basicConfig(filename = 'lottoerror.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)

#games stores our ticket info
games = {'Mega Millions': {'numbers':'0', 'ball':'0'},
         'Powerball': {'numbers':'0', 'ball':'0'},
         'Megabucks Doubler': {'numbers':'0', 'ball':'0'},
         'Lucky for Life': {'numbers':'0', 'ball':'0'}
         }

gameNames = ['Mega Millions', 'Powerball', 'Lucky for Life', 'Megabucks Doubler']

#gamePrize stores winning ticket value. stored in format [game[!ball:[matches:prize], ball:[matches:prize]]]
gamePrize = {'Mega Millions':     {'0' : {'0':'0', '1':'0', '2':'0', '3':'5', '4':'500', '5':'1000000', '6': '0'},
                                   '1' : {'0':'1', '1':'2', '2':'5', '3':'50', '4':'5000', '5':'1000000', '6': '0'}},
             'Powerball':         {'0' : {'0':'0', '1':'0', '2':'0', '3':'7', '4':'100', '5':'1000000', '6': '0'},
                                   '1' : {'0':'4', '1':'4', '2':'7', '3':'100', '4':'50000', '5':'1000000', '6': '0'}},
             'Lucky for Life':    {'0' : {'0':'0', '1':'0', '2':'3', '3':'20', '4':'200', '5':'25000', '6': '0'},
                                   '1' : {'0':'4', '1':'6', '2':'25', '3':'150', '4':'5000', '5':'1000000', '6': '0'}},
             'Megabucks Doubler': {'0' : {'0':'0', '1':'0', '2':'0', '3':'2', '4':'100', '5':'2500', '6':'7000'},
                                   '1' : {'0':'0', '1':'0', '2':'0', '3':'4', '4':'200', '5':'5000', '6':'7000'}}
             }

#use yesterdays date, some games update at 11:45pm local time so script should run after midnight
#exit if yesterday was sunday
yesterday = datetime.datetime.now() - datetime.timedelta(days = 2)
yesterdayDate= (yesterday.strftime("%A")) 
if yesterdayDate == 'Sunday': 
    sys.exit()

#read in ticket info, store in games
try:
    with open("tickets.txt", 'r') as lottotext:
        for line in lottotext:  
            line = line.split('\n')[0]
            line = line.split(':')
            games[line[0]]['numbers']=line[1]
            games[line[0]]['ball']=line[2]
            #games[line[0]]['date']=line[3]
except:
    logging.error('Failed read tickets.txt')
    sys.exit()

#get lotto results from website, store in webData
try:                    
    websource = urllib.request.urlopen('http://www.masslottery.com/data/json/games/lottery/recent.json')
except:
    logging.error('Failed to connect to web site')
    sys.exit()
    
webData = json.loads(websource.read().decode())

#loop through webData, and check our numbers to drawn numbers if numbers were drawn last night
while (loopCount <= (len(gameNames) -1)):
    match = 0
    ball = 0
    if (yesterdayDate == webData['games'][loopCount]['draw_date_name']):
        GameNumbers = webData['games'][loopCount]['winning_num'].split('-')
        OurNumbers = games[gameNames[loopCount]]['numbers'].split('-')
        for number in OurNumbers: 
            if number in GameNumbers:
                match = match +1
        #add game info, numbers, matches to outMsg so it can be printed or emailed
        outMsg += "\nGame: " + webData['games'][loopCount]['game_name']
        outMsg += "\nDate: " + webData['games'][loopCount]['draw_date_name']
        outMsg += "\nJackpot: " +webData['games'][loopCount]['estimated_jackpot']
        if loopCount == 3: #Megabucks Doubler has a different format
            outMsg += "\nNumbers: " + webData['games'][loopCount]['winning_num'] + " Bonus: " + webData['games'][loopCount]['bonus']
            outMsg += "\nOur Num: " + games[gameNames[loopCount]]['numbers'] + " Bonus: " + games[gameNames[loopCount]]['ball']
            outMsg += "\nMatches: " + str(match)
            if (webData['games'][loopCount]['bonus'] != games[gameNames[loopCount]]['ball']):
                outMsg += ",   Bonus: No Match"
            else:
                outMsg += ",   Bonus: Match"
                ball = 1
        else: #format for MM, PB, LFL
            outMsg += "\nNumbers: " + webData['games'][loopCount]['winning_num'] + " Ball:" + webData['games'][loopCount]['ball']
            outMsg += "\nOur Num: " + games[gameNames[loopCount]]['numbers'] +" Ball:" + games[gameNames[loopCount]]['ball']
            outMsg += "\nMatches: " + str(match)
            if (webData['games'][loopCount]['ball'] != games[gameNames[loopCount]]['ball']):
                outMsg += ",   Ball: No match"
            else:
                outMsg +=",   Ball: Match"
                ball = 1
        #get winnings, then loop
        gameWin = gamePrize[gameNames[loopCount]][str(ball)][str(match)]
        outMsg += "\nWinnings: $" + gameWin
        outMsg += "\nVideo: " + webData['games'][loopCount]['video'] + "\n"
    loopCount = loopCount + 1

#print results
print (yesterdayDate, 'results:', outMsg)


