import cgi
import json
from google.appengine.api import users
import webapp2
from lib.datastore import store_booking, get_bookings, cancel_bookings
MAIN_PAGE_HTML = 'static/home.html'

class MainPage(webapp2.RequestHandler):
    def get(self):
        mp = open(MAIN_PAGE_HTML, 'r')
        self.response.write(mp.read())

class Guestbook(webapp2.RequestHandler):
    def post(self):
        self.response.write('<html><body>Your Input:<pre>')
        self.response.write(cgi.escape(self.request.get('pickup')))
        self.response.write('</pre></body></html>')
        
class HandleBooking(webapp2.RequestHandler):
    def post(self):
        try:
            user = users.get_current_user()
            if user is None:
                raise ValueError("Please login to complete booking")
            params = {            
                      'pickup' : self.request.get('pickup'),
                      'pickup_date' : self.request.get('pickup_date'), 
                      'mobile_no' : self.request.get('mobile_no'),
                      'email_address' : self.request.get('email_address'),
                      'address' : self.request.get('address'),
                      'to_airport' : self.request.get('to_airport'),
                      'name' : user.nickname() 
            }
            booking_id = store_booking(params)
            self.response.write(booking_id)
        except (TypeError, ValueError) as e:
            self.response.write(str(e))        

class HandleLogin(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        url = "#"
        nick_name = "Sign In"
        if user:
            url = users.create_logout_url('/')
            nick_name = user.nickname()
        else:
            url = users.create_login_url('/')

        print url, nick_name
        self.response.out.write('["%s", "%s"]' % (url, nick_name))
    
class GetBookings(webapp2.RequestHandler):
    def post(self):
        user = users.GetCurrentUser()
        bookings_result = []
        if user:
            bookings = get_bookings(user.nickname())
            for b in bookings:
                bs = [str(i) for i in b]
                bookings_result.append(bs)
        self.response.headers['Content-Type'] = 'application/json'   
        self.response.out.write(json.dumps(bookings_result))
        
class CancelBooking(webapp2.RequestHandler):
    def post(self):
        booking_ids = json.loads(self.request.get('booking_ids'))
        cancel_bookings(booking_ids)
        user = users.GetCurrentUser()
        bookings_result = []
        if user:
            bookings = get_bookings(user.nickname())
            for b in bookings:
                bs = [str(i) for i in b]
                bookings_result.append(bs)
        self.response.headers['Content-Type'] = 'application/json'   
        self.response.out.write(json.dumps(bookings_result))
        
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
    ('/confirm_booking', HandleBooking),
    ('/do_signin', HandleLogin),
    ('/my_bookings', GetBookings),
    ('/cancel_booking', CancelBooking)
], debug=True)