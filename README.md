[![Hits](https://hits.sh/github.com/tingirifistik/Instagram-Password-Encryption.svg?label=views&color=0099ff&labelColor=464646)](https://hits.sh/github.com/tingirifistik/Instagram-Password-Encryption/)

<h2>Installation</h2>

```console
git clone https://github.com/tingirifistik/Instagram-Password-Encryption.git
cd Instagram-Password-Encryption
pip3 install -r requirements.txt
python3 insta_encrypt.py
```

<h3>Syntax</h3>

```python
encrypt_password(password, [version], [key_id], [public_key_hex])
```
<h3>Parameters</h3>

- `password` (str): The password to be encrypted
- `version` (str): The version of the encryption algorithm, default is `10`
- `keyID` (str): The key identifier, default is `143`
- `publicKey` (str): The public key used for encryption, default is `f219393f2381eab7abd6d20130bfa274cc4ffc8b67988da60abeffc88c1b9b15`

 You can find these values at [endpoint](https://www.instagram.com/api/v1/web/data/shared_data/)
 

 ###### Thanks to [this](https://github.com/glizzykingdreko/Instagram-Password-Encryption) repo
