import urllib


BLOCK=8
cipher="XiFnKGRM67n53Tf%2BZ3yyQa2iR%2FGM%2FStB"
cipher = urllib.unquote(cipher).decode('utf8') 

print cipher

cipher_hex=cipher.decode('base64').encode('hex')

p1 = cipher_hex[:-BLOCK-2]
p2 = cipher_hex[-BLOCK:]
a=[]



print cipher_hex
print p1, '', p2, '\n'

with open('c.txt', 'wb') as f:
    for i in xrange(0,256):
        new_cipher = (p1+chr(i).encode('hex') + p2).decode('hex').encode('base64').replace('\n','')
        f.write(urllib.quote_plus(new_cipher)+'\n')
        

