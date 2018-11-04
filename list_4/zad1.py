import math
import string

def most_common(lst):
    if set(lst) == set():
        return ''
    return max(set(lst), key=lst.count)

def bits2string(b=None):
    return ''.join([chr(int(x, 2)) for x in b])

def fun(lst):
    letters = string.ascii_lowercase



def main():
    l = int(input("no. of messages: "))
    msgs = []
    for i in range (0, l):
        msgs.append( input(str(i) + ": ").replace(" ", "") )
    target =  input("target: ").replace(" ", "")
    maxlen = max([len(m) // 8 for m in msgs])
    helper = []
    for i in range(0, l):
        new = [0] * maxlen
        helper.append(new)

    for a in range(0, l):
        for b in range (1 ,l):
            if (b <= a):
                continue
            for i in range(0, min( len(msgs[a]), len(msgs[b]) ), 8):
                xored = int(msgs[a][i:i+8], 2) ^ int(msgs[b][i:i+8], 2)
                xored_str = format(xored, 'b').zfill(8)
                print(xored_str)
                if (xored_str[:2] == "01"):
                    helper[a][i // 8] += 1
                    helper[b][i // 8] += 1
    print(helper)

    helper_bytes = []
    for bidx in range(0, maxlen ):
        helper_bytes.append([])
        local_max = max( [helper[i][bidx] for i in range (0, l)] )
        print(local_max)
        for i in range(0, l):
            if local_max == helper[i][bidx]:
                print(str(i) + " " + str(bidx))
                if (len(msgs[i]) > bidx * 8):
                    helper_bytes[bidx].append(msgs[i][bidx * 8:bidx * 8+8])
    print(helper_bytes)

    for bidx in range(0, maxlen):
        for eidx in range( 0, len(helper_bytes[bidx]) ):
            xored = int(helper_bytes[bidx][eidx], 2) ^ int("00100000", 2)
            helper_bytes[bidx][eidx] = format(xored, 'b').zfill(8)

    print(helper_bytes)

    filtered = []
    for bidx in range(0, maxlen):
        filtered.append([])
        filtered[bidx] = [helper_bytes[bidx][i] for i in range(0, len(helper_bytes[bidx])) if chr(int(helper_bytes[bidx][i], 2)) in string.ascii_letters or chr(int(helper_bytes[bidx][i], 2)) in string.digits]
    print(filtered)

    key = ''.join( [ most_common(helper_bytes[bidx]) for bidx in range(0, maxlen) ] )
    print((key))
    print( format( int(key, 2) ^ int(msgs[0], 2), 'b' ) )

    output = []
    for i in range(0, min( len(key), len(target) ), 8):
        xored = int(key[i:i+8], 2) ^ int(target[i:i+8], 2)
        xored_str = format(xored, 'b').zfill(8)
        output.append( chr( int( xored_str, 2 ) ) )

    print(*output, sep='')

if __name__ == "__main__":
    main()
