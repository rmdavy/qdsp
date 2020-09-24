#!/usr/bin/python

import argparse, os

#Define list which we'll use to write to file
output = []
listgroupmembers = []
listUserDetails = []

try:
	#Get file to parse from the command line
	parser = argparse.ArgumentParser()
	parser.add_argument("--spnfile", help="list of cracked spns to parse")
	#Add option to be able to output result to csv file
	parser.add_argument("--output", help="save output to csv file", type=str, default="", required=False)
	#Add option to retrieve group membership for cracked SPN users
	parser.add_argument("--groupmembers", help="path to adrecon GroupMembers.csv", type=str, default="", required=False)

	args = parser.parse_args()

	#Display banner
	print("\n[*] Hashcat SPN Parser")
	print("[*] Richard Davy, ECSC plc - 2020\n")

	#Read in file to parse
	with open(args.spnfile, 'r') as f:
		contents = f.read().splitlines()

	#Read in group membership details if groupmembers argument is not empty
	if args.groupmembers!="":
		#Check specified file exists
		if os.path.isfile(args.groupmembers):
			#Open file and read in details into list
			with open(args.groupmembers, 'r') as f:
				for line in f:
					usernamegroup=line.split(",")[0][1:-1]
					#print(usernamegroup)
					#Parse username
					username=line.split(",")[1][1:-1]
					#print(username)

					listgroupmembers.append(usernamegroup+":"+username)

	#If we're not outputing to file display results to screen
	if args.output=="":
		if args.groupmembers!="":
			print("Group Membership:Username:Password:Masked Password")
		else:
			print("Username:Password:Masked Password")
	else:
		if args.groupmembers!="":
			output.append("Group Membership,Username,Password,Masked Password")
		else:
			output.append("Username,Password,Masked Password")

	#Iternate through SPN's in file
	for c in contents:
		#Get username from string
		cusername=c.split("$")[3][1:]
		#Get cracked password from string
		cpassword=c.split(":")[1]
		#Mask the password
		maskedpw=(cpassword[:1]+("*"*(len(cpassword)-2))+cpassword[-1:])
		
		#Check to see if groupmembers flag has been used
		if args.groupmembers!="":
			#Iterate through groupmembers
			for grpmem in listgroupmembers:
				#If SPN username and username from groupmembers file match
				if cusername==grpmem.split(":")[1]:
					#Add to list groupmembership, username, password and masked password
					listUserDetails.append(grpmem.split(":")[0]+":"+cusername+":"+cpassword+":"+maskedpw)

		else:
			#Add to list username, password and masked password
			listUserDetails.append(cusername+":"+cpassword+":"+maskedpw)

	#Sort List
	listUserDetails.sort()
	
	#If not outputing to CSV print details of users to screen
	if args.output=="":
		for ud in listUserDetails:
			print(ud)

	#See if we're outputting to file
	if args.output!="":
		try:
			#Add userdetails to the output list
			output.extend(listUserDetails)
			
			#Open file handler
			with open(args.output,'w') as result_file:
				#Iterate our list
				for r in output:
					#Write line to file, changing : delimiter for , so that we're good for csv output
					result_file.write(r.replace(":",",") + "\n")
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