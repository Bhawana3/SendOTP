from flask import Blueprint, render_template, request
from flask.views import MethodView
from .models import Contacts, Messages


views = Blueprint ("views", __name__, template_folder='templates')


"""
	Display a list of contacts from the database
"""
class ListView (MethodView):
	def get (self):
		contact_list = Contacts.query.all()
		return render_template('index.html', contacts_list=contact_list)


"""
	Get details of a particular contact
"""
class DetailView (MethodView):
    def get (self, id):
    	contact = Contacts.query.filter_by(id=id).first()
        return render_template('contact_details.html', contact=contact)

"""
	Send message to the particular contact
"""
class SendView (MethodView):

	def get (self):
		# Generate OTP and message
		from random import randint
		otp = randint(100000,1000000)
		msg =  "Hi. Your OTP is: " + str(otp)

		contact_id = request.values.get('id')
		number = request.values.get('number')

		return render_template('edit.html', id=contact_id, number=number, otp=otp, msg=msg)

	
	def post (self):
		otp=request.values.get('otp')
		msg=request.values.get('msg')
		number=request.values.get('number')
		
		# Send the OTP
		from utils import send_sms
		try:
			send_sms (to_number=number, body=msg)
		except Exception as e:
			print e
			return render_template('error.html')

		# Save the OTP
		message = Messages(otp=otp, msg=msg, contact_id=request.values.get('id'))
		message.save()
		
		return render_template('sent.html', number=number)

"""
	Display a list of messages in decreasing order of date-time
"""
class MessageListView (MethodView):

	def get (self):
		messages = Messages.get_messages()
		return render_template('messages.html', messages=messages)

"""
	Add a new contact
"""
class AddContactView (MethodView):

	def get(self):
		return render_template('add_contact.html')

	def post (self):
		#print type(request)
		#print dir(request.values)
		print request.form.keys()
		contact = Contacts (
			number=request.form.get('number'), 
			firstname=request.form.get('firstname'), 
			lastname=request.form.get('lastname')
			)
		contact_list = list()
		try:
			contact.save()
			contact_list = Contacts.query.all()
		except Exception as e:
			print e
			return render_template('erro.html')
		return render_template('index.html', contacts_list=contact_list)



# Register the urls
views.add_url_rule('/', view_func = ListView.as_view ('contacts'))
views.add_url_rule('/contact/add/', view_func = AddContactView.as_view ('add'), methods=['GET', 'POST'])
views.add_url_rule('/contact/<id>/', view_func = DetailView.as_view ('detail'))
views.add_url_rule('/send/', view_func = SendView.as_view ('send'), methods=['GET','POST'])
views.add_url_rule('/messages/', view_func = MessageListView.as_view ('messages'))
