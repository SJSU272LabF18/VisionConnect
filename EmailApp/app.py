#!/usr/bin/env python

import urllib
import json
import os

import firebase_admin
import requests
from firebase_admin import db
from flask import Flask, jsonify
from flask import request
from flask import make_response
from flask_mail import Mail, Message
import sendgrid
import os
from sendgrid.helpers.mail import *

from cloud import ref

app = Flask(__name__)
mail = Mail(app)
msg_dict = {}


@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    # print("Request:")
    # print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)
    print(res)
    # res = json.dumps(res, indent=4)
    # print(res)
    # r = make_response(res)
    # r.headers['Content-Type'] = 'application/json'
    # res["fulfillmentText"]
    s = str(res["fulfillmentText"])
    print(s)
    return jsonify({"fulfillmentText": s,})
    # return jsonify({"fulfillmentMessages": res["fulfillmentMessages"], })


def makeWebhookResult(req):
    if req.get("queryResult").get("intent").get("displayName") == "EmailIntent":
        response = sendEmailLogic(req)
    elif(req.get("queryResult").get("intent").get("displayName") == "EmailIntent - yes" or req.get("queryResult").get("intent").get("displayName") == "ShowEmailIntent"):
        print("inside showemailintent")
        response = showEmailLogic(req)
    # elif(req.get("expectedInputs").get("possibleIntents").get("intent") == )
    # print(req.get("expectedInputs").get("possibleIntents").get("intent"))
    return response


def sendEmailLogic(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    receiver = parameters.get("receiver")
    message = parameters.get("message")
    print("Hi")
    # cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}

    speech = "Hello!"

    print(ref.get()['LoggedInUser'])
    ref.push({
        u'message_text': message,
        u'receiverEmail': receiver,
        u'senderEmail': ref.get()['LoggedInUser']
    })
    # snapshot = ref.order_by_key().get()
    # for key, val in snapshot.items():
    #     if val['receiverEmail'] == 'nsharma335@gmail.com':
    #         print('{0} => {1}'.format(key, val))
    # print(ref.get())

    # users_ref = db.collection(u'users')
    # docs = users_ref.get()
    # for doc in docs:
    #     print(u'{} => {}'.format(doc.id, doc.to_dict()))
    # db = firebase_admin.get_app()
    # ref = db.reference(u'users')
    # print("Here" + ref.get())

    # msg = send_simple_message(receiver, message)
    # email_message(receiver,message)
    # print("Response:")
    # print(msg)
    r = {
        "fulfillmentText": "Email sent successfully to " + receiver + " saying " + message + "\nDo you want me to show your emails?",
        "data": {},
        "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }
    return r


def showEmailLogic(req):
    docs = ref.get()
    fumfillmenttext = ""
    count = 0

    snapshot = ref.order_by_key().get()
    for key, val in snapshot.items():
        print(val)
        # print(val['receiverEmail'])
        if not isinstance(val, str):
            if val['receiverEmail'] == ref.get()['LoggedInUser']:
                fumfillmenttext += val['senderEmail'] + " sent an email to you saying " + val['message_text'] + "\n"
                # print('{0} => {1}'.format(key, val))

    # for doc in docs:
    #     msg_dict[doc.id] = doc.to_dict()
    #     print("doc.id: " + doc.id)
    #     if msg_dict[doc.id]['receiverEmail'] == "nsharma335@gmail.com":
    #         count += 1
    #         print(u'{} => {}'.format(oc.id, doc.to_dict()))
    #         # print(msg_dict['']['message'])
    #         if count==1:
    #             fumfillmenttext += doc.id + " sent an email to you saying " + msg_dict['userDocument']['message']
    #         if count == 2:
    #             fumfillmenttext += "\nAnd " + doc.id + " sent an email to you saying " + msg_dict['userDocument']['message']
    #         if count > 2:
    #             fumfillmenttext += "\nAlso " + doc.id + " sent an email to you saying " + msg_dict['userDocument'][
    #                 'message']

    if fumfillmenttext == "":
        fumfillmenttext = "You currently do not have any new emails\n"
    r = {
         "fulfillmentText": fumfillmenttext,
          "data": {},
          "contextOut": [],
          "source": "apiai-onlinestore-shipping"
    }
    return r


def email_message(receiver,message):
    sg = sendgrid.SendGridAPIClient(apikey='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')
    from_email = Email("myemailapp@myemailapp.com")
    to_email = Email(receiver)
    subject = "Message from My Email App"
    content = Content("text/plain", message + "\n\n Sent by " + "janhavidahihande@gmail.com")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')