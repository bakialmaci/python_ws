import sys
print("dene")

bits = ""
steghedImage = sys.argv[1] #Image Path
keyWord = sys.argv[2] #Word that will be search
iteration = sys.argv[3] # Binary shifting value.

print("Searching:",keyWord)

for seq in range(int(iteration)):
    print(seq,"/",iteration)
    with open(steghedImage, "rb") as f:
        data = f.read()

        data = data[seq:]

        for c in data:
            lsb = str(c & 0x1) # I got an LSB value.
            bits += lsb # I have collect all LSB to here

        bytess = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
        lsbstr = "".join(bytess)
        if keyWord in lsbstr:
            print(lsbstr)
            print("\n Founded at",seq,". iteration")
            break
