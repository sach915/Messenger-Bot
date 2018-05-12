import flask
import requests
import os

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
            message_data = datum["messaging"]
            message = message_data["message"]["text"]
            print("MESSAGE IS ", message)
            print("RECIPIENT ", message_data["recipient"]["id"])
            print("SENDER ", message_data["sender"]["id"])


    return "Done!"


if __name__ == "__main__":
    app.run(debug=False)
