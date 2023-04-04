from machine import *
from time import *
import time

start=time.ticks_ms()

led0=Pin(25,Pin.OUT,value=1)
led=[Pin(14,Pin.OUT,value=0),Pin(19,Pin.OUT,value=0),Pin(8,Pin.OUT,value=0),Pin(6,Pin.OUT,value=0)]
sw=[Pin(15,Pin.IN),Pin(18,Pin.IN),Pin(9,Pin.IN),Pin(7,Pin.IN)]
adc=ADC(Pin(28))
tsensor=ADC(4)
period=adc.read_u16()
i=0
logfile='log.txt'

def led_move(t):
    global i,tim
    if i>0:
        led[i-1].on()
        if sw[i].value()==1:
            led[i].off()
    else:
        led[3].on()
        if sw[i].value()==1:
            led[i].off()
    if i<3:
        i=i+1
    else:
        i= 0
    newperiod=int(adc.read_u16()/65535*1000)
    tim = Timer(period=newperiod, mode=Timer.ONE_SHOT, callback=led_move)
    

tim=Timer(period=0, mode=Timer.ONE_SHOT, callback=led_move)


#lib
#conversione da count a tensione
def v(c):
    return 3.3*c/65536


#conversione da tensione a temperatura
def t(v):
    return 27-((v-0.706)/0.001721)


#write log
def log_temp(tT):
    f = open(logfile,'a')
    mylog=str(time.ticks_diff(time.ticks_ms(),start))+", "+str(t(v(tsensor.read_u16())))+"\n"
    f.write(mylog)
    f.close()


#read log
def readlog():
    f = open(logfile, 'r')
    print(f.read())
    f.close()


timT = Timer(period=0, mode=Timer.ONE_SHOT, callback=log_temp)
timT = Timer(period=60000, mode=Timer.PERIODIC, callback=log_temp)