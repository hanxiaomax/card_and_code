import time
import hashlib

signature = raw_input("signature  :")
timestamp = raw_input("timestamp  :")
nonce = raw_input("nonce  :")
echostr = raw_input("echostr  :")
token = "shenlian"

s = [timestamp,nonce,token]
s.sort()
s = "".join(s)
print "signature:",signature
print "sha1:",hashlib.sha1(s).hexdigest()
