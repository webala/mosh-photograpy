import pyrebase4
import secrets, os

firebase_config = {
    'apiKey': "AIzaSyDONrFp2bNY1vw5Lm9mCvTc4NVRyjlgdv4",

  'authDomain': "mosh-photography.firebaseapp.com",

  'projectId': "mosh-photography",

  'storageBucket': "mosh-photography.appspot.com",

  'messagingSenderId': "743008571288",

  'appId': "1:743008571288:web:5a1ba6ffa447c6c78225ed",

  'measurementId': "G-H1TRK2PB0K"

}
firebase = pyrebase4.initialize_app(firebase_config)
storege = firebase.storage()

def upload_image(directory, file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    filename = random_hex + f_ext
    file.filename = filename
    storege.child(directory).put(file)
    return filename
    