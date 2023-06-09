################################################################################
##
## This library is free software; you can redistribute it and/or
## modify it under the terms of the GNU Lesser General Public
## License as published by the Free Software Foundation; either
## version 2.1 of the License, or (at your option) any later version.
## 
## This library is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## Lesser General Public License for more details.
## 
## You should have received a copy of the GNU Lesser General Public
## License along with this library; if not, write to the Free Software
## Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
##
## (C) Copyrights Dr. Michel F. Sanner and TSRI 2016
##
################################################################################

#!/usr/bin/env python

# Ununicode.toascii(): convert perfectly good unicode or utf-8
# strings to puny pathetic plain ascii.

# Copyright 2009 by Akkana Peck.
# Please reuse, modify and otherwise enjoy under the terms
# of the GNU Public License v2 or, at your option, a later version.

import unicodedata
import types

def toascii(line, errfilename = None, in_encoding = 'utf-8') :
    """
    Convert a line to plain ascii, making reasonable substitutions
    for accented characters, curly quotes, emdashes etc.
    Unknown characters will be backslash replaced, and
    can also be appended, with context, to an error file.
    Characters in the error file can then be added to the
    xlate table so they will be handled next time.

    Arguments:
    line:        a string or unicode string to be converted to ASCII.
    errfilename: a place to log unknown characters.
    in_encoding: the encoding used if line is a string
    (not used for unicode input).
    """

    # Define the error file. In Python 2.6, the sub-function
    # log_error can see a list but not a scalar variable.
    # So the file pointer has to be errfile[0], not just errfile.
    errfile = [ None, errfilename ]

    # Log an error, giving some context around the problematic area:
    def log_error(uni, start, end, msg="error") :
        contextsize = 15
        if errfile[0] == None :
            if errfilename == None :
                return
            errfile[0] = open(errfile[1], "a")
        unilen = len(uni)
        strstart = start -contextsize
        if strstart < 0 : strstart = 0
        strend = end + contextsize
        if strend > unilen : strend = unilen
        print(msg, ":", \
            uni[strstart:strend].encode('ascii', 'backslashreplace'), file=errfile[0])
# [ u for u in uni[start:end]]

    output = ''

    # If it's a string, decode it to Unicode.
    # If it's already unicode, no need to do that.
    if type(line) == bytes :
        if in_encoding == '' :
            in_encoding = 'utf-8'
            # Slower but safer: try decoding with utf-8 then iso8859-15
        line = line.decode(in_encoding, 'replace')
    elif type(line) != str :
        return "toascii needs either string or unicode, not" + str(type(line))

    normalized = unicodedata.normalize('NFKD', line)
    while normalized != None :
        try :
            output += str(normalized.encode('ascii', 'strict'), 'utf-8')
            # or ignore, replace, etc.
            normalized = None
            break

        except UnicodeEncodeError as e :
            # At this point, e has these useful attributes:
            # e.encoding: 'ascii'
            # e.args: (encoding, unicode, start, end?, message)
            # e.g.    ('ascii', u'\xff', 0, 1, 'ordinal not in range(128)')
            #print e
            #print "\nargs:", e.args
            #print "Error encoding to ascii:", e.args[2], e.args[3]

            # Now turn it into something we can view.

            # Some values unicodedata.normalize().encode doesn't grok:
            # Add to this table as you see characters showing up in
            # your error file.
            xlate = {
                # A few multi-char UTF-8 strings -- some sites, like
                # BBC, persist in throwing in UTF-8 quotes even though
                # they're using another charset like 8859-1.
                '\x80\x93' : '-',  # UTF-8 endash
                '\x80\x94' : '--', # UTF-8 emdash
                '\x80\x98' : '`',  # UTF-8 left single quote
                '\x80\x99' : '\'', # UTF-8 apostrophe
                # Previous line isn't catching the zillions of hits on BBC,
                # so let's try it without the u prefix.
                # If afterward we get \x80\x9d and \x80\x93
                # but no more \x80\x99, then probably none of these
                # should have the u prefix.
                #'\x80\x99'  : '\'', # UTF-8 apostrophe
                '\x80\x9c' : '"',  # UTF-8 left double quote
                '\x80\x9d' : '"',  # UTF-8 right double quote
                '\x80\xa2' : '*',  # UTF-8 bullet

                # Combining forms.
                # If you don't want to see them (e.g. prefer to see
                # &ntilde; as n rather than n~), replace the matches
                # with '' instead of the characters here.
                '\u0300' : '`',    # Combining grave accent
                '\u0301' : '\'',   # Combining acute accent
                '\u0302' : '^',    # Combining circumflex
                '\u0303' : '~',    # Combining tilde
                '\u0304' : '-',    # Combining overscore
                '\u0306' : '^',    # Combining breve
                '\u0308' : 'e',    # Combining diaresis
                '\u030a' : '^',    # Combining ring above
                '\u030c' : '^',    # Combining caron
                '\u0327' : ',',    # Combining cedilla?

                # Unicode symbols
                '\u0131' : 'i',   # unicode dotless i
                '\u03bc' : '(u)', # mu
                '\u200b' : '',    # zero-width space (zwsp)
                '\u2010' : '-',   # hyphen
                '\u2013' : '-',   # endash
                '\u2014' : '--',  # emdash
                '\u2015' : '--',  # horizontal bar
                '\u2016' : '||',  # double vertical line
                '\u2018' : '`',   # left single quote
                '\u2019' : '\'',  # right single quote
                '\u201a' : ',',   # single low-9 quot. mark (mistaken comma?)
                '\u201c' : '"',   # left double quote
                '\u201d' : '"',   # right double quote
                '\u201e' : '"',   # double low-9 quotation mark
                '\u2020' : '*',   # dagger
                '\u2021' : '*',   # double dagger
                '\u2022' : '*',   # bullet
                '\u2028' : '_',   # "line separator" -- thereg uses as a space
                '\u2032' : '\'',  # prime
                '\u2039' : '&lt;', # left arrow
                '\u203a' : '&gt;', # right arrow
                '\u2044' : '/',   # "fraction slash"
                '\u2190' : '<-',  # left arrow
                '\u2191' : '^',   # up arrow
                '\u2192' : '->',  # right arrow
                '\u2193' : 'v',   # down arrow
                '\u20ac' : '(EUR)',  # Euro symbol
                '\u2192' : '-&gt;',  # right arrow
                '\u25cf' : '*',   # black filled circle
                '\ufeff' : '',    # Merc uses it, firefox displays nothing
                '\ufffd' : '\'',  # Yet another apostrophe

                # Characters that oddly don't get translated to unicode:
                '\x85' : '...',    # BBC uses this for ellipsis, though it's
                                    #   really a Unicode 3.0 newline [NEL]
                '\x92' : '\'',     # yet another apostrophe
                '\x93' : '"',      # yet another open quote
                '\x94' : '"',      # yet another close quote
                '\x96' : '-',      # yet another endash
                '\xa1' : '!',      # upside down !
                '\xa2' : '(c)',    # cents
                '\xa3' : '(L)',    # UK pounds
                '\xa5' : '(Y)',    # Yen
                '\xa7' : '(sect)', # Section sign
                '\xa8' : ':',      # umlaut
                '\xa9' : '-',      # maybe an emdash?
                '\xab' : '<<',     # left German quote
                '\xad' : '-',      # emdash
                '\xae' : '(R)',    # Registered trademark
                '\xb0' : '^',      # degree
                '\xb1' : '+/1',    # plus/minus
                '\xb6' : 'PP',     # paragraph
                '\xb7' : '*',      # mid dot
                '\xbb' : '>>',     # left German quote
                '\xbf' : '?',      # Spanish upside-down question mark
                '\xc6' : 'ae',     # ae ligature
                '\xd7' : 'x',      # math, times
                '\xd8' : 'O/',     # O-slash
                '\xdf' : 'ss',     # German ss ligature (like a beta)
                '\xf8' : 'o/',     # o slash
                }

            # Encode the first part of the string, up to the error point.
            # Use backslashreplace even though there shouldn't be any errs.
            s = normalized[0:e.args[2]].encode('ascii', 'backslashreplace')

            # e.args[3] is supposedly the end point, but encode() isn't
            # smart enough to notice most multi-char sequences, so
            # in practice it's always e.args[2]+1.
            bad_u = normalized[e.args[2]:]
            if bad_u[0] in xlate :
                s += xlate[bad_u[0:1]]
                normalized = normalized[e.args[2] + 1 : ]
            else :
                s += bad_u[0].encode('ascii', 'backslashreplace')
                log_error(e.args[1], e.args[2], e.args[3], e.args[4])
                normalized = normalized[e.args[3]:]

            # print with no newline OR space:
            output += s
            continue

    if errfile[0] != None :
        errfile[0].close()
    return output

#
# Main -- read the config file and loop over sites.
#
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 :
        fp = open(sys.argv[1], "r")
    else :
        fp = sys.stdin
    while True :
        line = fp.readline()
        if not line : break

        # Use: line = ununicode.toascii(line) when calling externally
        line = toascii(line)
        sys.stdout.write(line)
