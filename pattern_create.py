# Base on Pattern_Creator.rb
# Author : peternguyen

#Support debugging in GDB easier

import sys
import getopt,string
from struct import * 

lower = string.ascii_lowercase
upper = string.ascii_uppercase
digits = string.digits

def create_pattern(size):
	pattern = ''
	j = k = l = 0
	for i in xrange(0,size,3):
		if(l == len(digits)):
			l = 0
			k += 1
			if(k == len(lower)):
				k = 0
				j += 1
				if(j == len(upper)):
					j = 0
		pattern += upper[j]+lower[k]+digits[l]
		l += 1
	return pattern

def calculateEIP(pattern_str,str_input,mode=1):
	#calculate eip offset
	#Mode 1: input 0x414141414
	#Mode 0: input str
	if mode:
		key = pack('<I',int(str_input,16))
	else:
		key = str_input
	if pattern_str.rfind(key) > -1:
		offset = len(pattern_str[:pattern_str.rfind(key)])
	else:
		offset = -1
	return offset

def usage():
	print 'Usage : %s <length_pattern> ' % sys.argv[0]
	print '\t - Use in GDB use option -g'
	print '\t - If You Want Calculate junk size use : '
	print '\t\t %s 2000 -b 0x68423768(for byte) or -s At05(for string)' % sys.argv[0]

def main():
	#call main program
	pattern_len = 0#default len
	try:
		opts,args = getopt.getopt(sys.argv[1:],'l:b:s:xvh')
	except getopt.GetoptError as err:
		usage()
		print str(err)
		sys.exit(1)
	for option,variable in opts:
		if option == '-l':
			pattern_len = int(variable)
		elif option == '-v':# use this option in gdb
			if pattern_len:
				sys.stdout.write(create_pattern(pattern_len))
			else:
				print '[!] Error len pattern = 0'
		elif option == '-x':# use this option in terminal
			if pattern_len:
				print '-> Pattern : %s' % create_pattern(pattern_len)
			else:
				print '[!] Error len pattern = 0'
		elif option == '-b':#input byte to calculate offset EIP
			if pattern_len:
				print '-> EIP offset : %d' % calculateEIP(create_pattern(pattern_len),variable)
			else:
				print '[!] Error len pattern = 0'
		elif option == '-s':
			if pattern_len:
				print '-> EIP offset : %d' % calculateEIP(create_pattern(pattern_len),variable,mode=0)
			else:
				print '[!] Error len pattern = 0'
		elif option == '-h':
			usage()
		else:
			assert False, "unhandled option"
			sys.exit(0)
if __name__ == '__main__':
	main()