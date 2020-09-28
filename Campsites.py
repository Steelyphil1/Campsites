#You will need to create a campsites.txt file in the same folder of the python program.
#Additionally fill out the email information in the program below. I would create a crontab 
#job that runs this program every 30 minutes and emails you if a campsite becomes available.
#I still need to make it so it doesn't continuously email you about the same campsite. 
#If FOUND = TRUE AND CAMPSITE NOT IN LISTOFCAMSITESEMAILED THEN email

#Written by Steelyphil
#Last modified March 26 2018
#Scrapes Yosemite campgrounds and if a campsite is available, emails you.

#!/usr/bin/env python3

import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import bs4 as bs
import urllib.request
from urllib.request import Request, urlopen

urlUpperPrefix = 'https://www.recreation.gov/campsiteCalendar.do?page=matrix&calarvdate='
urlUpperPostfix = '&contractCode=NRSO&parkId=70925'
urlLowerPrefix = 'https://www.recreation.gov/campsiteCalendar.do?page=matrix&calarvdate='
urlLowerPostfix = '&contractCode=NRSO&parkId=70928'
urlNorthPrefix = 'https://www.recreation.gov/campsiteCalendar.do?page=matrix&calarvdate='
urlNorthPostfix = '&contractCode=NRSO&parkId=70927'
wantedDate = sys.argv[1]
searchDate = sys.argv[2]
finalUpperUrl = urlUpperPrefix + wantedDate + urlUpperPostfix
finalLowerUrl = urlLowerPrefix + wantedDate + urlLowerPostfix
finalNorthUrl = urlNorthPrefix + wantedDate + urlNorthPostfix


reqUpper = Request(finalUpperUrl, headers={'User-Agent': 'Mozilla/5.0'})
reqLower = Request(finalLowerUrl, headers={'User-Agent': 'Mozilla/5.0'})
reqNorth = Request(finalNorthUrl, headers={'User-Agent': 'Mozilla/5.0'})

webpageUpper = urlopen(reqUpper).read()
webpageLower = urlopen(reqLower).read()
webpageNorth = urlopen(reqNorth).read()

soupUpper = bs.BeautifulSoup(webpageUpper, 'lxml')
soupLower = bs.BeautifulSoup(webpageLower, 'lxml')
soupNorth = bs.BeautifulSoup(webpageNorth, 'lxml')

tdsall = []

#UpperPines
for tds in soupUpper.find_all('td', class_="status a"):
    # find every <td> tag thats available including the sub <a>
    tds_string = str(tds)
    tdsall.append(tds_string)
for tdssat in soupUpper.find_all('td', class_="status a sat"):
    # previous loop doesnt include sat or sun, retreiving them
    tdssat_string = str(tdssat)
    tdsall.append(tdssat_string)
for tdssun in soupUpper.find_all('td', class_="status a sun"):
    tdssun_string = str(tdssun)
    tdsall.append(tdssun_string)
#LowerPines
for tds in soupLower.find_all('td', class_="status a"):
    tds_string = str(tds)
    tdsall.append(tds_string)
for tdssat in soupLower.find_all('td', class_="status a sat"):
    tdssat_string = str(tdssat)
    tdsall.append(tdssat_string)
for tdssun in soupLower.find_all('td', class_="status a sun"):
    tdssun_string = str(tdssun)
    tdsall.append(tdssun_string)
#NorthPines
for tds in soupNorth.find_all('td', class_="status a"):
    tds_string = str(tds)
    tdsall.append(tds_string)
for tdssat in soupNorth.find_all('td', class_="status a sat"):
    tdssat_string = str(tdssat)
    tdsall.append(tdssat_string)
for tdssun in soupNorth.find_all('td', class_="status a sun"):
    tdssun_string = str(tdssun)
    tdsall.append(tdssun_string)

#Creating the Email

MY_ADDRESS = 'INSERT EMAIL ADDRESS HERE'
MY_PASSWORD = 'INSERT PASSWORD HERE'
DESTINATION_ADDRESS = 'INSERT DESTINATION ADDRESS HERE'

s = smtplib.SMTP(host='INSERT HOST SMTP HERE', port=INSERT HOST PORT HERE)
s.starttls()
s.login(MY_ADDRESS, MY_PASSWORD)

message = " "

msg = MIMEMultipart()
msg['From'] = MY_ADDRESS
msg['To'] = DESTINATION_ADDRESS
msg['Subject'] = "Campsite!"


#Writing all <td>'s with available status to file

fileout = open("campsites.txt", "a")
    
for avails in tdsall:
    str(avails)
    fileout.write(avails + "\n")

#Reading in <td>'s, and making a boolean true if a campsite is available

found = False
foundLine = " "
filein = open("campsites.txt", "r")

for line in filein:
    if searchDate in line:
        found = True
        foundLine = line
        
#Reseting the file

fileclear = open("campsites.txt", "w").close()

#Creating the message for the Email and sending it

campground = " "

if '70925' in foundLine:
    campground = "Upper Pines"
elif '70928' in foundLine:
    campground = "Lower Pines"
elif '70927' in foundLine:
    campground = "North Pines"
    

if found == True:
    message = "There is a campsite available in " + campground + "! Hurry!"
    msg.attach(MIMEText(message, 'plain'))
    s.send_message(msg)
