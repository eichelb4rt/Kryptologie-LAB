#!/bin/python3
# SHEBANG

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        metavar = 'in',
        dest = 'input',
        help = 'File that the input text is read from'
    )
    parser.add_argument(
        metavar = 'out',
        dest = 'output',
        help = 'File that the output text is written to'
    )
    parser.add_argument(
        '-k',
        '--key',
        metavar = 'key',
        dest = 'key',
        default = 'key.txt',
        help = 'File that the key is read from (default: key.txt)'
    )
    parser.add_argument(
        '-l',
        '--blocklength',
        metavar = 'blocklength',
        dest = 'blocklength',
        type = int,
        default = 128,
        help = 'The length of the blocks in bits (default: 128)'
    )
    args = parser.parse_args()
    with open(args.input, "rb") as f_in, open(args.output, "wb") as f_out:
        while block := f_in.read(args.blocklength//8): # read the blocks
            block = int.from_bytes(block, 'big') << (args.blocklength - len(block)*8)   # pad the block if it's not full (fill the right side with 0) (len(block) is in bytes)
            #output = encrypt_block(block, key, args.blocklength)  # encrypt the block
            #f_out.write(output.to_bytes(args.blocklength//8, 'big'))    # write it in binary

if __name__ == "__main__":
    main()