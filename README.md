# Read [ITIS](https://www.itis.si/)

## Description

Read AJPES website, click through the public auctions, download and merge PDF public auction files and send it in an e-mail.

## Requirements

1. Python 3.10. or higher
2. Chrome browser with ChromeDriver to use with selenium browser automation tool
3. Install requirements with pip install requirements.txt 

## How do I use it?

1. Script uses Selenium driver to control Chrome web browser, correct version of selenium driver for your Chrome web browser is required. 
2. Create a SeleniumDrivers folder and download latest driver from [ChromeDriver](https://chromedriver.chromium.org/downloads)
3. Required Python packages are documented in requirements.txt, see [instructions how to install packages](https://learn.microsoft.com/en-us/visualstudio/python/managing-required-packages-with-requirements-txt?view=vs-2022)
4. Create [access credentials for gmail account](https://developers.google.com/workspace/guides/create-credentials) 
5. Configure config.ini with your credentials
    - mailUname (your gmail address), 
    - mailPwd (your gmail password) 
    - fromEmail (send from email address)
    - recipientEmail (recipient email list, divided by ;)

## Example

Example of merged pdf can be found in [DownloadFolder/send](https://github.com/Baselj/PythonAJPESWebCrawler/blob/main/DownloadFolder/send/2022-09-26AjpesDrazbe.pdf)

## Features

The script is designed to use automated control of Chrome browser. The process is as follows:
 - It goes to the original website, 
 - finds the selected element, 
 - clicks it, 
 - waits for page to load,
 - clicks the download link, 
 - waits for chrome to finish downloading, 
 - closes the newly opened window,
 - goes back to original website, 
 - and repeats the process.

Afterwards it merges all the downloaded PDFs and sends the via e-mail with description of downloaded files in the body and merged PDF in the attachment.
