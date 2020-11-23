# Introduction

This repo contains all the components of **DRISHYAM**, a platform to conduct privacy preserving clinical trials. The system 
mainly contains three parts 

* System to Generate of RSA Key Pairs
* APIs to get the information from the patients and hash it to blockchain server.
* Mapping keys and information to actual Patients.
* Zero Knowledge proof implementation. ( Schnorr Signature Schemes implementation )

A quick introduction and working of all the parts with demo videos available below.

## How the system works

- Initially when a patient registers for a study( signs up on the platform of CRO ), an authentication using a RSA key pair is generated. In which, a set of public and private key is generated, 
    - the private key is given to the patients 
    - the public key is exposed on the server and is given to us and any organization that wants to randomly send some data to the users

- The data is mapped to the public key and exposed to the user, on matching with the particular private key the data is shared with the user.

- When the user sends the data, the data is send accross the private key, the MD5sum of the data is committed to the blockchain server that is generated as a response to the api request send by the user.

- Whenever the data is changed and hence commited, the hash is different which helps us identify if there was any tampering with the data.

- **TODO** how ZKP comes into the play?

- If some external agency wants to verify the ingrety of the data, the get simply call an api which returns hash of the data and can check it with the hash on the blockchain server, if the hash maps the data is tampered free else not.


## SubSystems

### Generating RSA Keys 

- This sub system helps in generating of the RSA key pair which help in keeping the user identity annonimised.
- The Code and the corresonding readme can be found [here](https://github.com/ayushshivani/MD5_Generation/tree/main/rsa_key_pair_generation).

[DEMO VIDEO](https://www.youtube.com/watch?v=g8GoDeEph7U&list=PLibW_SCiVev2NjuWV8NMWwCrR3oeFGwLB&index=1)

### APIs ( Django App ) 

- This sub system helps in getting data from users and hashing the data. It is also used by third party to check the authenticity of the data at the stage when they want to verify it.

- It contains the the following APIs:
    
    - /api/userdata/insert/ : return md5 hash of the data stored. Also saves to files folder.
    - /api/userdata/testing/ : return md5 hash of the data sent. 

#### To run

- cd django_app
- python manage.py runserver

#### To check the code 

- UserDataEntry in user_data/views.py

[DEMO VIDEO](https://www.youtube.com/watch?v=-lCoHOrTOns&list=PLibW_SCiVev2NjuWV8NMWwCrR3oeFGwLB&index=2)


### BlockChain Server

[DEMO VIDEO](https://www.youtube.com/watch?v=-lCoHOrTOns&list=PLibW_SCiVev2NjuWV8NMWwCrR3oeFGwLB&index=2)

### Zero Knowledge Proofs


## Authors

- Ayush Shivani
- Anurag Jain
- Shaunak Badani