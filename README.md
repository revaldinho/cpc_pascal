# cpc_pascal
Utilities and demo programs for Pascal on the Amstrad CPC Computers

Working With HiSoft Pascal 4T and ASCII Files
=============================================

HiSoft Pascal 4T has its own line editor and stores all files in a binary format to
save space. Unfortunately the line editor is very painful to use and there is no option
to import or export ASCII files from another text editor.

In fact, a good deal of the file content is actually ASCII text, but reserved words
are tokenized and indenting spaces are compressed into a single byte per line. Actual
compaction depends a lot on how much indenting is used, but in general the resulting
binary files are around 25% smaller than the ASCII equivalent.

The CPM version was provided with a couple of utilities to convert files to and from 
ASCII text: FROMAMS.COM, TOAMS.COM. These aren't greatly convenient to use with the
AMSDOS version or if editing on a modern machine and storing files on .dsk images
for use with emulators or USB/SD card systems.

The two utilities here written in Python3 do the same task on Linux or MacOS:

  o asc2pas.py
  o pas2asc.py

Both will translate from the AMSDOS file format to and from plain ASCII text. Optionally
both and strip or add line numbers (necessary only for Hisoft's built in editor rather than
the language itself) so that syntax colouring can be used in Emacs or other editors.


ASCII to HiSoft Pascal 4T Translation
=====================================

```
NAME

  asc2pas.py - ASCII Text to HSP Translation

USAGE

  asc2pas.py [-a|--ascii]<filename> [-p|--pascal]<filename> [-l|--addlinenum] [-v|--verbose] [-h|--help]

MANDATORY SWITCHES

  -a|--ascii  <filename>   specify input file of ASCII text

OPTIONAL SWITCHES

  -p|--pascal  <filename>  specify output filename. If omitted this defaults to the input filename with '.p' appended
  -l|--addlinenum          add line numbers
  -v|--verbose             writes information to stdout as translation progresses
  -h|--help                show this help message

EXAMPLES

  python3 asc2pas.py -a sphere.asc -p sphere.p
```

Hisoft Pascal 4T to ASCII Translation
=====================================


```
NAME

  pas2asc.py - ASCII Text to HiSoft Pascal 4T Translation

USAGE

  pas2asc.py [-a|--ascii]<filename> [-p|--pascal]<filename> [-n|--nolinenum][-v|--verbose] [-h|--help]

MANDATORY SWITCHES

  -p|--pascal  <filename>  specify input file

OPTIONAL SWITCHES

  -a|--ascii  <filename>   specify output filename. If omitted this defaults to the input filename with '.asc' appended
  -n|--nolinenum           remove line numbers
  -v|--verbose             writes information to stdout as translation progresses
  -h|--help                show this help message

EXAMPLES

  python3 pas2asc.py -a sphere.asc -p sphere.p -n
  
```


Example Session
===============

Create the Sphere demo program in your favourite Linux/MacOS editor


```
(* Sphere or Woolball demo after Acornsoft BASIC original *)

program sphere;
const
  xo = 300;
  yo = 200;
  sc = 200;
var
  n, x, y : integer;
  i : real;


procedure scrsetmode(mode : integer);
begin
   ra:=chr(mode);
   user(#bc0e)
end;

                            
procedure gramoveabs(x,y :integer );
begin
   rde:=x; rhl:=y;
   user(#bbc0)
end;

procedure gralineabs(x,y :integer );
begin
   rde:=x; rhl:=y;
   user(#bbf6)
end;

procedure graclearwindow;
begin
   user(#bbdb)
end;

procedure klsettime;
begin
   rde:=0; rhl:=0;
   user(#bd10)
end;

begin
  scrsetmode(0);
  graclearwindow;
  gramoveabs(xo, yo);
  for n := 0 to 504 do
    begin
      i := n * 0.25;
      x := round(sc * sin(i));
      y := round(sc * cos(i) * sin(i*0.95));
      gralineabs(x+xo,y+yo);
    end
end.
```

Save it as sphere.p

Convert it from ASCII to Hisoft Pascal format, adding line numbers and then pop it oon a fresh DSK image

```
python asc2pas.py -a sphere.p -p sphere.hsp -l
iDSK new.dsk -n
iDSK new.dsk -i sphere.hsp
```

Fire up Hisoft Pascal on an emulator or better still real hardware and mount the disk image. Then compile and run

```
>g,,sphere.hsp
>C
>R
```

HiSoft Pascal 4T File Format
============================

The file has the following general format

  Section                | Comment
  -----------------------|-----------------------------------------------------
  File size              | 2 byte file size
  [line][line]..[line]   | Program body made up of multiple line sections
  end of program         | 2 byte end of program marker
  padding                | variable number of bytes to pad out to multiple of 128 bytes
  end of file            | 3 byte end of file

File Size
=========

This is a two byte field describing the total number of bytes in the file
in 128byte sections. 

The low byte (the first byte) holds the number of bytes in the final section. 

The high byte (second byte) holds the number of 128 byte sections in the file, 
numbered starting at 1.

```
  byte0 = file_len MOD 128
  byte1 = (file_len DIV 128) + 1
```
Line
====

Each line entry starts with a two byte field for the line number and ends 
with an 0x1D character to mark the end of line. 

  Byte | Field                       | Comment
  -----|-----------------------------|--------------------------------
  0    | linenum lo byte             | low byte = linenum MOD 256
  1    | linenum hi byte             | high byte = linenum DIV 256
  2    | number of spaces indentation| one byte
  3..N | line text                   | multiple bytes
  N+1  | 0x0d                        | end of line marker

A single space is always assumed between line number and the first character of the
line text, so the number of spaces in the field here is actually one less than will
be shown on screen in the Hisoft editor.

Line text
=========

Line text is mainly simple ASCII characters, except that reserved words are tokenized
using the following table.

   Keyword  | Token   | Keyword     | Token  | Keyword      |  Token |  Keyword     | Token
  ----------|---------|-------------|--------|--------------|--------|--------------|---------   
  PROGRAM   |	0x81  | VAR	    |	0x8A | REPEAT	    |	0x93 |  ARRAY	    |	0x9C                     
  DIV	    |	0x82  | OF	    |	0x8B | CASE	    |	0x94 |  FORWARD	    |	0x9D                     
  CONST	    |	0x83  | TO	    |	0x8C | WHILE	    |	0x95 |	RECORD	    |	0x9E
  PROCEDURE |	0x84  | DOWNTO	    |	0x8D | FOR	    |	0x96 |	TYPE	    |	0x9F
  FUNCTION  |	0x85  | THEN	    |	0x8E | IF	    |	0x97 |	IN    	    |	0xA0
  NOT	    |	0x86  | UNTIL	    |	0x8F | BEGIN	    |	0x98 |	LABEL	    |	0xA1
  OR	    |	0x87  | END	    |	0x90 | WITH	    |	0x99 |  NIL	    |	0xA2
  AND	    |	0x88  | DO	    |	0x91 | GOTO	    |	0x9A |  PACKED	    |	0xA3
  MOD	    |	0x89  | ELSE	    |	0x92 | SET	    |	0x9B | 	            |
                                                                             	
Reserved words in comments or quotes are not tokenized.

End of Program
==============

The end of program marker is made up of two zero bytes. Effectively these are a 
line number of zero as the parser progresses past the last actual line of program.

Padding
=======

Each file is padded out to a multiple of 128 bytes. The actual padding character 
seems not to matter, but zeroes are used by asc2pas.py.

End of file
===========

After the padding, three more bytes are added to mark the end of file. If the 
file (including padding) is 128 bytes long, then these will be bytes 129,130 
and 131. The bytes are 
```
[0x00] [0x00] [0x1A].
```
