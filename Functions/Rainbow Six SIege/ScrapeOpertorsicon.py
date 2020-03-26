#Scrape entire operator's icon
#To prevent for new operator problem, i select double url open 

import discord
import asyncio
import os
from discord.ext import commands
import urllib
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import re # Regex for youtube link
import warnings
import requests

unisoftURL = "https://www.ubisoft.com"
rainbowSixSiegeOperatorIconURL = "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/game-info/operators"
html = requests.get(rainbowSixSiegeOperatorIconURL).text
bs = BeautifulSoup(html,'html.parser')

operatoriconURLDict = dict()

#Get oprators' pages with ccid
operatorListDiv = bs.findAll('div',{'ccid' : re.compile('[0-9A-Za-z]*')})
print(len(operatorListDiv))
for ind in range(0,len(operatorListDiv)):
    print(ind + 1)
    operatormainURL = operatorListDiv[ind].a['href']
    #Get Operator's name
    operatorname = operatormainURL.split('/')[-1]
    #Open URL : each operator's pages
    html2 = requests.get(unisoftURL + operatormainURL).text
    bs2 = BeautifulSoup(html2, 'html.parser')
    operatoriconURL = bs2.find('div',{'class' : "operator__header__icons__names"}).img['src']
    operatoriconURLDict[operatorname] = operatoriconURL
