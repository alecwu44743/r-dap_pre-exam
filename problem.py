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

compressed_code = {
    "0000000" : "000",
    "0000001" : "001",
    "000001" : "010",
    "00001" : "011",
    "0001" : "100",
    "001" : "101",
    "01" : "110",
    "1" : "111"
}

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
    print(data,"\n\n")
    frames.append(data)
print("end!")
stream.stop_stream()
stream.close()
p.terminate()
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()


# reference - https://www.vine.wiki/a_keji/202109/304208.html
# reference - https://blog.csdn.net/jenie/article/details/106298846
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
