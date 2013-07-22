#!/usr/bin/env python
import re
import sys
import os, os.path

searchTarget = 'smtp.connect(self._smtp_host, self._smtp_port)\n'
undoTarget = '# SMTP FIX BEGIN\n'

relativeFilePath = 'google/appengine/api/mail_stub.py'

appEnginePathResult = os.environ.get('GOOGLE_APP_ENGINE')

if appEnginePathResult != None:
	targetFilePath = appEnginePathResult + '/' + relativeFilePath
else:
	targetFilePath = relativeFilePath

def main():

	try:
		f = open(targetFilePath, 'r')
		fileContents = f.readlines()
		f.close()
	except IOError as e:
		print "Aborting. Target file not found. Add --help for help."
		return

	if len(sys.argv) < 2:

		if [ i for i, word in enumerate(fileContents) if word.endswith(undoTarget) ] != []:
			print "Aborting. SMTP TLS patch already done."
			return

		targetLineNumber = int([ i for i, word in enumerate(fileContents) if word.endswith(searchTarget) ][0]) + 1
		targetLine = fileContents[targetLineNumber]

		print "Target string found at line: " + str(targetLineNumber - 1)

		leadingSpaces = re.match(r'(\W+)', targetLine).group(1)

		print "Adding SMTP TLS fix lines to mail_stub.py"
		fileContents.insert(targetLineNumber, leadingSpaces + '# SMTP FIX END\n')
		fileContents.insert(targetLineNumber, leadingSpaces + 'smtp.ehlo()\n')	
		fileContents.insert(targetLineNumber, leadingSpaces + 'smtp.starttls()\n')
		fileContents.insert(targetLineNumber, leadingSpaces + 'smtp.ehlo()\n')
		fileContents.insert(targetLineNumber, leadingSpaces + '# SMTP FIX BEGIN\n')

		f = open(targetFilePath, "w")
		f.writelines(fileContents)
		f.close()
	else:
		firstArgument = sys.argv[1]

		if firstArgument == "--help" or firstArgument == "-h":
			print "Github: https://github.com/chrisbutcher/appengine-smtp-tls-fix"
			print "=============================================================="
			print "Place `fixsmtp.py` into the root of your `google_appengine` folder, then"
			print "To install:"
			print "'python fixsmtp.py' or 'chmod +x fixsmtp.py; ./fixsmtp' (without quotes)"
			print "To remove:"
			print "'python fixsmtp.py undo' or 'chmod +x fixsmtp.py; ./fixsmtp undo' (without quotes)"
		elif firstArgument == "undo":

			if [ i for i, word in enumerate(fileContents) if word.endswith(undoTarget) ] == []:
				print "Aborting. SMTP path already removed."
				return

			targetLineNumber = int([ i for i, word in enumerate(fileContents) if word.endswith(undoTarget) ][0])
			print "Target string found at line: " + str(targetLineNumber - 1)

			print "Removing SMTP TLS fix lines to mail_stub.py"
			del fileContents[targetLineNumber:targetLineNumber + 5]

			f = open(targetFilePath, "w")
			f.writelines(fileContents)
			f.close()
		else:
			print "Invalid command. Use --help or -h for help."

if  __name__ =='__main__':
	main()