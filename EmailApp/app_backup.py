#!/usr/bin/env python

import urllib
import json
import os

import requests
from flask import Flask
from flask import request
from flask import make_response
from flask_mail import Mail, Message

# Flask app should start in global layout
app = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'janhavidahihande@gmail.com',
    "MAIL_PASSWORD": 'ievallprbgvlleyc'
}
app.config.update(mail_settings)
mail = Mail(app)


@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeWebhookResult(req):
    if req.get("queryResult").get("intent").get("displayName") != "Languages":
        print("Hi")
    result = req.get("queryResult")
    parameters = result.get("parameters")
    zone = parameters.get("language")
    print("Hi")
    # cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}

    speech = "Hello! "
    #with app.app_context():
        # msg = Message(subject=speech,
        #               sender=app.config.get("MAIL_USERNAME"),
        #               recipients=["janhavidahihande@gmail.com"],  # replace with your email for testing
        #               body="This is a test email!")
        # mail.send(msg)

    msg = send_simple_message(zone)
    print("Response:")
    print(msg)

    return {
        # "fulfillmentText": speech,
        # "data": {},
        # "contextOut": [],
        # "source": "apiai-onlinestore-shipping"
    }


def send_simple_message(zone):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox8cc62313e362427e926edb162c297f28.mailgun.org/messages",
        auth=("api", "7dc0f655cff9219a9e8887766a53ce4a-1053eade-957689bb"),
        data={"from": "My Email System<postmaster@sandbox8cc62313e362427e926edb162c297f28.mailgun.org>",
              "to": "Janhavi Dahihande <janhavi.dahihande@sjsu.edu>",
              "subject": "Hello Janhavi Dahihande",
              "text": "Congratulations Janhavi Dahihande, , you just received an email from " + zone})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')