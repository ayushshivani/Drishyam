# Introduction

The script generate RSA public private key pairs using Crypto library in python and save it to separate CSVs.

Three CSV files are generated 
- public_keys.csv : Contains only the public keys.
- private_keys.csv : Contains only the private keys.
- all_pairs.csv : Contains both the public and its corresponding private key.

# Steps

* Download necessary packages

```
pip install -r requirements.txt
```

* Generate the keys and save to csvs.

```
python generate_rsa_pairs.py
```

# Author
- Ayush Shivani