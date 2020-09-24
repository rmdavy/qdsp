#!/usr/bin/python

import argparse

#Define list which we'll use to write to file
output = []

try:
	#Get file to parse from the command line
	parser = argparse.ArgumentParser()
	parser.add_argument("--spnfile", help="list of spns to parse")
	#Add option to be able to output results to folder
	parser.add_argument("--privusers", help="list of privileged user accounts", type=str, default="", required=False)

	args = parser.parse_args()

	#Display banner
	print("\n[*] Quick and Dirty SPN Parser")
	print("[*] Richard Davy, ECSC plc - 2020\n")

	#Read in file to parse
	with open(args.spnfile, 'r') as f:
		contents = f.read().splitlines()

	print("[*] Number of SPN's found is ",len(contents))
	print("[*] Parsed files will be written to /tmp/\n")

	#
	#Parse all the SPN's and write each one individually to file
	#
	for c in contents:
		#Get username from string
		cusername=c.split("$")[3][1:]
				
		try:
			#Open file handler
			with open("/tmp/"+cusername+".txt",'w') as result_file:
				#Write line
				#print(c)
				result_file.write(c + "\n")
				#Close file handle
				result_file.close()
				#Print msg to screen
				print("[*] Output has been written to "+ "/tmp/"+cusername+".txt")
		#Friendly Error Handler code
		except Exception as e:
			print("[!] Doh... Well that didn't work as expected!")
			print("[!] type error: " + str(e))

	#
	#Write all the usernames to file
	#
	try:
		#Open file handler
		with open("/tmp/spn_usernames.txt",'w') as result_file:
			#Write line
			#print(c)
			for c in contents:
				#Get username from string
				cusername=c.split("$")[3][1:]
				result_file.write(cusername + "\n")
			
			#Close file handle
			result_file.close()
			#Print msg to screen
			print("[*] List of usernames has been written to "+ "/tmp/spn_usernames.txt\n")
	#Friendly Error Handler code
	except Exception as e:
		print("[!] Doh... Well that didn't work as expected!")
		print("[!] type error: " + str(e))


#Friendly Error Handler code
except Exception as e:
	print("[!] Doh... Well that didn't work as expected!")
	print("[!] type error: " + str(e))