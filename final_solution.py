import pyaudio
import wave


# audio setup
CHUNK = 160
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "demo.wav"
G711_OUTPUT_FILENAME = "out_demo.g711a"

#converter variables
QUANT_MASK = 0xf   # 15 ->  0b000000001111
NSEGS      = 8
SEG_SHIFT  = 4
SEG_MASK   = 0x70  # 112 -> 0b000001110000
seg_aend = [
                0x1F,   # 31    -> 0b000000011111
                0x3F,   # 63    -> 0b000000111111
                0x7F,   # 127   -> 0b000001111111
                0xFF,   # 255   -> 0b000011111111
                0x1FF,  # 511   -> 0b000111111111
                0x3FF,  # 1023  -> 0b001111111111
                0x7FF,  # 2047  -> 0b011111111111
                0xFFF   # 4095  -> 0b111111111111
            ]



def int2bytes(val: int, size=1) -> bytes:
    out = val.to_bytes(size, 'big')
    return out

def bytes2int(val: bytes) -> int:
    out = int.from_bytes(val, 'big')
    return out



def find_aend(data, size=8):
    for i in range(size):
        if data <= seg_aend[i]:
            return i
    return size

def linear_to_alaw(bytes_val: bytes) -> bytes:
    out = bytes()
    
    for data in bytes_val:
        
        # print(data)

        data = data >> 3
    
        if data >= 0:
            mask = 0xD5
        else:
            mask = 0x55
            data = -data - 1
            
        seg = find_aend(data)

        if seg >= 8:
            out += int2bytes((0x7F ^ mask))
        else:
            aval = seg << SEG_SHIFT
            # print(aval)
            
            if seg < 2:
                aval |= (data >> 1) & QUANT_MASK
            else:
                aval |= (data >> seg) & QUANT_MASK
            # print(aval)
            # print("->" + str(aval ^ mask))
            out += int2bytes((aval ^ mask))
            
        # print()
        # print()
        # print(out)
        # print()
        # print()
            
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
    bytes_data = stream.read(CHUNK)
    bytes_data = linear_to_alaw(bytes_data)
    bytes_data = b'\x00\x01\xa0\x00'+ bytes_data
    print(bytes_data, "\n\n")
    frames.append(bytes_data)
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
# rf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')