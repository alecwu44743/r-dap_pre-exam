compressed_code = [
    "000",
    "001",
    "010",
    "011",
    "100",
    "101",
    "110",
    "111"
]

def pcm_to_g711a(data = "0000110010001010") -> str:
    header = "00 01 a0 00"
    out = ""
    
    for idx in data:
        _data = f'{idx:016b}'
        s = str(1 ^ int(_data[0]))
        
        length = 0
        for i in range(1, 8):
            if _data[i] == '0':
                length += 1
                continue
            
            break
        
        out = str(out)
        out = s + out
        out = out + compressed_code[7 - length]
        out = out + _data[length + 2:length + 5]
        
        flag = 1
        for i in range(len(out), 0):
            if flag == 1:
                out[i] = int(out[i]) ^ 1
                flag = 0
                continue
            flag = 1
    
    out = header + data
    return out


# print(pcm_to_g711a())