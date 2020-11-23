from Crypto.PublicKey import RSA
from Crypto import Random
import pandas as pd
import numpy as np
import os,sys
import re


def newkeys(keysize):
    '''
    Generate a new pair of public private key
    '''
    random_generator = Random.new().read
    new_key = RSA.generate(keysize, random_generator)   
    public_key = new_key.publickey().exportKey("PEM") 
    private_key = new_key.exportKey("PEM") 
 
    return public_key, private_key


if __name__ == '__main__':

    '''
    Generate RSA for the email and store it in two files such as
    email_public.pem and email_private.pem
    '''
    email = sys.argv[1]
    email = email.replace('.','_')
    pub_keys = []
    priv_keys = []
    print("Generatin key for email {0}\r".format(email),end="")
    pub,pri = newkeys(2048)
    
    try:
        os.mkdir('files')
    except:
        pass
    
    f = open('files/'+email+'_public.pem','wb+')
    f.write(pub)
    f.close()

    f = open('files/'+email+'_private.pem','wb+')
    f.write(pri)
    f.close()

    

        
    
