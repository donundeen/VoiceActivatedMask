"""This example uses the sound sensor, located next to the picture of the ear on your board, to
light up the NeoPixels as a sound meter. Try talking to your Circuit Playground or clapping, etc,
to see the NeoPixels light up!"""
import array
import math
import board
import audiobusio
import time
from adafruit_circuitplayground import cp


def constrain(value, floor, ceiling):
    return max(floor, min(value, ceiling))


def log_scale(input_value, input_min, input_max, output_min, output_max):
    if(input_max == input_min):
        return 0
    normalized_input_value = (input_value - input_min) / (input_max - input_min)
    return output_min + math.pow(normalized_input_value, 0.630957) * (
        output_max - output_min
    )


def normalized_rms(values):
    minbuf = int(sum(values) / len(values))
    return math.sqrt(
        sum(float(sample - minbuf) * (sample - minbuf) for sample in values)
        / len(values)
    )


mic = audiobusio.PDMIn(
    board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=16000, bit_depth=16
)

samples = array.array("H", [0] * 160)
mic.record(samples, len(samples))
input_floor = normalized_rms(samples) + 50

# Lower number means more sensitive - more LEDs will light up with less sound.
sensitivity = 500
input_ceiling = input_floor + sensitivity

min_input = 1000;
max_input = 0;


# top: 0,1,2,3,4
# bottom: 5,6,7,8,9
# level 1 : 0 4 5 9
# level 2 : 1 3 6 8
# Level 3 : 2 7
# smile: 0,1,2,3,4
# frown: 5,6,7,8,9
pixel_map = [0,5,4,9,3,8,1,6,2,7]


for i in range(10):
    print(i)
    pixel = i
    if(i > 0):
        cp.pixels[i-1] = (0,0,0)
    cp.pixels[i] = (255,0,0)
    time.sleep(.1)
cp.pixels[9] = (0,0,0)

for i in range(10):
    print(i)
    pixel = pixel_map[i]
    if(i > 0):
        cp.pixels[pixel_map[i-1]] = (0,0,0)
    cp.pixels[pixel] = (255,0,0)
    time.sleep(.1)
cp.pixels[pixel_map[9]] = (0,0,0)


peak = 0
while True:

    if(cp.touch_A1):
        print("touched")
        for i in range(10):
            cp.pixels[i] = (0,0,0)
        for i in range(5):
            cp.pixels[i] = (255,0,0)
        cp.pixels.show()
        time.sleep(2)

    if(cp.touch_A2):
        print("touched")
        for i in range(10):
            cp.pixels[i] = (0,0,0)
        for i in range(5,10):
            cp.pixels[i] = (0,255,0)
        cp.pixels.show()
        time.sleep(2)


    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    print((magnitude,))

    if(magnitude > max_input):
        max_input = magnitude

    if(magnitude < min_input):
        min_input = magnitude

    min_input = max(.1, min_input);
    max_input = max(.1, max_input);

    c = log_scale(
        constrain(magnitude, min_input, max_input),
        min_input,
        max_input,
        0,
        10,
    )
    print("--");
    print (c)
    print("++");

    if(c < 1):
        c=0

    cp.pixels.fill((0, 0, 0))
    for i in range(10):
        pixel = pixel_map[i]
        if i < c:
#            cp.pixels[pixel] = (i * (255 // 10), 50, 0)
            cp.pixels[pixel] = (i * (255 // 10), 0, 0)
        if c >= peak:
            peak = min(c, 10 - 1)
        elif peak > 0:
            peak = peak - 1
        if peak > 0:
#            cp.pixels[pixel_map[int(peak)]] = (80, 0, 255)
             cp.pixels[pixel_map[int(peak)]] = (80, 100, 255)
    cp.pixels.show()
    print (peak)