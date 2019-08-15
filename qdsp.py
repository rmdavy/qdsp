#!/usr/bin/python3

#Quick and Dirty SPN Parser
#Takes list of SPNS normally from Impacket output 
#https://github.com/SecureAuthCorp/impacket/blob/master/examples/GetUserSPNs.py
#and parses them
#Outputs SPNS's to individual file with username as filename
#Also outputs a list of usernames, handy for reporting purposes.

import os, signal

def main():
	spnslist = []
	spn_usernames = []

	global DumpFolder

	os.system('clear')
	print("Quick and Dirty SPN Parser - by Rich Davy")
	print("@rd_pentest\n")
	DumpFolder=input ("[*]Please enter folder location of spns.txt file to process: ") or (os.getcwd())

	if os.path.isfile(DumpFolder+"/spns.txt"):
		print("[*]spns.txt file found")
		with open(DumpFolder+"/spns.txt") as fp:
			for line in fp:
				#get start position of username
				unamestart=line.find("$krb5tgs$23$*")+13
				#get end of username
				uanmeend=line.find('$',unamestart)
				#cut out username
				uname=line[unamestart:uanmeend]
				
				#Create a list of SPN usernames
				spn_usernames.append(uname)

				#Write SPN#s out to individual files
				fout=open(DumpFolder+uname+".txt",'w')
				#Write details to file
				fout.write(line)
				#Close handle
				fout.close()

				#Write out all the usernames to file
				fout=open(DumpFolder+"spn_usernames.txt",'w')
				for uname in spn_usernames:
					#Write details to file
					fout.write(uname+"\n")
					#Close handle
				fout.close()
		
		#Print output details
		print("[*]Check "+DumpFolder+" for parsed output.")
		#print list of filenames that have been written
		for u in spn_usernames:
			print(DumpFolder+u+".txt")

		print(DumpFolder+"spn_usernames.txt") 

	else:
		print("[!]spns.txt not found")

#Routine handles Crtl+C
def signal_handler(signal, frame):
	print ("\nCtrl+C pressed.. exiting...")
	sys.exit()

if __name__ == '__main__':
	#Setup Signal handler in case of Ctrl+C
	signal.signal(signal.SIGINT, signal_handler)
	#Call main routine.
	main()
