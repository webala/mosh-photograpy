import pyrebase
import secrets, os, requests, json, base64, smtplib, ssl
from requests.auth import HTTPBasicAuth
from django.conf import settings
from datetime import datetime
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
from django.core.files import File
from email.message import EmailMessage


load_dotenv()

firebase_config = {
    "apiKey": "AIzaSyDONrFp2bNY1vw5Lm9mCvTc4NVRyjlgdv4",
    "authDomain": "mosh-photography.firebaseapp.com",
    "projectId": "mosh-photography",
    "storageBucket": "mosh-photography.appspot.com",
    "messagingSenderId": "743008571288",
    "appId": "1:743008571288:web:5a1ba6ffa447c6c78225ed",
    "measurementId": "G-H1TRK2PB0K",
    "databaseURL": "",
}

firebase = pyrebase.initialize_app(firebase_config)
storege = firebase.storage()


auth = firebase.auth()
email = os.getenv("FIREBASE_EMAIL")
password = os.getenv("FIREBASE_PASSWORD")


def compress(image, f_ext):
    im = Image.open(image)
    im_io = BytesIO()
    im.save(im_io, "JPEG", quality=60)
    new_image = File(im_io, name=image.name)
    return new_image


def upload_image(directory, file):
    print("image upload called")
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.name)
    filename = random_hex + f_ext
    file.name = filename
    image = compress(file, f_ext[1:])
    print("image:", image)
    directory = directory + "/" + filename
    print("filename: ", image.name)
    storege.child(directory).put(image)
    return filename


def get_image_url(directory, filename, user):
    path = directory + "/" + filename
    url = storege.child(path).get_url(user["idToken"])
    return url


# Function to generate daraja access token
def get_access_token():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    response = requests.get(
        settings.DARAJA_AUTH_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret)
    )

    json_res = response.json()
    access_token = json_res["access_token"]
    return access_token


# function to format date time
def format_date_time():
    current_time = datetime.now()
    formated_time = current_time.strftime("%Y%m%d%H%M%S")
    return formated_time


# function to generate password string
def generate_password(dates):
    data_to_encode = (
        str(settings.BUSINESS_SHORT_CODE) + settings.LIPANAMPESA_PASSKEY + dates
    )
    encoded_string = base64.b64encode(data_to_encode.encode())
    decoded_passkey = encoded_string.decode("utf-8")

    return decoded_passkey


# function to initiate stk push for mpesa payment
def initiate_stk_push(phone, amount):
    access_token = get_access_token()
    formated_time = format_date_time()
    password = generate_password(formated_time)

    headers = {"Authorization": "Bearer %s" % access_token}

    payload = {
        "BusinessShortCode": settings.BUSINESS_SHORT_CODE,
        "Password": password,
        "Timestamp": formated_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": phone,
        "PartyB": "174379",
        "PhoneNumber": phone,
        "CallBackURL": "https://962a-102-219-208-82.in.ngrok.io/stk_callback",
        "AccountReference": "GLITCH CLOUD PHOTOGRAPHY",
        "TransactionDesc": "Make Payment",
    }

    response = requests.post(settings.API_RESOURCE_URL, headers=headers, json=payload)

    string_response = response.text
    string_object = json.loads(string_response)

    if "errorCode" in string_object:
        print("Error: ", string_object)
        return string_object
    else:
        data = {
            "merchant_request_id": string_object["MerchantRequestID"],
            "chechout_request_id": string_object["CheckoutRequestID"],
            "response_code": string_object["ResponseCode"],
            "response_description": string_object["ResponseDescription"],
            "customer_message": string_object["CustomerMessage"],
        }
    return data


def send_app_message(phone, type):
    phone_number_id = "+1 555 046 0909"
    recipient_phone_number = "+254791055897"
    access_token = "EAAQgBW2ERmgBAJ6gtvoHs3t7XsKlEXZCwQd85IovfO7rVGZAFXkVZBw7BeyrkjMIWvPZAS1LZCmQiNibZA4xZAU1TA4OeOYHzcehtEeJs2ZCRIJaDcpdLdCc5PIP5mD2TmOZCvw1uQhTLjeIIuRSjI0JFB54ycFi0pWWIwSTF7OSPfSWEj5SHZB9ezPJtOIKnEL2eXLNWzpnZBiZCsltqOuDgQFy"
    endpoint = f"https://graph.facebook.com/v14.0/{phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    data = {
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": f"{recipient_phone_number}",
      "type": "text",
      "text": { 
        "preview_url": False,
        "body": "MESSAGE_CONTENT"
        }
    }

    response = requests.post(endpoint, headers=headers, data=json.dumps(data))

    if response.ok:
        print("success")
    else:
        print("failed")
        print("response: ", response.json())



def send_email(subject, body, receiver):
    email_sender = 'webdspam@gmail.com'
    email_password = os.getenv('GMAIL_L0GIN')
    email_receiver = receiver

    #Instantiate EmailMessage class
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    #Use SSL to add a layer of security
    context = ssl.create_default_context()

    #Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
