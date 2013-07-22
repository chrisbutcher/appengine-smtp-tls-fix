#!/usr/bin/env python
import re
import sys

searchTarget = 'smtp.connect(self._smtp_host, self._smtp_port)\n'
undoTarget = '# SMTP FIX BEGIN\n'

def main():
	if len(sys.argv) < 2:

		f = open('google/appengine/api/mail_stub.py', 'r')
		fileContents = f.readlines()
		f.close()

		if [ i for i, word in enumerate(fileContents) if word.endswith(undoTarget) ] != []:
			print "Aborting. SMTP patch already done."
			return

		targetLineNumber = int([ i for i, word in enumerate(fileContents) if word.endswith(searchTarget) ][0]) + 1
		targetLine = fileContents[targetLineNumber]

		print "Target string found at line: " + str(targetLineNumber - 1)

		leadingSpaces = re.match(r'(\W+)', targetLine).group(1)

		print "Adding SMTP fix lines to mail_stub.py"
		fileContents.insert(targetLineNumber, leadingSpaces + '# SMTP FIX END\n')
		fileContents.insert(targetLineNumber, leadingSpaces + 'smtp.ehlo()\n')	
		fileContents.insert(targetLineNumber, leadingSpaces + 'smtp.starttls()\n')
		fileContents.insert(targetLineNumber, leadingSpaces + 'smtp.ehlo()\n')
		fileContents.insert(targetLineNumber, leadingSpaces + '# SMTP FIX BEGIN\n')

		f = open('google/appengine/api/mail_stub.py', "w")
		f.writelines(fileContents)
		f.close()
	else:
		firstArgument = sys.argv[1]

		if firstArgument == "--help" or firstArgument == "-h":
			print "To install:"
			print "'python fixsmtp.py' or 'chmod +x fixsmtp.py; ./fixsmtp' (without quotes)"
			print "To remove:"
			print "'python fixsmtp.py undo' or 'chmod +x fixsmtp.py; ./fixsmtp undo' (without quotes)"
		elif firstArgument == "undo":

			f = open('google/appengine/api/mail_stub.py', 'r')
			fileContents = f.readlines()
			f.close()

			if [ i for i, word in enumerate(fileContents) if word.endswith(undoTarget) ] == []:
				print "Aborting. SMTP path already removed."
				return

			targetLineNumber = int([ i for i, word in enumerate(fileContents) if word.endswith(undoTarget) ][0])
			print "Target string found at line: " + str(targetLineNumber - 1)

			print "Removing SMTP fix lines to mail_stub.py"
			del fileContents[targetLineNumber:targetLineNumber + 5]

			f = open('google/appengine/api/mail_stub.py', "w")
			f.writelines(fileContents)
			f.close()
		else:
			print "Invalid command. Use --help or -h for help."

if  __name__ =='__main__':
	main()