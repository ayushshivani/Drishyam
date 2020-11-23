# Introduction

The script generate RSA public private key pairs using Crypto library in python and save it to separate CSVs based on the email of the user.

Three CSV files are generated 
- public_keys.csv : Contains only the public keys.
- private_keys.csv : Contains only the private keys.
- all_pairs.csv : Contains both the public and its corresponding private key.

[DEMO VIDEO](https://www.youtube.com/watch?v=g8GoDeEph7U&list=PLibW_SCiVev2NjuWV8NMWwCrR3oeFGwLB&index=1)

# Steps

* Download necessary packages

```
pip install -r requirements.txt
```

* Generate the keys and save to csvs.

```
python generate_rsa_pairs_from_emails.py [email]
```

# Author
- Ayush Shivani