import board
import neopixel
import requests
from time import sleep
from datetime import datetime
from datetime import timedelta

brightness_input = 1 # Brughtness Level. Max = 1

loopspeed = .2 #Number of seconds between loops

flashcount = 10

isactive = "false"
pixels = neopixel.NeoPixel(board.D18, 100, brightness = 1, auto_write=True)
pixels2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

file = open('/home/pi/Scoreboard/scores.txt', 'r')
lines = file.readlines()

active_count = 0


def brightness():
    
    global pixels
    global brightness_input
    file3 = open('/home/pi/Scoreboard/brightness.txt', 'r')
    lines3 = file3.readlines()
    brightness_input = float(lines3[0]) / 100
    brightness_input = max(brightness_input, .03)
    file3.close

def startup():

    #Signal Reset

    #W>B>G>R>X

    g = 200
    r = 200
    b = 200

    #W>B
    while r > 0:
        pixels.fill((g, r, b))
        r = max(r-5,0)
        sleep(.00005)

    #B>G
    while b > 0:
        pixels.fill((g, r, b))
        b = max(b-5,0)
        sleep(.00005)

    #G>R
    while r < 255:
        pixels.fill((g, r, b))
        g = max(g-5,0)
        r = min(r+5,255)
        sleep(.00005)

    #R>X
    while r > 0:
        pixels.fill((g, r, b))
        r = max(r-5,0)
        sleep(.00005)
        
    pixels.fill((0, 0, 0))

def GetColors():
    
    global active_count
    active_count = 0
    
    file = open('/home/pi/Scoreboard/scores.txt', 'r')
    lines = file.readlines()
    line_counter = -1

    #SET FADE TO COLORS
    for index, line in enumerate(lines):
        
        string = line.strip()
        line_counter = line_counter + 1
        
        light_number = int(string[1:3])
        color_code = string[4:5]
        flash_code = string[6:7]

        
        if color_code == "R":
            green_value = 0 
            red_value = 255 
            blue_value = 0 
            
        if color_code == "B":
            green_value = 255 
            red_value = 0 
            blue_value = 255 
            
        if color_code == "Y":
            green_value = 255 
            red_value = 255 
            blue_value = 0 
            
        if color_code == "G":
            green_value = 255 
            red_value = 0 
            blue_value = 0 
            
        if color_code == "P":
            green_value = 0 
            red_value = 30 
            blue_value = 30 
            
        if color_code == "O":
            green_value = 100 
            red_value = 255 
            blue_value = 0 
            
        if color_code == "X":
            green_value = 0 
            red_value = 0 
            blue_value = 0
            
        if color_code != "X":
            active_count = active_count + 1
            
        pixels2[light_number] = [int(round(green_value,0)), int(round(red_value,0)), int(round(blue_value,0))]

    file.close()
    
    print("Scheduled Games: " , active_count)

def Schedule():
    #Show Schedule
    file2 = open('/home/pi/Scoreboard/matchups.txt', 'r')
    lines2 = file2.readlines()
    

    for index, line in enumerate(lines2):
        
        brightness()
        br = brightness_input
        full_b = int(round(255 * br,0))
    
        string = line.strip()
        
        if string != "X-X":
            
        
            t1 = int(string[0:2].replace("-",""))
            t2 = string[-2] + string[-1]
            t2 = int(t2.replace("-",""))
            
            print("Schedule: ", t1, " vs ", t2)
            
            g=0
            b=0
            r=0
            
            #Fade Blue in
            while g < full_b:
                pixels[t1] = g, r, b
                pixels[t2] = g, r, b
                g = min(g+int(round(17 * br,0)), full_b)
                b = min(b+int(round(17 * br,0)), full_b)
                sleep(.0005)
            sleep(1)
            
            #Fade to Color
            
            fade_speed_adjust = .1 #Lower Number = Faster Fading
            fade_speed_adjust = fade_speed_adjust / max(1,active_count)
            fade_speed = max(round(5 * br,0),1)
            change = "true"
            
            #Fade Green
            while change == "true":
                sleep(fade_speed_adjust)
                change = "false"
                if pixels[t1][0] < round(pixels2[t1][0] * br,0):
                    pixels[t1] = min(pixels[t1][0] + fade_speed + 1, full_b), pixels[t1][1], pixels[t1][2]
                    change = "true"
                if pixels[t1][0] > round(pixels2[t1][0] * br,0):
                    pixels[t1] = max(pixels[t1][0] - fade_speed, 0), pixels[t1][1], pixels[t1][2]
                    change = "true"
                if pixels[t2][0] < round(pixels2[t2][0] * br,0):
                    pixels[t2] = min(pixels[t2][0] + fade_speed + 1, full_b), pixels[t2][1], pixels[t2][2]
                    change = "true"
                if pixels[t2][0] > round(pixels2[t2][0] * br,0):
                    pixels[t2] = max(pixels[t2][0] - fade_speed, 0), pixels[t2][1], pixels[t2][2]
                    change = "true"
                    
            #Fade Red

                if pixels[t1][1] < round(pixels2[t1][1] * br,0):
                    pixels[t1] = pixels[t1][0], min(pixels[t1][1] + fade_speed + 1, full_b), pixels[t1][2]
                    change = "true"
                if pixels[t1][1] > round(pixels2[t1][1] * br,0):
                    pixels[t1] = pixels[t1][0], max(pixels[t1][1] - fade_speed, 0), pixels[t1][2]
                    change = "true"
                if pixels[t2][1] < round(pixels2[t2][1] * br,0):
                    pixels[t2] = pixels[t2][0], min(pixels[t2][1] + fade_speed + 1, full_b), pixels[t2][2]
                    change = "true"
                if pixels[t2][1] > round(pixels2[t2][1] * br,0):
                    pixels[t2] = pixels[t2][0], max(pixels[t2][1] - fade_speed, 0), pixels[t2][2]
                    change = "true"
                
            #Fade Blue

                if pixels[t1][2] < round(pixels2[t1][2] * br,0):
                    pixels[t1] = pixels[t1][0], pixels[t1][1], min(pixels[t1][2] + fade_speed + 1, full_b)
                    change = "true"
                if pixels[t1][2] > round(pixels2[t1][2] * br,0):
                    pixels[t1] = pixels[t1][0], pixels[t1][1], max(pixels[t1][2] - fade_speed, 0)
                    change = "true"
                if pixels[t2][2] < round(pixels2[t2][2] * br,0):
                    pixels[t2] = pixels[t2][0], pixels[t2][1], min(pixels[t2][2] + fade_speed + 1, full_b)
                    change = "true"
                if pixels[t2][2] > round(pixels2[t2][2] * br,0):
                    pixels[t2] = pixels[t2][0], pixels[t2][1], max(pixels[t2][2] - fade_speed, 0)
                    change = "true"



    file2.close()


def Flash(flashcount):

    line_counter = -1
    loopstop = "false"
    flashmode = 1
    loop = 1
    isactive = "true"
    
    brightness()
    b = brightness_input
    full_b = int(round(255 * b,0))

    #Flashing

    flashcount = flashcount * 6

    #DO
    while loop <= flashcount and isactive == "true":
        isactive = "false"
        line_counter = -1
        print("Flashing: ", loop, "/", flashcount)
        brightness()
        br = brightness_input
        full_b = int(round(255 * br,0))
        for index, line in enumerate(lines):
            
            
            string = line.strip()
            line_counter = line_counter + 1
            
            light_number = int(string[1:3])
            color_code = string[4:5]
            flash_code = int(string[6:7])
            
            if flash_code != 0:
                isactive = "true"
            
            if color_code == "R":
                green_value = 0
                red_value = full_b
                blue_value = 0
                
            if color_code == "B":
                green_value = full_b
                red_value = 0
                blue_value = full_b
                
            if color_code == "Y":
                green_value = full_b / 2
                red_value = full_b
                blue_value = 0
            
            if color_code == "G":
                green_value = full_b
                red_value = 0
                blue_value = 0
            
            if color_code == "P":
                green_value = 0
                red_value = full_b
                blue_value = full_b
            
            if color_code == "O":
                green_value = 100
                red_value = full_b
                blue_value = 0
            
            if color_code == "X":
                green_value = 0
                red_value = 0
                blue_value = 0
        
            #EVERYTHING ON FOR MODE 4 OR 6
            if flashmode == 4 or flashmode == 6:
                if flash_code != 0:
                    pixels[light_number] = green_value, red_value, blue_value
                
            
            #EVERYTHING OFF FOR MODE 1 OR 3
            if flashmode == 1 or flashmode == 3:
                if flash_code != 0:
                    pixels[light_number] = 0, 0, 0
                
            
            #MODE 2
            if flashmode == 2 and flash_code != 0:
                if flash_code == 1:
                    pixels[light_number] = 0, 0, 0
                else:
                    pixels[light_number] = green_value, red_value, blue_value
                    
                
            #MODE 5
            if flashmode == 5 and flash_code != 0:
                if flash_code == 2:
                    pixels[light_number] = 0, 0, 0
                else:
                    pixels[light_number] = green_value, red_value, blue_value
        
        flashmode = flashmode + 1
        
        if flashmode == 7:
            flashmode = 1
        
        sleep(loopspeed)

        loop = loop + 1


    if(isactive != "true"):
        print("No Active Games. Skipping Flash")
        sleep(.5)

    file.close()

def trigger():
    triggerfile = open('/home/pi/Scoreboard/trigger.txt', 'r')
    triggerline = triggerfile.readlines()
    newtrigger = str(int(triggerline[0]) + 1)
    triggerfile = open('/home/pi/Scoreboard/trigger.txt', 'w')
    triggerfile.write(newtrigger)
    print("Setting Trigger: " + newtrigger)

#The actual run sequence**********************************************************************************************
print("Starting up...")

while True:
    brightness()
    print("Getting Colors")
    GetColors()
    print("Schedule")
    Schedule()
    print("Flash")
    Flash(flashcount)
    trigger()
    sleep(1)
