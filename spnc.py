#!/usr/bin/python

from bs4 import BeautifulSoup
import argparse

#Define list which we'll use to write to file
output = []

try:
	#Get file to parse from the command line
	parser = argparse.ArgumentParser()
	parser.add_argument("--spnfile", help="list of cracked spns to parse")
	#Add option to be able to output result to csv file
	parser.add_argument("--output", help="save output to csv file", type=str, default="", required=False)

	args = parser.parse_args()

	#Display banner
	print("\n[*] Hashcat SPN Parser")
	print("[*] Richard Davy, ECSC plc - 2020\n")

	#Read in file to parse
	with open(args.spnfile, 'r') as f:
		contents = f.read().splitlines()

	#If we're not outputing to file display results to screen
	if args.output=="":
		print("Username Password")
	
	#Add titles to our list
	output.append("Username,Password")

	for c in contents:
		startchar=c.find('*')+1
		endchar=c[startchar:].find('$')

		cusername=(c[startchar:(startchar+endchar)])

		delim=c.find(':')
		cpassword=c[(delim+1):]

		if args.output=="":
			print(cusername+" "+cpassword)
		
		output.append(cusername+","+cpassword)

	#See if we're outputting to file
	if args.output!="":
		try:
			#Open file handler
			with open(args.output,'w') as result_file:
				#Iterate our list
				for r in output:
					#Write line
					result_file.write(r + "\n")
				#Close file handle
				result_file.close()
				#Print msg to screen
				print("[*] Output has been written to "+ args.output)
		#Friendly Error Handler code
		except Exception as e:
			print("[!] Doh... Well that didn't work as expected!")
			print("[!] type error: " + str(e))
#Friendly Error Handler code
except Exception as e:
	print("[!] Doh... Well that didn't work as expected!")
	print("[!] type error: " + str(e))