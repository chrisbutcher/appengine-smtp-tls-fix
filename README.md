appengine-smtp-tls-fix
======================

A small python script to quickly patch the Google App Engine development server to support TLS over SMTP (required to send emails from your app using a Gmail.com account)

### To install:
Place fixsmtp.py into the root of your `google_appengine` folder, then run
    'python fixsmtp.py' or 'chmod +x fixsmtp.py; ./fixsmtp' (without quotes)
			
### To remove:
    'python fixsmtp.py undo' or 'chmod +x fixsmtp.py; ./fixsmtp undo' (without quotes)
