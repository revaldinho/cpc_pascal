#!/usr/bin/env python3

import getopt, sys

tokens = {
	"PROGRAM":0x81,
	"DIV":0x82,
	"CONST":0x83,
	"PROCEDURE":0x84,
	"FUNCTION":0x85,
	"NOT":0x86,
	"OR":0x87,
	"AND":0x88,
	"MOD":0x89,
	"VAR":0x8A,
	"OF":0x8B,
	"TO":0x8C,
	"DOWNTO":0x8D,
	"THEN":0x8E,
	"UNTIL":0x8F,
	"END":0x90,    
	"DO":0x91,
	"ELSE":0x92,
	"REPEAT":0x93,
	"CASE":0x94,
	"WHILE":0x95,
	"FOR":0x96,
	"IF":0x97,
	"BEGIN":0x98,
	"WITH":0x99,
	"GOTO":0x9A,
	"SET":0x9B,
	"ARRAY":0x9C,
	"FORWARD":0x9D,
	"RECORD":0x9E,
	"TYPE":0x9F,
	"IN":0xA0,
	"LABEL":0xA1,
	"NIL":0xA2,
	"PACKED":0xA3 }

reverse_lookup = {}
for w in tokens:
    reverse_lookup[tokens[w]] = w

def showUsageAndExit() :
    print ("\nNAME\n\n  pas2asc.py - ASCII Text to HiSoft Pascal 4T Translation")
    print ("\nUSAGE\n\n  pas2asc.py [-a|--ascii]<filename> [-p|--pascal]<filename> [-n|--nolinenum][-v|--verbose] [-h|--help]")
    print ("\nMANDATORY SWITCHES\n")
    print ("  -p|--pascal  <filename>  specify input file")
    print ("\nOPTIONAL SWITCHES\n")
    print ("  -a|--ascii  <filename>   specify output filename. If omitted this defaults to the input filename with '.asc' appended")
    print ("  -n|--nolinenum           remove line numbers")
    print ("  -v|--verbose             writes information to stdout as translation progresses")
    print ("  -h|--help                show this help message")
    print ("\nEXAMPLES\n")
    print ("  python3 pas2asc.py -a sphere.asc -p sphere.p -n\n")
    sys.exit(2)

def mainloop( bytes, striplinenum, verbose ):
    filesize = (bytes[0]+bytes[1]*128)
    if verbose:
        print ("Filesize: %d (0x%02x, 0x%02x)" % (filesize, bytes[0], bytes[1]))
    ptr = 2
    text = []
    while ptr < (min(len(bytes),filesize)-1) :
        linetext = []
        linenum = bytes[ptr]+ bytes[ptr+1]*256
        if linenum == 0:
            break
        indent = bytes[ptr+2]
        ptr+=3
        while bytes[ptr] != 0x0D:
            if bytes[ptr] < 0x80:
                linetext.append(chr(bytes[ptr]))
            else:
                if bytes[ptr] in reverse_lookup:
                    linetext.append(reverse_lookup[bytes[ptr]])
                else:
                    linetext.append("UNKNOWN_KEYWORD")
            ptr+= 1
        ptr+=1
        
        linenumstr = "%d" % linenum if not striplinenum else ""
        if verbose:            
            print ('%s%s%s' %( linenumstr,' '*(indent+(not striplinenum)), ''.join(linetext)))

        text.append( ''.join( [ linenumstr, ' '*(indent+(not striplinenum)), ''.join(linetext), '\n'] ))

    return ''.join(text)


if __name__ == "__main__":

    infile = ""
    outfile = ""
    verbose = False
    striplinenum= False

    try:
        opts, args = getopt.getopt( sys.argv[1:], "a:p:nvh", ["ascii=","pascal=","nolinenum","verbose","help"])
    except getopt.GetoptError:
        showUsageAndExit()
        
    for opt, arg in opts:
        if opt in ( "-a", "--ascii" ) :
            outfile = arg
        if opt in ( "-p", "--pascal" ) :
            infile = arg
        if opt in ( "-n", "--nolinenum" ) :
            striplinenum = True        
        if opt in ( "-v", "--verbose" ) :
            verbose = True        
        if opt in ( "-h","--help" ) :            
            showUsageAndExit()

    if infile == "":
        showUsageAndExit()        
    elif outfile == "":
        outfile = infile + ".asc"

    with open(infile,"rb") as f:
        bytes = f.read(32768)

    text = mainloop( bytes, striplinenum, verbose  ) 

    with open(outfile,"w") as f:
        f.write(text)

