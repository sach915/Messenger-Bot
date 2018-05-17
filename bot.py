import flask
import requests
import os
import json
from bs4 import BeautifulSoup
import datetime

app = flask.Flask(__name__)

@app.route("/", methods=["GET"])
def verification():
    print("Im in here")
    print(flask.request.args)

    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if flask.request.args.get("hub.mode") == "subscribe" and flask.request.args.get("hub.challenge"):
        if not flask.request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return flask.request.args["hub.challenge"], 200


    return "Hello World"

@app.route("/", methods=["POST"])
def handle_msg():
    print("Handle POST")
    print(flask.request.get_json())
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

                #print(recipient_id)


                headers = {
                "Content-Type": "application/json"
                }


                msg_to_send = {
                    "messaging_type": "RESPONSE",
                    "recipient":{
                      "id": recipient_id
                    },
                    "message":{
                      "text":"hello, world!"
                    }
                }

                current = str(datetime.datetime.now())
                print("CURRENT ",current)
                current = current.split(" ")
                print(current)
                # Trying to get mlb.com data


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
