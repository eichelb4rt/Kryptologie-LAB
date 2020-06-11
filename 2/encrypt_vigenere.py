import sys

def main():
    input = open(sys.argv[1], "r")
    text = input.read()
    input.close()
    m = int(sys.argv[3])
    key = [int(sys.argv[i]) for i in range(4,len(sys.argv))]
    crypto = encrypt_vigenere(text, m, key)
    output = open(sys.argv[2], "w")
    output.write(crypto)
    output.close()

def encrypt_vigenere(text: str, m: int, key: list):
    crypto = ""
    for i in range(0,len(text)):
        crypto += chr((ord(text[i]) + key[i%len(key)]) % m)
    return crypto

if __name__ == "__main__":
    main()