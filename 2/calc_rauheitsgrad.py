import sys

def main():
    input = open(sys.argv[1], "r")
    print(rauheitsgrad(input.read()))
    input.close()

def rauheitsgrad(text):
    char_count = [0]*128
    for char in text:
        char_count[ord(char)] -=- 1         # looks way cooler than += 1
    sum = - 1/len(char_count)               # -1/|A|
    for count in char_count:
        sum += (count/len(text))**2   # sum(p(a)^2) - 1/|A| (a in A)
    return sum

if __name__ == "__main__":
    main()