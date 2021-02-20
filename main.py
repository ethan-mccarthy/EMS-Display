#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
from logbook import *
from maintenanceDuty import *
from announcements import *
import textwrap
import pyqrcode
import png
import bitlyshortener
from datetime import datetime

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

try:
    tokens_pool = ['PLACE YOUR BITLY API TOKEN HERE']
    shortener = bitlyshortener.Shortener(tokens=tokens_pool, max_cache_size=256)

    print("UCLA EMS Display")
    epd = epd7in5_V2.EPD()
    
    print("Clearing display")
    epd.init()

    font24 = ImageFont.truetype(os.path.join(picdir, 'arial.ttf'), 24)
    font24bold = ImageFont.truetype(os.path.join(picdir, 'arialbd.ttf'), 24)
    font24italic = ImageFont.truetype(os.path.join(picdir, 'ariali.ttf'), 24)
    font24bolditalic = ImageFont.truetype(os.path.join(picdir, 'arialbi.ttf'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'arial.ttf'), 18)
    font18bold = ImageFont.truetype(os.path.join(picdir, 'arialbd.ttf'), 18)
    font18italic = ImageFont.truetype(os.path.join(picdir, 'ariali.ttf'), 18)
    font18bolditalic = ImageFont.truetype(os.path.join(picdir, 'arialbi.ttf'), 18)
    font12 = ImageFont.truetype(os.path.join(picdir, 'arial.ttf'), 12)
    font14 = ImageFont.truetype(os.path.join(picdir, 'arial.ttf'), 14)

    print("Getting maintenance data...")
    maintenanceData = getMaintenanceData(verbose = False)

    # Drawing on the Horizontal image
    print("Drawing startup screen")
    window = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(window)
    draw.text((10, 10), todaysDate(), font = font24bolditalic, fill = 0)

    qrmain = pyqrcode.create('http://bit.ly/2MRE5O1')
    qrmain.png('mainqr.png', scale=6) # generate and save a PNG (lol this is prob so jank)

    window.paste(Image.open('mainqr.png'), (600, 282))

    if maintenanceData.iloc[0]['Birthday'] == '' or maintenanceData.iloc[0]['Birthday'] == None:
        print("it is no one's birthday today")

        if maintenanceData.iloc[0]['Holiday'] == '' or maintenanceData.iloc[0]['Holiday'] == None:
            print("it is not a holiday today")
        elif (maintenanceData.iloc[0]['Holiday'] != None) or (maintenanceData.iloc[0]['Holiday'] != ""):
            if(maintenanceData.iloc[0]['Holiday'] == "Christmas Eve") or (maintenanceData.iloc[0]['Holiday'] == "Christmas"):
                christmastree = Image.open(os.path.join(picdir, 'christmastree.png'))
                snowflake = Image.open(os.path.join(picdir, 'snowflake.png'))
                window.paste(snowflake, (10, 50))
                window.paste(christmastree, (34, 50))
                holidayText = "Merry " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 52), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(christmastree, ((holidayTextLength[0] + 69), 50))
                window.paste(snowflake, ((holidayTextLength[0] + 93), 50))

            elif(maintenanceData.iloc[0]['Holiday'] == "Fourth of July") or (maintenanceData.iloc[0]['Holiday'] == "4th of July") or (maintenanceData.iloc[0]['Holiday'] == "Independence Day"):
                usaflag = Image.open(os.path.join(picdir, 'usaflag.png'))
                usaoutline = Image.open(os.path.join(picdir, 'usaoutline.png'))
                window.paste(usaoutline, (10, 50))
                window.paste(usaflag, (34, 50))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 52), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(usaflag, ((holidayTextLength[0] + 69), 50))
                window.paste(usaoutline, ((holidayTextLength[0] + 93), 50))
            elif(maintenanceData.iloc[0]['Holiday'] == "Thanksgiving"):
                leaves = Image.open(os.path.join(picdir, 'leaves.png'))
                #usaoutline = Image.open(os.path.join(picdir, 'usaoutline.png'))
                window.paste(leaves, (10, 50))
                window.paste(leaves, (34, 50))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 52), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(leaves, ((holidayTextLength[0] + 69), 50))
                window.paste(leaves, ((holidayTextLength[0] + 93), 50))
            elif(maintenanceData.iloc[0]['Holiday'] == "Easter"):
                eastereggs = Image.open(os.path.join(picdir, 'eastereggs.png'))
                bunny = Image.open(os.path.join(picdir, 'bunny.png'))
                window.paste(eastereggs, (10, 50))
                window.paste(bunny, (34, 50))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 52), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(eastereggs, ((holidayTextLength[0] + 69), 50))
                window.paste(bunny, ((holidayTextLength[0] + 93), 50))
            elif(maintenanceData.iloc[0]['Holiday'] == "Mother's Day"):
                partybackward = Image.open(os.path.join(picdir, '003-partyBackward.png'))
                partyforward = Image.open(os.path.join(picdir, '003-partyForward.png'))
                window.paste(partybackward, (10, 50))
                window.paste(partybackward, (34, 50))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 52), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(partyforward, ((holidayTextLength[0] + 69), 50))
                window.paste(partyforward, ((holidayTextLength[0] + 93), 50))
            elif(maintenanceData.iloc[0]['Holiday'] == "Father's Day"):
                partybackward = Image.open(os.path.join(picdir, '003-partyBackward.png'))
                partyforward = Image.open(os.path.join(picdir, '003-partyForward.png'))
                window.paste(partybackward, (10, 50))
                window.paste(partybackward, (34, 50))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 52), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(partyforward, ((holidayTextLength[0] + 69), 50))
                window.paste(partyforward, ((holidayTextLength[0] + 93), 50))
            elif(maintenanceData.iloc[0]['Holiday'] == "Halloween"):
                spiderweb = Image.open(os.path.join(picdir, 'spiderweb.png'))
                jackolantern = Image.open(os.path.join(picdir, 'jackolantern.png'))
                window.paste(jackolantern, (10, 50))
                window.paste(spiderweb, (34, 50))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 52), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(spiderweb, ((holidayTextLength[0] + 69), 50))
                window.paste(jackolantern, ((holidayTextLength[0] + 93), 50))
            elif(maintenanceData.iloc[0]['Holiday'] == "Valentine's Day"):
                heart1 = Image.open(os.path.join(picdir, 'heart1.png'))
                heart2 = Image.open(os.path.join(picdir, 'heart2.png'))
                window.paste(heart1, (10, 50))
                window.paste(heart2, (34, 50))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 52), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(heart2, ((holidayTextLength[0] + 69), 50))
                window.paste(heart1, ((holidayTextLength[0] + 93), 50))
            elif(maintenanceData.iloc[0]['Holiday'] == "St. Patrick's Day"):
                spiderweb = Image.open(os.path.join(picdir, 'spiderweb.png'))
                jackolantern = Image.open(os.path.join(picdir, 'jackolantern.png'))
                window.paste(jackolantern, (10, 50))
                window.paste(spiderweb, (34, 50))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 52), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(spiderweb, ((holidayTextLength[0] + 69), 50))
                window.paste(jackolantern, ((holidayTextLength[0] + 93), 50))
            elif(maintenanceData.iloc[0]['Holiday'] == "New Year") or (maintenanceData.iloc[0]['Holiday'] == "New Year's Eve"):
                fireworks = Image.open(os.path.join(picdir, 'fireworks.png'))
                partyBackward = Image.open(os.path.join(picdir, '003-partyBackward.png'))
                partyForward = Image.open(os.path.join(picdir, '003-partyForward.png'))
                window.paste(partyBackward, (10, 50))
                window.paste(fireworks, (34, 50))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 52), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(fireworks, ((holidayTextLength[0] + 69), 50))
                window.paste(partyForward, ((holidayTextLength[0] + 93), 50))
            elif(maintenanceData.iloc[0]['Holiday'] == "Labor Day"):
                partyBackward = Image.open(os.path.join(picdir, '003-partyBackward.png'))
                partyForward = Image.open(os.path.join(picdir, '003-partyForward.png'))
                window.paste(partyBackward, (10, 50))
                window.paste(partyBackward, (34, 50))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 52), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(partyForward, ((holidayTextLength[0] + 69), 50))
                window.paste(partyForward, ((holidayTextLength[0] + 93), 50))
            elif(maintenanceData.iloc[0]['Holiday'] == "MLK Jr. Day"):
                partyBackward = Image.open(os.path.join(picdir, '003-partyBackward.png'))
                partyForward = Image.open(os.path.join(picdir, '003-partyForward.png'))
                window.paste(partyBackward, (10, 50))
                window.paste(partyBackward, (34, 50))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 52), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(partyForward, ((holidayTextLength[0] + 69), 50))
                window.paste(partyForward, ((holidayTextLength[0] + 93), 50))
            elif(maintenanceData.iloc[0]['Holiday'] == "April Fools' Day"):
                smiley = Image.open(os.path.join(picdir, 'smiley.png'))
                window.paste(smiley, (10, 50))
                window.paste(smiley, (34, 50))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 52), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(smiley, ((holidayTextLength[0] + 69), 50))
                window.paste(smiley, ((holidayTextLength[0] + 93), 50))
            elif(maintenanceData.iloc[0]['Holiday'] == "Earth Day"):
                earth = Image.open(os.path.join(picdir, 'earth.png'))
                window.paste(earth, (10, 50))
                window.paste(earth, (34, 50))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 52), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(earth, ((holidayTextLength[0] + 69), 50))
                window.paste(earth, ((holidayTextLength[0] + 93), 50))
            elif(maintenanceData.iloc[0]['Holiday'] == "Cinco de Mayo"):
                partyBackward = Image.open(os.path.join(picdir, '003-partyBackward.png'))
                partyForward = Image.open(os.path.join(picdir, '003-partyForward.png'))
                window.paste(partyBackward, (10, 50))
                window.paste(partyBackward, (34, 50))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 52), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(partyForward, ((holidayTextLength[0] + 69), 50))
                window.paste(partyForward, ((holidayTextLength[0] + 93), 50))
            elif(maintenanceData.iloc[0]['Holiday'] == "Women's Equality Day"):
                partyBackward = Image.open(os.path.join(picdir, '003-partyBackward.png'))
                partyForward = Image.open(os.path.join(picdir, '003-partyForward.png'))
                equal = Image.open(os.path.join(picdir, 'equal.png'))
                window.paste(partyBackward, (10, 50))
                window.paste(equal, (34, 50))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 52), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(equal, ((holidayTextLength[0] + 69), 50))
                window.paste(partyForward, ((holidayTextLength[0] + 93), 50))
            elif(maintenanceData.iloc[0]['Holiday'] == "Election Day"):
                usaflag = Image.open(os.path.join(picdir, 'usaflag.png'))
                vote = Image.open(os.path.join(picdir, 'vote.png'))
                equal = Image.open(os.path.join(picdir, 'equal.png'))
                window.paste(usaflag, (10, 54))
                window.paste(vote, (34, 50))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 52), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(vote, ((holidayTextLength[0] + 69), 50))
                window.paste(usaflag, ((holidayTextLength[0] + 93), 54))
            else:
                partyBackward = Image.open(os.path.join(picdir, '003-partyBackward.png'))
                partyForward = Image.open(os.path.join(picdir, '003-partyForward.png'))
                window.paste(partyBackward, (10, 50))
                window.paste(partyBackward, (34, 50))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 52), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(partyForward, ((holidayTextLength[0] + 69), 50))
                window.paste(partyForward, ((holidayTextLength[0] + 93), 50))

    elif (maintenanceData.iloc[0]['Birthday'] != None) or (maintenanceData.iloc[0]['Birthday'] != ""):
        celebForward = Image.open(os.path.join(picdir, '003-partyForward.png'))
        celebBackward = Image.open(os.path.join(picdir, '003-partyBackward.png'))
        balloon = Image.open(os.path.join(picdir, '002-balloon.png'))
        window.paste(balloon, (33, 50))
        window.paste(celebBackward, (10, 50))
        birthdayText = "Happy Birthday " + maintenanceData.iloc[0]['Birthday'] + "! "
        draw.text((63, 52), birthdayText, font = font18bold, fill = 0)
        birthdayTextLength = draw.textsize(birthdayText, font = font18bold)

        window.paste(balloon, ((birthdayTextLength[0] + 68), 50))
        window.paste(celebForward, ((birthdayTextLength[0] + 92), 50))

        if maintenanceData.iloc[0]['Holiday'] == '' or maintenanceData.iloc[0]['Holiday'] == None:
            print("it is not a holiday today")
        elif (maintenanceData.iloc[0]['Holiday'] != None) or (maintenanceData.iloc[0]['Holiday'] != ""):
            if(maintenanceData.iloc[0]['Holiday'] == "Christmas Eve") or (maintenanceData.iloc[0]['Holiday'] == "Christmas"):
                christmastree = Image.open(os.path.join(picdir, 'christmastree.png'))
                snowflake = Image.open(os.path.join(picdir, 'snowflake.png'))
                window.paste(snowflake, (10, 90))
                window.paste(christmastree, (34, 90))
                holidayText = "Merry " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 92), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(christmastree, ((holidayTextLength[0] + 69), 90))
                window.paste(snowflake, ((holidayTextLength[0] + 93), 90))

            elif(maintenanceData.iloc[0]['Holiday'] == "Fourth of July") or (maintenanceData.iloc[0]['Holiday'] == "4th of July") or (maintenanceData.iloc[0]['Holiday'] == "Independence Day"):
                usaflag = Image.open(os.path.join(picdir, 'usaflag.png'))
                usaoutline = Image.open(os.path.join(picdir, 'usaoutline.png'))
                window.paste(usaoutline, (10, 90))
                window.paste(usaflag, (34, 94))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 92), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(usaflag, ((holidayTextLength[0] + 69), 94))
                window.paste(usaoutline, ((holidayTextLength[0] + 93), 90))
            elif(maintenanceData.iloc[0]['Holiday'] == "Thanksgiving"):
                leaves = Image.open(os.path.join(picdir, 'leaves.png'))
                #usaoutline = Image.open(os.path.join(picdir, 'usaoutline.png'))
                window.paste(leaves, (10, 90))
                window.paste(leaves, (34, 90))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 92), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(leaves, ((holidayTextLength[0] + 69), 90))
                window.paste(leaves, ((holidayTextLength[0] + 93), 90))
            elif(maintenanceData.iloc[0]['Holiday'] == "Easter"):
                eastereggs = Image.open(os.path.join(picdir, 'eastereggs.png'))
                bunny = Image.open(os.path.join(picdir, 'bunny.png'))
                window.paste(eastereggs, (10, 90))
                window.paste(bunny, (34, 90))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 92), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(eastereggs, ((holidayTextLength[0] + 69), 90))
                window.paste(bunny, ((holidayTextLength[0] + 93), 90))
            elif(maintenanceData.iloc[0]['Holiday'] == "Mother's Day"):
                partybackward = Image.open(os.path.join(picdir, '003-partyBackward.png'))
                partyforward = Image.open(os.path.join(picdir, '003-partyForward.png'))
                window.paste(partybackward, (10, 90))
                window.paste(partybackward, (34, 90))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 92), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(partyforward, ((holidayTextLength[0] + 69), 90))
                window.paste(partyforward, ((holidayTextLength[0] + 93), 90))
            elif(maintenanceData.iloc[0]['Holiday'] == "Father's Day"):
                partybackward = Image.open(os.path.join(picdir, '003-partyBackward.png'))
                partyforward = Image.open(os.path.join(picdir, '003-partyForward.png'))
                window.paste(partybackward, (10, 90))
                window.paste(partybackward, (34, 90))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 92), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(partyforward, ((holidayTextLength[0] + 69), 90))
                window.paste(partyforward, ((holidayTextLength[0] + 93), 90))
            elif(maintenanceData.iloc[0]['Holiday'] == "Halloween"):
                spiderweb = Image.open(os.path.join(picdir, 'spiderweb.png'))
                jackolantern = Image.open(os.path.join(picdir, 'jackolantern.png'))
                window.paste(jackolantern, (10, 90))
                window.paste(spiderweb, (34, 90))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 92), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(spiderweb, ((holidayTextLength[0] + 69), 90))
                window.paste(jackolantern, ((holidayTextLength[0] + 93), 90))
            elif(maintenanceData.iloc[0]['Holiday'] == "Valentine's Day"):
                heart1 = Image.open(os.path.join(picdir, 'heart1.png'))
                heart2 = Image.open(os.path.join(picdir, 'heart2.png'))
                window.paste(heart1, (10, 90))
                window.paste(heart2, (34, 90))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 92), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(heart2, ((holidayTextLength[0] + 69), 90))
                window.paste(heart1, ((holidayTextLength[0] + 93), 90))
            elif(maintenanceData.iloc[0]['Holiday'] == "St. Patrick's Day"):
                spiderweb = Image.open(os.path.join(picdir, 'spiderweb.png'))
                jackolantern = Image.open(os.path.join(picdir, 'jackolantern.png'))
                window.paste(jackolantern, (10, 90))
                window.paste(spiderweb, (34, 90))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 92), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(spiderweb, ((holidayTextLength[0] + 69), 90))
                window.paste(jackolantern, ((holidayTextLength[0] + 93), 90))
            elif(maintenanceData.iloc[0]['Holiday'] == "New Year") or (maintenanceData.iloc[0]['Holiday'] == "New Year's Eve"):
                fireworks = Image.open(os.path.join(picdir, 'fireworks.png'))
                partyBackward = Image.open(os.path.join(picdir, '003-partyBackward.png'))
                partyForward = Image.open(os.path.join(picdir, '003-partyForward.png'))
                window.paste(partyBackward, (10, 90))
                window.paste(fireworks, (34, 90))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 92), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(fireworks, ((holidayTextLength[0] + 69), 90))
                window.paste(partyForward, ((holidayTextLength[0] + 93), 90))
            elif(maintenanceData.iloc[0]['Holiday'] == "Labor Day"):
                partyBackward = Image.open(os.path.join(picdir, '003-partyBackward.png'))
                partyForward = Image.open(os.path.join(picdir, '003-partyForward.png'))
                window.paste(partyBackward, (10, 90))
                window.paste(partyBackward, (34, 90))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 92), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(partyForward, ((holidayTextLength[0] + 69), 90))
                window.paste(partyForward, ((holidayTextLength[0] + 93), 90))
            elif(maintenanceData.iloc[0]['Holiday'] == "MLK Jr. Day"):
                partyBackward = Image.open(os.path.join(picdir, '003-partyBackward.png'))
                partyForward = Image.open(os.path.join(picdir, '003-partyForward.png'))
                window.paste(partyBackward, (10, 90))
                window.paste(partyBackward, (34, 90))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 92), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(partyForward, ((holidayTextLength[0] + 69), 90))
                window.paste(partyForward, ((holidayTextLength[0] + 93), 90))
            elif(maintenanceData.iloc[0]['Holiday'] == "April Fools' Day"):
                smiley = Image.open(os.path.join(picdir, 'smiley.png'))
                window.paste(smiley, (10, 90))
                window.paste(smiley, (34, 90))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 92), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(smiley, ((holidayTextLength[0] + 69), 90))
                window.paste(smiley, ((holidayTextLength[0] + 93), 90))
            elif(maintenanceData.iloc[0]['Holiday'] == "Earth Day"):
                earth = Image.open(os.path.join(picdir, 'earth.png'))
                window.paste(earth, (10, 90))
                window.paste(earth, (34, 90))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 92), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(earth, ((holidayTextLength[0] + 69), 90))
                window.paste(earth, ((holidayTextLength[0] + 93), 90))
            elif(maintenanceData.iloc[0]['Holiday'] == "Cinco de Mayo"):
                partyBackward = Image.open(os.path.join(picdir, '003-partyBackward.png'))
                partyForward = Image.open(os.path.join(picdir, '003-partyForward.png'))
                window.paste(partyBackward, (10, 90))
                window.paste(partyBackward, (34, 90))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 92), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(partyForward, ((holidayTextLength[0] + 69), 90))
                window.paste(partyForward, ((holidayTextLength[0] + 93), 90))
            elif(maintenanceData.iloc[0]['Holiday'] == "Women's Equality Day"):
                partyBackward = Image.open(os.path.join(picdir, '003-partyBackward.png'))
                partyForward = Image.open(os.path.join(picdir, '003-partyForward.png'))
                equal = Image.open(os.path.join(picdir, 'equal.png'))
                window.paste(partyBackward, (10, 90))
                window.paste(equal, (34, 90))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 92), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(equal, ((holidayTextLength[0] + 69), 90))
                window.paste(partyForward, ((holidayTextLength[0] + 93), 90))
            elif(maintenanceData.iloc[0]['Holiday'] == "Election Day"):
                usaflag = Image.open(os.path.join(picdir, 'usaflag.png'))
                vote = Image.open(os.path.join(picdir, 'vote.png'))
                equal = Image.open(os.path.join(picdir, 'equal.png'))
                window.paste(usaflag, (10, 94))
                window.paste(vote, (34, 90))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 92), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(vote, ((holidayTextLength[0] + 69), 90))
                window.paste(usaflag, ((holidayTextLength[0] + 93), 94))
            else:
                partyBackward = Image.open(os.path.join(picdir, '003-partyBackward.png'))
                partyForward = Image.open(os.path.join(picdir, '003-partyForward.png'))
                window.paste(partyBackward, (10, 90))
                window.paste(partyBackward, (34, 90))
                holidayText = "Happy " + maintenanceData.iloc[0]['Holiday'] + "! "
                draw.text((64, 92), holidayText, font = font18bold, fill = 0)
                holidayTextLength = draw.textsize(holidayText, font = font18bold)

                window.paste(partyForward, ((holidayTextLength[0] + 69), 90))
                window.paste(partyForward, ((holidayTextLength[0] + 93), 90))
    
    draw.rectangle([(0,136), (200, 169)], outline=0)
    draw.text((10, 140), 'MAINTENANCE', font = font24bold, fill = 0)
    draw.rectangle([(0,204), (40,239)], fill=0)
    draw.line([(40,169),(40,204)], fill = 0)

    prevShift = maintenanceData.iloc[1]['Shift']
    if prevShift == "EM":
        draw.text((7, 177), prevShift, font = font18bold, fill=0)
    else:
        draw.text((5, 177), prevShift, font = font18bold, fill=0)
    currentShift = maintenanceData.iloc[0]['Shift']
    if currentShift == "EM":
        draw.text((7, 212), currentShift, font = font18bold, fill=1)
    else:
        draw.text((5, 212), currentShift, font = font18bold, fill=1)
    draw.rectangle([(0,169), (350, 239)], outline=0)
    draw.line([(0,204),(350,204)], fill = 0)

    prevShiftMaint = maintenanceData.iloc[1]['MaintenanceDuty']
    draw.text((50, 180), prevShiftMaint, font = font14, fill=0)
    currentShiftMaint = maintenanceData.iloc[0]['MaintenanceDuty']
    draw.text((50, 215), currentShiftMaint, font = font14, fill=0)
    print(maintenanceData)


    draw.rectangle([(0,273), (140, 306)], outline=0)
    draw.text((10, 277), 'LOGBOOK', font = font24bold, fill = 0)
    draw.rectangle([(0,306),(615,epd.height-1)], outline = 0)
    
    print("Getting shift data...")
    # Set n = to the number of shifts you want to retrieve (from the current shift, inclusive)
    shiftData = getShiftData(n=4, verbose=False)
    print(shiftData)
    draw.rectangle([(0,306), (615,340)], fill=0)
    draw.text((10, 314), 'DATE', font = font18bold, fill=1)
    draw.text((80, 314), 'TIME', font = font18bold, fill=1)
    draw.text((145, 314), 'RELIEF CREW', font = font18bold, fill=1)
    draw.text((385, 314), 'PREVIOUS CREW', font = font18bold, fill=1)

    # Display latest entry
    draw.text((7, 349), shiftData.iloc[0]['SHIFT_DATE'], font = font14, fill=0)
    draw.text((85, 349), shiftData.iloc[0]['START_TIME'], font = font14, fill=0)
    draw.text((142, 349), shiftData.iloc[0]['RELIEF'], font = font14, fill=0)
    draw.text((382, 349), shiftData.iloc[0]['PREVIOUS_CREW'], font = font14, fill=0)

    draw.line([(0,375),(615,375)], fill = 0)
    draw.text((7, 386), shiftData.iloc[1]['SHIFT_DATE'], font = font14, fill=0)
    draw.text((85, 386), shiftData.iloc[1]['START_TIME'], font = font14, fill=0)
    draw.text((142, 386), shiftData.iloc[1]['RELIEF'], font = font14, fill=0)
    draw.text((382, 386), shiftData.iloc[1]['PREVIOUS_CREW'], font = font14, fill=0)

    draw.line([(0,410),(615,410)], fill = 0)
    draw.text((7, 421), shiftData.iloc[2]['SHIFT_DATE'], font = font14, fill=0)
    draw.text((85, 421), shiftData.iloc[2]['START_TIME'], font = font14, fill=0)
    draw.text((142, 421), shiftData.iloc[2]['RELIEF'], font = font14, fill=0)
    draw.text((382, 421), shiftData.iloc[2]['PREVIOUS_CREW'], font = font14, fill=0)

    draw.line([(0,445),(615,445)], fill = 0)
    draw.text((7, 456), shiftData.iloc[3]['SHIFT_DATE'], font = font14, fill=0)
    draw.text((85, 456), shiftData.iloc[3]['START_TIME'], font = font14, fill=0)
    draw.text((142, 456), shiftData.iloc[3]['RELIEF'], font = font14, fill=0)
    draw.text((382, 456), shiftData.iloc[3]['PREVIOUS_CREW'], font = font14, fill=0)

    draw.line([(70,315),(70,epd.height)], fill = 0)
    draw.line([(135,315),(135,epd.height)], fill = 0)
    draw.line([(375,315),(375,epd.height)], fill = 0)

    ################ Announcements

    announcements = getAnnouncements()    
    numberOfAnnouncements = len(announcements.index)

    print("Number of announcements: " + str(numberOfAnnouncements)) 
    print(announcements)

    wrappedAnnouncement = ''
    wrappedAnnouncement1 = ''
    wrappedAnnouncement2 = ''

    if numberOfAnnouncements == 1:
        print(announcements.iloc[0]['Announcement Message'])

        requester1 = announcements.iloc[0]['Requesting Entity']
        heading1length = draw.textsize(requester1, font = font18bolditalic)

        draw.rectangle([(epd.width/2, 5), (((epd.width/2) + (heading1length[0] + 15)), (heading1length[1] + 14))], fill=0)
        draw.text(((epd.width/2)+8, 10), requester1, font = font18bolditalic, fill = 1)

        if (announcements.iloc[0]['Website Link'] == "") or (announcements.iloc[0]['Website Link'] == None):
            wrapper = textwrap.TextWrapper(width = 45)
            wrappedAnnouncement = wrapper.fill(text=announcements.iloc[0]['Announcement Message'])
            wrappedAnnouncement.replace('\n', ' \n ')
            print(wrappedAnnouncement)
            draw.text(((epd.width/2)+5, 50), wrappedAnnouncement, font = font18, fill = 0)

        elif (announcements.iloc[0]['Website Link'] != "") or (announcements.iloc[0]['Website Link'] != None):
            long_url = [announcements.iloc[0]['Website Link']]
            short_url = shortener.shorten_urls(long_url)
            print(short_url[0])
            qr = pyqrcode.create(short_url[0])
            qr.png('qr1.png', scale=3) # generate and save a PNG (lol this is prob so jank)

            window.paste(Image.open('qr1.png'), ((epd.width-105), 35))

            wrapper = textwrap.TextWrapper(width = 35)
            wrappedAnnouncement = wrapper.fill(text=announcements.iloc[0]['Announcement Message'])
            wrappedAnnouncement.replace('\n', ' \n ')
            print(wrappedAnnouncement)

        draw.rectangle([((epd.width/2)-5,0), (epd.width-1,138)], outline=0)
        draw.text(((epd.width/2)+5, 50), wrappedAnnouncement, font = font18, fill = 0)
    elif numberOfAnnouncements >= 2:
        print(announcements.iloc[0]['Announcement Message'])
        print(announcements.iloc[1]['Announcement Message'])

        websiteCheck = (announcements['Website Link'] != None) & (announcements['Website Link'] != "")

        if (len(announcements[websiteCheck].index) == 1):
            print(announcements[websiteCheck].iloc[0]['Website Link'])

            requester1 = announcements.iloc[0]['Requesting Entity']
            heading1length = draw.textsize(requester1, font = font18bolditalic)

            draw.rectangle([(epd.width/2, 5), (((epd.width/2) + (heading1length[0] + 15)), (heading1length[1] + 14))], fill=0)
            draw.text(((epd.width/2)+8, 10), requester1, font = font18bolditalic, fill = 1)

            if (announcements.iloc[0]['Website Link'] == "") or (announcements.iloc[0]['Website Link'] == None):
                wrapper = textwrap.TextWrapper(width = 45)
                wrappedAnnouncement1 = wrapper.fill(text=announcements.iloc[0]['Announcement Message'])
                wrappedAnnouncement1.replace('\n', ' \n ')
                print(wrappedAnnouncement1)

            elif (announcements.iloc[0]['Website Link'] != "") or (announcements.iloc[0]['Website Link'] != None):

                wrapper = textwrap.TextWrapper(width = 35)
                wrappedAnnouncement1 = wrapper.fill(text=announcements.iloc[0]['Announcement Message'])
                wrappedAnnouncement1.replace('\n', ' \n ')
                print(wrappedAnnouncement1)

                long_url = [announcements.iloc[0]['Website Link']]
                short_url = shortener.shorten_urls(long_url)
                print(short_url[0])
                qr = pyqrcode.create(short_url[0])
                qr.png('qr1.png', scale=3) # generate and save a PNG (lol this is prob so jank)
                window.paste(Image.open('qr1.png'), ((epd.width-105), 35))

            draw.rectangle([((epd.width/2)-5,0), (epd.width-1,138)], outline=0)
            draw.text(((epd.width/2)+5, 50), wrappedAnnouncement1, font = font18, fill = 0)

            requester2 = announcements.iloc[1]['Requesting Entity']
            heading2length = draw.textsize(requester2, font = font18bolditalic)
            draw.rectangle([(epd.width/2, 148), (((epd.width/2) + (heading2length[0] + 17)), (heading2length[1] + 157))], fill=0)
            draw.text(((epd.width/2)+8, 153), requester2, font = font18bolditalic, fill = 1)

            if (announcements.iloc[1]['Website Link'] == "") or (announcements.iloc[1]['Website Link'] == None):
                wrapper = textwrap.TextWrapper(width = 45)
                wrappedAnnouncement2 = wrapper.fill(text=announcements.iloc[1]['Announcement Message'])
                wrappedAnnouncement2.replace('\n', ' \n ')
                print(wrappedAnnouncement2)

            elif (announcements.iloc[1]['Website Link'] != "") or (announcements.iloc[1]['Website Link'] != None):
                wrapper = textwrap.TextWrapper(width = 35)
                wrappedAnnouncement2 = wrapper.fill(text=announcements.iloc[1]['Announcement Message'])
                wrappedAnnouncement2.replace('\n', ' \n ')
                print(wrappedAnnouncement2)

                long_url = [announcements.iloc[1]['Website Link']]
                short_url = shortener.shorten_urls(long_url)
                print(short_url[0])

                qr2 = pyqrcode.create(short_url[0])
                qr2.png('qr2.png', scale=3) # generate and save a PNG (lol this is prob so jank)

                window.paste(Image.open('qr2.png'), ((epd.width-105), 173))

            draw.rectangle([((epd.width/2)-5,143), (epd.width-1,276)], outline=0)
            draw.text(((epd.width/2)+5, 185), wrappedAnnouncement2, font = font18, fill = 0)

        elif(len(announcements[websiteCheck].index) == 2):
            print(announcements[websiteCheck].iloc[0]['Website Link'])
            print(announcements[websiteCheck].iloc[1]['Website Link'])

            long_urls = [announcements[websiteCheck].iloc[0]['Website Link'], announcements[websiteCheck].iloc[1]['Website Link']]
            short_urls = shortener.shorten_urls(long_urls)

            ### Announcement 1 with Link ###

            requester1 = announcements.iloc[0]['Requesting Entity']
            heading1length = draw.textsize(requester1, font = font18bolditalic)
            draw.rectangle([(epd.width/2, 5), (((epd.width/2) + (heading1length[0] + 15)), (heading1length[1] + 14))], fill=0)
            draw.text(((epd.width/2)+8, 10), requester1, font = font18bolditalic, fill = 1)

            wrapper = textwrap.TextWrapper(width = 35)
            wrappedAnnouncement1 = wrapper.fill(text=announcements.iloc[0]['Announcement Message'])
            wrappedAnnouncement1.replace('\n', ' \n ')
            print(wrappedAnnouncement1)

            qr1 = pyqrcode.create(short_urls[0])
            qr1.png('qr1.png', scale=3) # generate and save a PNG (lol this is prob so jank)

            window.paste(Image.open('qr1.png'), ((epd.width-105), 35))

            draw.rectangle([((epd.width/2)-5,0), (epd.width-1,138)], outline=0)
            draw.text(((epd.width/2)+5, 45), wrappedAnnouncement1, font = font18, fill = 0)

            ### Announcement 2 with Link ###

            requester2 = announcements.iloc[1]['Requesting Entity']
            heading2length = draw.textsize(requester2, font = font18bolditalic)
            draw.rectangle([(epd.width/2, 148), (((epd.width/2) + (heading2length[0] + 17)), (heading2length[1] + 157))], fill=0)
            draw.text(((epd.width/2)+8, 153), requester2, font = font18bolditalic, fill = 1)

            wrapper = textwrap.TextWrapper(width = 35)
            wrappedAnnouncement2 = wrapper.fill(text=announcements.iloc[1]['Announcement Message'])
            wrappedAnnouncement2.replace('\n', ' \n ')
            print(wrappedAnnouncement2)

            qr2 = pyqrcode.create(short_urls[1])
            qr2.png('qr2.png', scale=3) # generate and save a PNG (lol this is prob so jank)

            window.paste(Image.open('qr2.png'), ((epd.width-105), 173))

            draw.rectangle([((epd.width/2)-5,143), (epd.width-1,276)], outline=0)
            draw.text(((epd.width/2)+5, 185), wrappedAnnouncement2, font = font18, fill = 0)

        else:
            requester1 = announcements.iloc[0]['Requesting Entity']
            heading1length = draw.textsize(requester1, font = font18bolditalic)

            draw.rectangle([(epd.width/2, 5), (((epd.width/2) + (heading1length[0] + 15)), (heading1length[1] + 14))], fill=0)
            draw.text(((epd.width/2)+8, 10), requester1, font = font18bolditalic, fill = 1)

            wrapper = textwrap.TextWrapper(width = 45)
            wrappedAnnouncement1 = wrapper.fill(text=announcements.iloc[0]['Announcement Message'])
            wrappedAnnouncement1.replace('\n', ' \n ')
            print(wrappedAnnouncement1)

            requester2 = announcements.iloc[1]['Requesting Entity']
            heading2length = draw.textsize(requester2, font = font18bolditalic)
            draw.rectangle([(epd.width/2, 148), (((epd.width/2) + (heading2length[0] + 17)), (heading2length[1] + 157))], fill=0)
            draw.text(((epd.width/2)+8, 153), requester2, font = font18bolditalic, fill = 1)

            wrapper = textwrap.TextWrapper(width = 45)
            wrappedAnnouncement2 = wrapper.fill(text=announcements.iloc[1]['Announcement Message'])
            wrappedAnnouncement2.replace('\n', ' \n ')
            print(wrappedAnnouncement2)

            draw.text(((epd.width/2)+5, 50), wrappedAnnouncement1, font = font18, fill = 0)
            draw.text(((epd.width/2)+5, 185), wrappedAnnouncement2, font = font18, fill = 0)


    #######################

    lastUpdate = 'Last updated: ' + getCurrentDateTime() + " "
    updateLength = draw.textsize(lastUpdate, font = font12)

    draw.text(((epd.width - updateLength[0]), 285), lastUpdate, font = font12, fill = 0)

    epd.Clear()

    epd.display(epd.getbuffer(window))
    time.sleep(2)

    print("Goto Sleep...")
    epd.sleep()
    time.sleep(3)
        
    epd.Dev_exit()

# except Exception as e:
#     print("####ERROR####\n" + traceback.format_exc())
#     draw.rectangle([(160,254), (750, 290)], fill=0)
#     draw.text((170, 260), 'AN ERROR OCCURRED - Assume data unreliable', font = font24bold, fill = 1)
#     epd.display(epd.getbuffer(window))
#     time.sleep(2)
#     epd.Dev_exit()

except Exception as e:
    print("####ERROR####\n" + traceback.format_exc())
    errorWindow = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    drawError = ImageDraw.Draw(errorWindow)
    drawError.rectangle([(0,0), (300, 44)], fill=0)
    drawError.text((10, 10), 'AN ERROR OCCURRED', font = font24bold, fill = 1)

    # Get error text and print it
    wrapper = textwrap.TextWrapper(width = 100)
    wrappedError = wrapper.fill(text=traceback.format_exc())
    wrappedError.replace('\n', ' \n ')
    drawError.text((10,58), wrappedError, font=font14)
    errorWindow.paste(Image.open('mainqr.png'), (600, 282))
    epd.display(epd.getbuffer(errorWindow))
    time.sleep(2)
    epd.Dev_exit()

    
# except KeyboardInterrupt:    
#     logging.info("ctrl + c:")
#     epd7in5_V2.epdconfig.module_exit()
#     exit()





