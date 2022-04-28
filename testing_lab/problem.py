from bz2 import compress
import pyaudio
import wave

'''
pcm to g711a

1. pcm是對模擬的連續訊號進行抽樣。
2. g711則是對pcm資料進行再一次的抽樣。
3. g711主要是對16bit的pcm進行抽樣,取到pcm的高位資料,去掉低位的資料,並且只保留8位。這樣壓縮的比率就達到了2:1。可知是有失真壓縮。

'''

CHUNK = 160
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "demo.wav"
G711_OUTPUT_FILENAME = "demo.g711a"

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

def pcm_to_g711a(data: bytes) -> bytes:
    header = b'\x00\x01\xa0\x00'
    out = bytes()
    
    for idx in data:
        # print("index: " + str(idx))
        _data = f'{idx:013b}'
        # print("_data: " + _data)
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
    # print("out: " + str(out))
    return out
    


p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("start recording......")
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    data = pcm_to_g711a(data)
    print(data,"\n\n")
    frames.append(data)
print("end!")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(G711_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()


# reference - https://www.vine.wiki/a_keji/202109/304208.html
# reference - https://blog.csdn.net/jenie/article/details/106298846
# reference - https://www.itread01.com/content/1541337363.html
# reference - https://www.796t.com/content/1541337363.html

'''
输入pcm数据为3210, 二进制对应为 (0000 1100 1000 1010)

二进制变换下排列组合方式 (0 0001 1001 0001010)

(1)      获取符号位最高位为0,取反,s=1

(2)      获取强度位0001,查表,编码制应该是eee=100

(3)      获取高位样本wxyz=1001

(4)      组合为11001001,逢偶数为取反为10011100

编码完毕。
————————————————
版权声明:本文为CSDN博主「jenie」的原创文章,遵循CC 4.0 BY-SA版权协议,转载请附上原文出处链接及本声明。
原文链接:https://blog.csdn.net/jenie/article/details/106298846
'''
