from Crypto.PublicKey import RSA
from Crypto import Random
import pandas as pd
import numpy as np
import os


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

    # Generate n public private pairs of RSA keys
    no_of_keys = 100
    pub_keys = []
    priv_keys = []
    for i in range(no_of_keys):
        print("Generatin key number {0}\r".format(i),end="")
        pub,pri = newkeys(2048)
        pub_keys.append(pub)
        priv_keys.append(pri)


    pub_keys_df = pd.DataFrame(pub_keys,columns=['public_keys'])
    priv_keys_df = pd.DataFrame(priv_keys,columns=['private_keys'])
    
    both_keys_df = pd.DataFrame(columns=['public_keys','private_keys'])
    both_keys_df['public_keys'] = pub_keys_df['public_keys']
    both_keys_df['private_keys'] =priv_keys_df['private_keys']
    
    # Save to CSVs
    print("Generated keys, writing to csv ...")
    os.system('mkdir csv')
    pub_keys_df.to_csv('csv/public_keys.csv',index=False)
    priv_keys_df.to_csv('csv/private_keys.csv',index=False)
    both_keys_df.to_csv('csv/all_pair.csv',index=False)
    print("Wrote to csvs.")


    

        
    
