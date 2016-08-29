from sendOTPApp import db, Session
from datetime import datetime


class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    number = db.Column(db.String(10), unique=True)
    messages = db.relationship('Messages', backref='contacts',
                                uselist=False)

    def __init__(self, number, firstname=None, lastname=None):
    	self.number = number
    	if firstname is not None:
    		self.firstname = firstname
    	if lastname is not None:
    		self.lastname = lastname

    def __repr__(self):
        return '<User %r>' % self.firstname

    def save (self):
        db.session.add(self)
        db.session.commit()

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    otp = db.Column(db.String(6))
    msg = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    is_verified = db.Column(db.Boolean)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'))

    def __init__(self, otp, msg, contact_id, timestamp=None, is_verified=None):
        self.otp = otp
        self.msg = msg
        self.contact_id = contact_id
        if timestamp is None:
            self.timestamp = datetime.utcnow()
        if is_verified is None:
            self.is_verified = False

    def __repr__(self):
        return '<Message %r>' % self.otp

    @staticmethod
    def get_messages ():
        from sqlalchemy import desc
        session = Session()
        messages = session.query(Messages, Contacts).join(Contacts).order_by(desc(Messages.timestamp)).all()
        return messages

    def save (self):
        db.session.add (self)
        db.session.commit()