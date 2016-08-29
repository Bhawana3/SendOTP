import plivo

def send_sms (to_number, body):
	auth_id = "MANME4ZJQ2ZWU4ZTZHYZ"
	auth_token = "ODNiZDY0YmU4ODRlYmU2MGI3M2QyZDU4NjhhMWYw"

	p = plivo.RestAPI(auth_id, auth_token)
	params = {
	    'src': '91988618345',
	    'dst' : '91' + str(to_number),
	    'text' : body,
	    'url' : "", 
	    'method' : 'POST'
	}
	response = p.send_message(params)
	print "Status Code:", str(response[0])
	print "Response: ", str(response[1])

	if not(('200' < str(response[0])) and (str(response[0]) < '299')):
		raise Exception(response[1]['error'])
