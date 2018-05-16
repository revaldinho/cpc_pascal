#!/usr/bin/env python3
import getopt, re, sys

## Globals
line_re = re.compile("\s*?(?P<linenum>\d*)(?P<indent>\s+)?(?P<text>.*)?");
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
    print ("\nNAME\n\n  asc2pas.py - ASCII Text to HSP Translation")
    print ("\nUSAGE\n\n  asc2pas.py [-a|--ascii]<filename> [-p|--pascal]<filename> [-l|--addlinenum] [-v|--verbose] [-h|--help]")
    print ("\nMANDATORY SWITCHES\n")
    print ("  -a|--ascii  <filename>   specify input file of ASCII text")
    print ("\nOPTIONAL SWITCHES\n")
    print ("  -p|--pascal  <filename>  specify output filename. If omitted this defaults to the input filename with '.p' appended")
    print ("  -l|--addlinenum          add line numbers")    
    print ("  -v|--verbose             writes information to stdout as translation progresses")
    print ("  -h|--help                show this help message")
    print ("\nEXAMPLES\n")
    print ("  python3 asc2pas.py -a sphere.asc -p sphere.p\n")
    sys.exit(2)

def mainloop( text, verbose, tabmod, addlinenum):
    bytes = bytearray(2); ## reserve first two bytes

    if addlinenum:
        linenum = 10
    comment = False

    for line in text:
        if addlinenum:
            line = "%d %s" % (linenum, line)
        mobj = line_re.match(line.strip())        
        if mobj.groupdict()["linenum"] != '':            
            outtext = bytearray() 

            verbatim = False
            fields = re.split("(\W+)",line.strip()) +  ['','']            
            if verbose:
                print(fields)
            linenum = int(fields[0])

            ## expand tabs
            indent = ""
            for c in fields[1]:
                if c not in (' ', '\t'):
                    break
                indent +=  ' '
                if c == '\t' and (len(indent)%tabmod):
                    indent += ' '* (tabmod - (len(indent) % tabmod))
            indent = indent[:-2] ## strip back one space

            if '(*' in fields[1] or '{' in fields[1]:
                outtext.extend( ord(c) for c in fields[1][fields[1].find('(*'):] )
                comment = True                    
                                
            for word in fields[2:]:
                found = False
                if not verbatim and not comment:
                    for w in tokens:
                        if re.match( w+"([\(\)\s\n;]|$)", word, re.IGNORECASE):
                            found = True
                            outtext.append( tokens[w])
                            break
                if not found:
                    cptr = 0
                    while cptr < len(word):
                        if word[cptr] == "'":
                            verbatim = not verbatim  
                        elif word[cptr] == "(" and cptr<(len(word)-1) and word[cptr+1]=="*":
                            if not verbatim:
                                comment = True
                        elif word[cptr] == "{" :
                            if not verbatim:
                                comment = True                                
                        elif word[cptr] == "*" and cptr<(len(word)-1) and word[cptr+1]==")":
                            if not verbatim:
                                comment = False
                        elif word[cptr] == "}" :
                            if not verbatim:
                                comment = False                                                                
                        if word[cptr]=="\t":
                            outtext.append( ord(' '))
                            outtext.extend( [ord(' ')] * (tabmod - (len(indent) % tabmod)) if ( len(indent)%tabmod) else [] )
                        else:
                            outtext.append( ord(word[cptr]))
                        cptr+=1
            
            if ( verbose ) :
                lineout = ['<%d>'% linenum]
                lineout.append("<%d spaces>" % len(indent))
                lineout.append(''.join( [ chr(c) if c<128 else "[%s]"%reverse_lookup[c] for c in outtext]))
                lineout.append('<0xOD>')
                print(line.strip())
                print(lineout)

            bytes.extend( [ linenum & 0xFF, linenum // 256 ] )
            bytes.append( len(indent))
            bytes.extend(  c for c in outtext)
            bytes.append(0x0d)
            if addlinenum:
                linenum += 10

    ## First two bytes are the number of 0x80 byte segments required (and starting with 1)
    bytes[0] = len(bytes) % 0x80
    bytes[1] = (len(bytes) // 0x80) + 1
    ## Pad out to the end of the current segment at the end of the binary
    while (len(bytes) % 0x80):
        bytes.append(0x00)
    ## Add two null bytes and a soft end-of-file marker
    bytes.append(0x00)
    bytes.append(0x00)            
    bytes.append(0x1A)    
            
    return (bytes)

if __name__ == "__main__":

    infile = ""
    outfile = ""
    verbose = False
    tabmod = 4
    addlinenum = False

    try:
        opts, args = getopt.getopt( sys.argv[1:], "a:p:t:lvh", ["ascii=","pascal=","tab","addlinenum","verbose","help"])
    except getopt.GetoptError:
        showUsageAndExit()
        
    for opt, arg in opts:
        if opt in ( "-a", "--ascii" ) :
            infile = arg
        if opt in ( "-p", "--pascal" ) :
            outfile = arg
        if opt in ( "-v", "--verbose" ) :
            verbose = True        
        if opt in ( "-l", "--addlinenum" ) :
            addlinenum = True        
        if opt in ( "-t", "--tab" ) :
            tabmod = int(arg)
        if opt in ( "-h","--help" ) :            
            showUsageAndExit()

    if infile == "":
        showUsageAndExit()        
    elif outfile == "":
        outfile = infile + ".p"

    with open(infile, "r") as f:
        text = f.readlines()

    bytes = mainloop( text, verbose, tabmod, addlinenum ) 

    with open(outfile,"wb") as f:
        f.write(bytes)
