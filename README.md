# Read [ITIS](https://www.itis.si/) and gather Unique Slovene names

## Description

Read [Slovene phone book](https://www.itis.si/), insert cities name and create unique names.txt file with unique Slovene names seperated by new line

## Requirements

1. Python 3.10. or higher
2. Chrome browser with ChromeDriver to use with selenium browser automation tool (you need to find appropriate ChromeDriver for your Chrome browser)
3. Install requirements with pip install requirements.txt 

## How do I use it?

1. Script uses Selenium driver to control Chrome web browser, correct version of selenium driver for your Chrome web browser is required. 
2. Create a SeleniumDrivers folder and download latest driver from [ChromeDriver](https://chromedriver.chromium.org/downloads)
3. Required Python packages are documented in requirements.txt, see [instructions how to install packages](https://learn.microsoft.com/en-us/visualstudio/python/managing-required-packages-with-requirements-txt?view=vs-2022)
4. 

## Example

Example of names list can be found in 
 - [Unique names seperated by new line](https://github.com/Baselj/UniqueSloveneNamesWebCrawler/blob/main/name.txt)
 - [Unique names seperated by ;](https://github.com/Baselj/UniqueSloveneNamesWebCrawler/blob/main/namecsv.txt)
 - [All names and surnames](https://github.com/Baselj/UniqueSloveneNamesWebCrawler/blob/main/nameSurname.txt)

## Features

Script uses automated control of Chrome browser, it's designed for long term operation (24 hour of scraping)
 - It goes to Slovene phonebook,
 - copies the name of the city from cities.txt
 - copies it into the form and clicks search
 - scrapes through all the pages by name
 - stores the names in three files
    - names.txt : unique Slovene names seperated by new line
    - namecsv.txt : unique Slovene names seperated by ;
    - nameSurname.txt : all scraped Slovene names and surnames seperated by new line
