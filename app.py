import os
import tornado.auth
import tornado.autoreload
import tornado.ioloop
import tornado.web
import json

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class TestHandler(BaseHandler):
		def get(self):
				name = tornado.escape.xhtml_escape(self.current_user)
				print self.get_current_user()
				self.write("Hello, " + name)

class MainHandler(BaseHandler):
		def get(self):
				if not self.current_user:
						self.redirect("/")
						return

class GoogleOAuth2LoginHandler(BaseHandler, tornado.auth.GoogleOAuth2Mixin):
		@tornado.gen.coroutine
		def get(self):
				if self.get_argument('code', False):
						access = yield self.get_authenticated_user(
								redirect_uri=os.environ['REDIRECT_URI'],
								code=self.get_argument('code'))
						user = yield self.oauth2_request("https://www.googleapis.com/oauth2/v1/userinfo", access_token=access["access_token"])
						self.set_secure_cookie("user", json.dumps(user))
						# Save the user with e.g. set_secure_cookie
						self.current_user = user
						self.redirect('/test')
				else:
						yield self.authorize_redirect(
								redirect_uri=os.environ['REDIRECT_URI'],
								client_id=os.environ['CLIENT_ID'],
								client_secret=os.environ['CLIENT_SECRET'],
								scope=['profile', 'email'],
								response_type='code',
								extra_params={'approval_prompt': 'auto'}
						)

def make_app():
		settings = {
				'google_oauth' : {
						'key': os.environ['CLIENT_ID'],
						'secret': os.environ['CLIENT_SECRET'],
				},
				'redirect_uri': os.environ['REDIRECT_URI'],
				'login_url': '/',
				'cookie_secret': os.environ['COOKIE_SECRET']
		}
		return tornado.web.Application([
				(r"/", GoogleOAuth2LoginHandler),
				(r"/test", TestHandler)], **settings)

if __name__ == "__main__":
		app = make_app()
		app.listen(8888)
		print "Listening on port 8888"
		tornado.autoreload.start()
		for dir, _, files in os.walk('./'):
				[tornado.autoreload.watch(dir + '/' + f) for f in files if not f.startswith('.')]

		tornado.ioloop.IOLoop.current().start()

