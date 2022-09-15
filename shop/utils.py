import pyrebase
import secrets, os
from dotenv import load_dotenv

load_dotenv()

firebase_config = {
    'apiKey': "AIzaSyDONrFp2bNY1vw5Lm9mCvTc4NVRyjlgdv4",

  'authDomain': "mosh-photography.firebaseapp.com",

  'projectId': "mosh-photography",

  'storageBucket': "mosh-photography.appspot.com",

  'messagingSenderId': "743008571288",

  'appId': "1:743008571288:web:5a1ba6ffa447c6c78225ed",

  'measurementId': "G-H1TRK2PB0K",
  'databaseURL': ''

}

firebase = pyrebase.initialize_app(firebase_config)
storege = firebase.storage()


auth = firebase.auth()
email = os.getenv('FIREBASE_EMAIL')
password = os.getenv('FIREBASE_PASSWORD')



def upload_image(directory, file):
    print('image upload called')
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.name)
    filename = random_hex + f_ext
    file.name = filename
    directory = directory + '/' + filename
    print('filename: ', file.name)
    storege.child(directory).put(file)
    return filename

def get_image_url(directory, filename, user):
    path = directory + '/' + filename
    url = storege.child(path).get_url(user['idToken'])
    return url
    