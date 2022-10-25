from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime


cluster  = MongoClient("mongodb+srv://karan:p&Q7jp&!tG5hTHTy@cluster0.ebhdrht.mongodb.net/?retryWrites=true&w=majority")
db = cluster["apixelhouse"]
users = db["users"]



app = Flask(__name__)


@app.route("/", methods=["get", "post"])
def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")
    res = MessagingResponse()
    user = users.find_one({"number":number})
    if bool(user) == False:
        res.message("Hi, thanks for contacting *A PIXEL HOUSE Digital Agency*. \nYou can choose from one of the"
            " options below: \n\n*Services*\n\n1️⃣ To *Sales Department* us \n2️⃣ For *Job / Career* \n3️⃣ To *Contact Us* "
            "\n4️⃣ For *Working Hours*")
        users.insert_one({"number": number, "status": "main", "message":[]})
    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response.\nYou can choose from one of the"
            " options below: \n\n*Services*\n\n1️⃣ To *Sales Department* us \n2️⃣ For *Job / Career* \n3️⃣ To *Contact Us* "
            "\n4️⃣ For *Working Hours*")
            return str(res)

        if option == 1:
            res.message("For interest in our services, you can contact us through the following medium: \n*Phone:* +91 95401 90373 | +91 6289 454 934,\n*Email:* info@apixelhouse.com,\n*Link:* http://www.estimate.apixelhouse.com")
        elif option ==2:
            res.message("For being a part of our team, you can call or message us at: \n*Phone:* +91 98318 29566, \n*Email:* hr@apixelhouse.co.in, \n*Link:* http://www.career.apixelhouse.com")
        elif option ==3:
            res.message("For any query, you can call us at \n*Phone:* +91 98318 29566\n*Email:* hr@apixelhouse.co.in")
        elif option ==4:
            res.message("We work weekdays from 10am to 7pm IST. You can email us at info@apixelhouse.com for any query.")
        else:
            res.message("Please enter a valid response")
    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(res)


if __name__ == "__main__":
    app.run()
