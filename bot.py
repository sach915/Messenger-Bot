import flask
import requests
import os

app = flask.Flask(__name__)

@app.route("/", methods=["GET"])
def index():

    # Credit to : https://github.com/hartleybrody/fb-messenger-bot/blob/master/app.py
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True)
