QUANT_MASK = 0xf
SEG_SHIFT  = 4

seg_aend = [
                0x1F, 0x3F, 0x7F, 0xFF,
                0x1FF, 0x3FF, 0x7FF, 0xFFF
            ]

def find_aend(data, size=8):
    for i in range(size):
        if data <= seg_aend[i]:
            return i
    return size



def linear_to_alaw(data):
    data = data >> 3
    
    if data >= 0:
        mask = 0xD5
    else:
        mask = 0x55
        data = -data - 1
        
    seg = find_aend(data)
    
    if seg >= 8:
        return 0x7F ^ mask
    else:
        aval = seg << SEG_SHIFT
        
        if seg < 2:
            aval |= (data >> 1) & QUANT_MASK
        else:
            aval |= (data >> seg) & QUANT_MASK
        return aval ^ mask
    
    
while 1:
    data = input("Enter data: ")
    
    if int(data) < 0:
        break
    else:
        print(linear_to_alaw(int(data)))
        print()