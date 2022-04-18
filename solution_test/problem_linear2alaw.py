from bz2 import compress
import pyaudio
import wave

CHUNK = 160
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "demo.wav"
G711_OUTPUT_FILENAME = "demo.g711a"

QUANT_MASK = 0xf
SEG_SHIFT = 4
SEG_MASK = 0x70 # 0b1110000

seg_aend = [ 0x1F,  # 0b000000011111
             0x3F,  # 0b000000111111
             0x7F,  # 0b000001111111
             0xFF,  # 0b000011111111
             0x1FF, # 0b000111111111
             0x3FF, # 0b001111111111
             0x7FF, # 0b011111111111
             0xFFF  # 0b111111111111
           ];

# seg_uend = [ 0x3F,  # 0b0000000111111
#              0x7F,  # 0b0000001111111
#              0xFF,  # 0b0000011111111
#              0x1FF, # 0b0000111111111
#              0x3FF, # 0b0001111111111
#              0x7FF, # 0b0011111111111
#              0xFFF, # 0b0111111111111
#              0x1FFF # 0b1111111111111
#            ];


def find_seg(data, size=8):
    for i in range(size):
        if data <= seg_aend[i]:
            return i
    return size

def pcm_to_g711a(data: bytes) -> bytes:
    data = data >> 3
    
    if data >= 0:
        mask = 0xD5
    else:
        mask = 0x55
        pcm_val = -(int(pcm_val)) - 1
        
    seg = find_seg(pcm_val)
    if seg >= 8:
        return 0x7F ^ mask
    else:
        aval = seg << SEG_SHIFT
        if seg < 2:
            aval |= (data >> 1) & QUANT_MASK
        else:
            aval |= (data >> seg) & QUANT_MASK
        return aval ^ mask



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
