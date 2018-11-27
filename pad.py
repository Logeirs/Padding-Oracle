import urllib


BLOCK=8
s="XiFnKGRM67n53Tf%2BZ3yyQa2iR%2FGM%2FStB"
s = urllib.unquote(s).decode('utf8') 

print s

sd=s.decode('base64').encode('hex')

p1 = sd[:-BLOCK-2]
p2 = sd[-BLOCK:]
a=[]



print sd
print p1, '', p2, '\n'

with open('c.txt', 'wb') as f:
    for i in xrange(0,256):
        newc = (p1+chr(i).encode('hex') + p2).decode('hex').encode('base64').replace('\n','')
        f.write(urllib.quote_plus(newc)+'\n')
        

