import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore,db

# Use a service account
cred = credentials.Certificate('static/myemailapp-fbc93-ca8dccc97173.json')
firebase_admin = firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://myemailapp-fbc93.firebaseio.com/'
})

ref = db.reference('users')