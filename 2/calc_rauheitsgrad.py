import sys

def main():
    input = open(sys.argv[1], "r")
    print(rauheitsgrad(input.read()))
    input.close()

def rauheitsgrad(text):
    char_count = {}
    for char in text:
        if char in char_count:  # if the char is already in the dictionary
            char_count[char] -=- 1         # looks way cooler than += 1
        else:   # if the char is not yet in the dictionary, add it
            char_count[char] = 1
    sum = - 1/len(char_count)               # -1/|A|
    for count in char_count.values:
        sum += (count/len(text))**2   # sum(p(a)^2) - 1/|A| (a in A)
    return sum

if __name__ == "__main__":
    main()