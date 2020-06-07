sry, i can't do fancy symbol art

##############################################
#                                            #
# (insert fancy symbol art for my tool here) #
#                                            #
##############################################

This tool is designed to encrypt the vigenere chiffre and decrypt it without a key.
##############################################
Dependencies:
-decrypt_vigenere_known_d.py
-find_keylength.py
##############################################
Usage: ./vigenere.py <args>
----------------------------------------------
Enryption: ./vigenere.py <in> <out> <m> <key>
Example: ./vigenere.py files/lorem.txt files/encrypted-lorem-5.txt 128 5 10 7

<in>: Input file where the text to be encrypted is saved
<out>: Output file where the encrypted text will be saved
<m>: Length of the alphabet. The symbols that can be decrypted and encrypted will be the first m ASCII-symbols. Also, the keyspace will be the first m ASCII-symbols.
<key>: The key used for encryption seperated by spaces
----------------------------------------------
Decryption: ./vigenere.py -d <in> <lang> <m>
Example: ./vigenere.py -d files/encrypted-lorem-5.txt files/lorem.txt 128

<in>, <m>: same as in encryption (1 above)
<lang>: text file that will be used as a reference for the empirical probability of each character
##############################################
Thank you for reading the full README.txt - have fun using the tool!