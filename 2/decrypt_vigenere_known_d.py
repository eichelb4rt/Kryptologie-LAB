import numpy as np
import sys

def main():
    input = open(sys.argv[1], "r")
    m = 128 # length of alphabet
    keyspace = range(1,m)
    # get reference for the empirical propability of the chars
    language = get_language("files/lorem.txt", m) # insert any language here
    print(crack_vigenere(input.read(), language, m, keyspace, int(sys.argv[2])))
    input.close()

def crack_vigenere(text: str, language: list, m: int, keyspace: list, d: int, only_key = False):
    # divide text into d columns
    columns_crypt = [""]*d
    for i in range(0, len(text)):
        columns_crypt[i%d] += text[i]
    # return the clear text
    if not only_key:
        columns_clear_text = [""]*d
        for i in range(0,d):
            columns_clear_text[i] = crack_additive(columns_crypt[i], language, m, keyspace)
        clear_text = ""
        for i in range(0, len(text)):
            clear_text += columns_clear_text[i%d][i//d] # convert the columns back into 1 text
        return clear_text
    # return only the keys
    else:
        return [crack_additive(columns_crypt[i], language, m, keyspace, True) for i in range(0,d)]

def crack_additive(text: str, language: list, m:int, keyspace: list, only_key = False):
    # initiate start values for the search for the best fitting key
    max_key = keyspace[0]
    min_delta_ep = 2    # minimum normed difference between the eps: empirical probability vectors have a maximum length of 1, therefore max difference is 2 (sum of eps is <= 1, -> sum of squares is also <= 1, -> sqrt of sum of squares is <= 1)
    for key in keyspace:
        # empirical probability of the chars in a decrypted column (with a guessed key)
        ep = EP(decrypt_additive(text, key, m), m)
        # difference between the empirical probability vectors
        delta_ep = [0]*m
        for j in range(0,m):
            delta_ep[j] = ep[j] - language[j]
        # update best fitting key
        if norm(delta_ep) < min_delta_ep:
            min_delta_ep = norm(delta_ep)
            max_key = key
    if not only_key:   # return the clear text
        return decrypt_additive(text, max_key, m)
    else:   # return only the key
        return max_key

def norm(vector: list):
    sum = 0
    for x in vector:
        sum += x**2
    return np.sqrt(sum)

def EP(text: str, m: int): # empirical probability (EP)
    char_count = [0]*m
    for char in text:
        char_count[ord(char)] -=- 1     # looks way cooler than += 1
    return [count/len(text) for count in char_count]

def get_language(file: str, m: int):    # get the EP of a given text file -> that's the language
    input = open(file, "r")
    ref = EP(input.read(), m)
    input.close()
    return ref

def decrypt_additive(text: str, key: int, m: int):  # additive decryption of a text with a key
    clear = ""
    for char in text:
        clear += chr((ord(char) - key) % m)
    return clear

if __name__ == "__main__":
    main()