'''
Created on 10-Sep-2014

@author: Nirmal Tudu
'''
from datetime import datetime
from google.appengine.ext import db

class Route(db.Model):
    source = db.StringProperty(required=True)
    destination = db.StringProperty(required=True)
    route_data = db.StringProperty(required=False)
    distance   = db.FloatProperty(required=False)
    estimated_travel_time = db.TimeProperty(required=False)

class Customer(db.Model):
    mobile_no = db.PhoneNumberProperty(required=True)
    email_id  = db.EmailProperty(required=True)
    gender    = db.StringProperty(required=False)
    name      = db.StringProperty(required=False)
    address   = db.StringProperty(required=False)

class Booking(db.Model):
    '''
    
    '''
    customer_mobile_no = db.PhoneNumberProperty(required=True)
    customer_email_id  = db.EmailProperty(required=True)
    customer_name = db.StringProperty(required=True)
    pickup_datetime = db.DateTimeProperty(required=True)
    arrival_soft_datetime = db.DateTimeProperty(required=False)
    arrival_hard_datetime = db.DateTimeProperty(required=False)
    route_source = db.StringProperty(required=True)
    route_destination = db.StringProperty(required=True)
    willing_to_share      = db.BooleanProperty(required=True)
    no_of_passengers      = db.IntegerProperty(required=True)
    luggage_weight        = db.FloatProperty(required=True)
        

def _get_pickup_datetime(date_str):        
    pickup_date = date_str.split(".")[0]
    pickup_date = pickup_date.replace('"', '')
    (pd, pt) = pickup_date.split("T")
    (year, month, day) = pd.split("-")
    (hour, minute, sec) = pt.split(":")
    return datetime(int(year), int(month), int(day), int(hour), int(minute), int(sec))

def store_booking(params):
    to_airport = params['to_airport']
    src = "RGIA, Hyderabad, Andhra Pradesh, India"
    dest = params['pickup']
    if to_airport:
        dest = "RGIA, Hyderabad, Andhra Pradesh, India" 
        src = params['pickup']
    route = Route(source=src,
                  destination=dest)
    route.put()
    
    booking = Booking(customer_name=params['name'],
                      customer_mobile_no=params['mobile_no'],
                      customer_email_id=params['email_address'],
                      route_source=src,
                      route_destination=dest,
                      pickup_datetime=_get_pickup_datetime(params['pickup_date']),
                      willing_to_share=True,
                      no_of_passengers=1,
                      luggage_weight=2.5)
    db.put(booking)
    k_key = booking.key()
    booking_id = k_key.id()
    return booking_id
    
def get_bookings(user):
    q = Booking.all()
    q.filter('customer_name = ', user)
    res = list()
    for p in q.run():
        res.append([p.key().id(), p.pickup_datetime, p.route_source, p.route_destination])
    return res

def cancel_bookings(booking_id):
    b = db.Key.from_path("Booking", long(booking_id))
    bk = db.get(b)
    bk.delete()
    #  db.Key(Booking, long(booking_id)).delete()
    return True
