import flask
import requests
import os
import json
# from bs4 import BeautifulSoup
from selenium import webdriver

# These two imports were taken from p3 EECS485
# Note to self: need to look at docs
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime

app = flask.Flask(__name__)

@app.route("/", methods=["GET"])
def verification():
    print("Im in here")
    print(flask.request.args)

    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    """
    if flask.request.args.get("hub.mode") == "subscribe" and flask.request.args.get("hub.challenge"):
        if not flask.request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return flask.request.args["hub.challenge"], 200
    """


    # Get today's date
    current = str(datetime.datetime.now())
    print("CURRENT ",current)
    # print("Type ",type(current))
    current = current.split(" ")
    print(current)
    date = current[0]

    gameinfo = get_score(date)

    return "Hello World"

def get_score(date):
    """
    This wont work because the data is dynamially loaded with js
    # Trying to get mlb.com data
    r = requests.get("https://www.mlb.com/yankees/scores/2018-05-11")
    #print(r.content)
    soup = BeautifulSoup(r.content,"html.parser")
    """

    # Setting up headless browser to load the page
    # https://stackoverflow.com/questions/41059144/running-chromedriver-with-python-selenium-on-heroku

    options = Options()

    # This line is also for heroku
    options.binary_location = os.environ["GOOGLE_CHROME_PATH"]

    options.add_argument("--headless")
    # For local
    # driver = webdriver.Chrome(options=options)

    # For heroku
    driver = webdriver.Chrome(executable_path=os.environ["CHROMEDRIVER_PATH"])


    url = "https://www.mlb.com/yankees/scores/" + date
    driver.get(url)
    #print(driver)

    # Get the html node with the score
    classname = "g5-component--mlb-scores__panel g5-component--mlb-scores__panel--primary"
    xpath = ("//div[@class= '%s']" % classname)
    print(xpath)
    divs = driver.find_element_by_xpath(xpath)
    gameinfo = divs.text.split("\n")
    print(gameinfo)
    print("DONE")

@app.route("/", methods=["POST"])
def handle_msg():
    print("Handle POST")
    # print(flask.request.get_json())
    request = flask.request.get_json()

    if request["object"] == "page":
        for datum in request["entry"]:
            # Message data will always have only one message according to the docs
            message_data = datum["messaging"][0]

            if "text" in message_data["message"]:
                message = message_data["message"]["text"]

                print("MESSAGE IS ", message)
                # print("RECIPIENT ", message_data["recipient"]["id"])
                # print("SENDER ", message_data["sender"]["id"])
                # print("TOKEN ",os.environ["PAGE_ACCESS_TOKEN"])


                # Sending a message back !
                # After looking online I could've also used the param in reqest.post but oh well
                token = os.environ["PAGE_ACCESS_TOKEN"]
                url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + token

                # Recipient would be the sender
                recipient_id = message_data["sender"]["id"]

                headers = {
                "Content-Type": "application/json"
                }

                text = "hello, world!"

                if message.lower() == "yankees" or message.lower() == "nyy":
                    # Get today's date
                    current = str(datetime.datetime.now())
                    print("CURRENT ",current)
                    # print("Type ",type(current))
                    current = current.split(" ")
                    print(current)
                    date = current[0]

                    gameinfo = get_score(date)
                    text = " ".join(gameinfo)


                msg_to_send = {
                    "messaging_type": "RESPONSE",
                    "recipient":{
                      "id": recipient_id
                    },
                    "message":{
                      "text":text
                    }
                }

                msg = json.dumps(msg_to_send)
                #print(msg)
                print(url)
                print("about to post")
                #print("WHAT IS HAPPENING?")
                r = requests.post(url, headers=headers, data=msg)
                #print("POSTED THE MESSAGE?")

                print(r.status_code)
                print(r.text)
                print("Finished")
    return "Done!"


if __name__ == "__main__":
    app.run(debug=False)
