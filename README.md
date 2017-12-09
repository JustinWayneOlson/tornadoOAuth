# tornadoOAuth
[python-tornado](http://www.tornadoweb.org/en/stable/) (2.7) project boilerplate for google Oauth

## Install and Run
##### Clone the Repo

    git clone https://github.com/JustinWayneOlson/tornadoOauth
    
 ##### Install python-tornado
 
    pip install tornado
    
##### Register with Google Api's
- Go to the [Google Dev Console](https://console.developers.google.com/cloud-resource-manager) and register a new web application for the OAuth credentials
- Under Credentials register 	`http://localhost:8888/` as an authorized redirect URL
- Note the Client ID and Client Secret on this credentials page

##### Set up Environment Variables
    
Set up a small script to initialize your environment variables that won't get checked into version control.
    
###### env.conf

    export REDIRECT_URI="http://localhost:8888/"
    export PORT=8888
    export CLIENT_ID="Your client id here"
    export CLIENT_SECRET="Your client secret here"
    export COOKIE_SECRET="A randomized string here"
  
Run the script. You can do this in .bashrc as well. 
   
    source [pathToProject/tornadoOauth]/env.conf
      

##### Run the server

    python app.py
    
    
## Relevant Documentation
- [Tornado Authentication and Security](http://www.tornadoweb.org/en/stable/guide/security.html)
- [Tornado Asynchronous & Non-blocking I/O](http://www.tornadoweb.org/en/stable/guide/async.html) 
- [Google OAuth](https://developers.google.com/identity/protocols/OAuth2)
