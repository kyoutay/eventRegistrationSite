from flask import Blueprint, render_template, request, flash, jsonify
from flask_mail import Message
from website import sheets,mail
import paypalrestsdk as prs
from datetime import datetime
import urllib.parse as ul

views = Blueprint('views',__name__)

SUCCESS = False
ADMINMODE = False

prs.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "", #create a paypal sandbox account
  "client_secret": "" }) 

def sendEmail(title,message,recipients,imageLink=""):
    with mail.connect() as conn:
        for user in recipients:
            msg = Message(title,recipients=[user])
            msg.html = render_template('emailTemplate.html', value=imageLink, message=message)
            conn.send(msg)

@views.route("/about")
def home():
    return render_template("about.html")

@views.route("/registrationFee", methods=['POST'])
def registrationFee():
    payment = prs.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Reserve Spot",
                    "sku": "12345",
                    "price": "5.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "5.00",
                "currency": "USD"},
            "description": "Reserve your spot at the conference"}]})
    if payment.create():
        print('success')
    else:
        print(payment.error)

    return jsonify({'paymentID':payment.id})

@views.route("/execute", methods=['POST'])
def execute():
    global SUCCESS
    SUCCESS = False
    payment = prs.Payment.find(request.form['paymentID'])
    if payment.execute({'payer_id' : request.form['payerID']}):
        print('payment success')
        flash('payment success',category='success')
        SUCCESS = True
    else:
        print(payment.error)
        SUCCESS = False
    return jsonify({'success' : SUCCESS})

@views.route("/checkStatus", methods=['GET', 'POST'])
def checkStatus():
    if request.method == 'POST':
        email = request.form.get('checkEmail')
        if sheets.checkEmail(email):
            flash('You\'re registered for the conference!', category='success')
        else:
            flash('Sorry, we couldn\'t find you in our systems', category='error')
    return render_template("checkStatus.html")

@views.route("/deleteSpot", methods=['GET','POST'])
def deleteSpot():
    if request.method == 'POST':
        deleteEmail = request.form.get('deleteSpot')
        if sheets.checkEmail(deleteEmail):
            sheets.deleteSpot(deleteEmail)
            flash('You\'ve been removed from the list!', category='success')
            sendEmail('Spot Cancellation Confirmation',"Thanks for letting us know you won't be attending",[deleteEmail])
        else:
            flash("Your name already isn't on the list", category='error')
    return render_template("checkStatus.html")

@views.route("/adminLogin", methods=['GET','POST'])
def adminLogin():
    global ADMINMODE
    if request.method == 'POST':
        password = request.form.get('adminLogin')
        if password == 'blah':
            ADMINMODE = True
        else:
            flash('Please try again', category='error')
            ADMINMODE = False
        if "open" in request.form:
            ADMINMODE = False
    if not ADMINMODE:
        return render_template("adminLogin.html")
    return render_template("adminPage.html", spotsLeft=sheets.getSpotsLeft(), registrantsSheet="", canceledUsersSheet="")

@views.route("/broadcastEmail", methods=['GET','POST'])
def broadcastEmail():
    if request.method == 'POST':
        title=request.form.get('emailTitle')
        message=request.form.get('message')
        imageLink=request.form.get('imageLink')
        recipients=sheets.sheet.col_values(5)
        recipients.pop(0)
        print(message)
        sendEmail(title,message,recipients,imageLink)
        flash('Email successfully sent!',category="success")
    return render_template('adminPage.html')

#title,message,file,recipients

@views.route("/checkIn", methods=['GET','POST'])
def confirmSpot():
    checkInEmail = request.args.get('checkInEmail')
    sheets.checkIn(checkInEmail)
    print('checkIn success')
    return render_template("success.html")


@views.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        affliation = request.form.get('affliation')
        interest = request.form.get('interest')
        email = request.form.get('email')
        phoneNumber = request.form.get('phoneNumber')
        accomodations = request.form.get('accomodations')
        address = request.form.get('address')
        zip = request.form.get('zip')

        if SUCCESS == False:
            flash('Please make sure you\'ve paid the registration fee', category='error')
        else:
            flash('Successful! We\'ve received your info. Please check your email for details')
            sheets.addToSheets(firstName,lastName,affliation,interest,email,phoneNumber, accomodations, address, zip, datetime.now().strftime("%d/%m/%Y %H:%M"))
            encodedUrl = ul.quote('http://127.0.0.1:8000/checkIn?checkInEmail='+email) #change to actual website
            sendEmail('Conference Registration Details', 'Thank you for your registering for the conference, you\'ve been added into our systems.',[email],"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="+encodedUrl)
    return render_template("register.html", value=sheets.getSpotsLeft()>0)




