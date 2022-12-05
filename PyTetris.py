import tkinter as tk
import random
from tkinter import messagebox
import configparser
import time
from tetro.tetro import tetro_set
from tetro.misc import color_blend, spent_time, log_namer, num_time
import pygame
from PIL import ImageTk

pygame.init()
version = "1.0.0"
config = configparser.ConfigParser()
log = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
log.read('pytetris.log', encoding='utf-8')
log_name = log_namer(config)

color = config["COLOR"]
cont = config["KEY"]
glob = config["GLOBAL"]
SIZE = 30
SIZE_NEXT = 25
SIZE_LANE = 20
moveX = 5
moveY = 0
scene = 0
pause = False
start = time.time()
end = time.time()
pause_time = 0.0
karl = 0.0
parl = 0.0
snow = 0

btb = 1.0
pc = False
hdrop = False
hardd = False
tspin = False
spin = False
tmini = False
stone = False
replayed = False

hcount = 1
combo = 0
type_hold = 100
type_s = 100
turn = 0
dturn = 0
scene = 0
tetro = tetro_set(glob["rotation"], "list")
tl = len(tetro)
tetro_bag = [i for i in range(0, tl)]

move_s = pygame.mixer.Sound(".\sound\move.wav")
turn_s = pygame.mixer.Sound(".\sound\\turn.wav")
hdrop_s = pygame.mixer.Sound(".\sound\\harddrop.wav")
soft_s = pygame.mixer.Sound(".\sound\\soft.wav")
hold_s = pygame.mixer.Sound(".\sound\\hold.wav")
land_s = pygame.mixer.Sound(".\sound\\land.wav")
pause_s = pygame.mixer.Sound(".\sound\\pause.wav")
tspin_s = pygame.mixer.Sound(".\sound\\tspin.wav")
uline_s = pygame.mixer.Sound(".\sound\\1line.wav")
dline_s = pygame.mixer.Sound(".\sound\\2line.wav")
tline_s = pygame.mixer.Sound(".\sound\\3line.wav")
qline_s = pygame.mixer.Sound(".\sound\\4line.wav")
level_s = pygame.mixer.Sound(".\sound\\level.wav")
perfect_s = pygame.mixer.Sound(".\sound\\perfect.wav")
c1_s = pygame.mixer.Sound(".\sound\\combo1.wav")
c2_s = pygame.mixer.Sound(".\sound\\combo2.wav")
c3_s = pygame.mixer.Sound(".\sound\\combo3.wav")
c4_s = pygame.mixer.Sound(".\sound\\combo4.wav")
c5_s = pygame.mixer.Sound(".\sound\\combo5.wav")
c6_s = pygame.mixer.Sound(".\sound\\combo6.wav")
pygame.mixer.music.load(".\sound\BGM.mp3")

wallkickC = tetro_set(glob["rotation"], "C")
wallkickCC = tetro_set(glob["rotation"], "CC")
sym_pic = tetro_set(glob["rotation"], "sym")
spin_pic = tetro_set(glob["rotation"], "spin")
even_pic = tetro_set(glob["rotation"], "even")

def RMG():
    global tetro_bag
    type_mino = 0
    if tetro_bag == []:
        tetro_bag = [i for i in range(0, tl)]
    type_mino = random.choice(tetro_bag)
    tetro_bag.remove(type_mino)
    return type_mino

type_c = RMG()
type_next = RMG()
type_0 = RMG()
type_1 = RMG()
type_2 = RMG()
type_3 = RMG()
type_4 = RMG()
type_5 = RMG()
    
level = int(glob["SLevel"])

if glob["gamemode"] == "original" or glob["gamemode"] == "orlv15" or glob["gamemode"] == "limor" or glob["gamemode"] == "lolv15":
    timer = int(1000*((0.8-((level-1)*0.007))**(level-1)))
else:
    timer = 850 - (50 * level)
if glob["gamemode"] == "original" or glob["gamemode"] == "orlv15":
    if level > 9 :
        timer = int(1000*((0.8-(8*0.007))**8))
elif glob["gamemode"] == "normal" or glob["gamemode"] == "level15":
    if timer < 150:
        timer = 150
elif glob["gamemode"] == "limless" or glob["gamemode"] == "lesslv15":
    if timer < 10:
        timer = 10
        
score = 0
line = 0

if glob["leveling"] == "normal":
    rest_line = 10 * level
elif glob["leveling"] == "world":
    rest_line = 5 * level
else:
    rest_line = 10
    
listed = [0]

if log_name != "":
    try:
        hscore = int(log["LOG"][log_name+"_score"])
        former_time = num_time(log["LOG"][log_name+"_time"])
    except KeyError:
        hscore = 0
        former_time = 0.0
else:
    hscore = 0
    former_time = 0.0
if score >= hscore:
    hscore = score

def make_field(field_list = None):
    fielded = []
    if field_list != None:
        if type(field_list) is list:
            fielded = field_list
    else:
        for y in range(26):
            sub = []
            for x in range(16):
                if x==0 or x>=11 or y>=21 :
                    sub.append(40)
                else :
                    sub.append(50)
            fielded.append(sub)
    return fielded

field = make_field()
field0 = make_field()

nextfield = []
for y in range(20):
    sub = []
    for x in range(20):
        sub.append(50)
    nextfield.append(sub)

lanefield = []
for y in range(120):
    sub = []
    for x in range(20):
        sub.append(50)
    lanefield.append(sub)

def drawTetris():
    global turn, tetro
    if type_c in even_pic:
        add = 0.5
    else:
        add = 0
    for i in range(int(len(tetro[type_c][turn])/2)):
        x = int(tetro[type_c][turn][i*2]+moveX+add)*SIZE
        y = int(tetro[type_c][turn][i*2+1]+moveY+add)*SIZE
        base = color[str(type_c)]
        light = color_blend(base, "white")
        semi_shade = color_blend(base, "gray")
        shade = color_blend(base, "black")
        can.create_rectangle(x, y, x+SIZE, y+SIZE, fill=semi_shade, width=1, outline=shade)
        can.create_polygon(x, y, x+SIZE, y, x+int(SIZE/2), y+int(SIZE/2), fill=light, width=0)
        can.create_polygon(x, y+SIZE, x+SIZE, y+SIZE, x+int(SIZE/2), y+int(SIZE/2), fill=shade, width=1, outline="black")
        can.create_rectangle(x+3, y+3, x+SIZE-3, y+SIZE-3, fill=base, width=0)

def drawGhostTetris():
    global turn, tetro
    k = hard_drop(moveX, moveY, tetro[type_c][turn], False)
    if type_c in even_pic:
        add = 0.5
    else:
        add = 0
    for i in range(int(len(tetro[type_c][turn])/2)):
        x = int(tetro[type_c][turn][i*2]+moveX+add)*SIZE
        y = int(tetro[type_c][turn][i*2+1]+moveY+add+k)*SIZE
        can.create_rectangle(x+1, y+1, x+SIZE-1, y+SIZE-1, width=2, outline="red")
             
def drawNextTetris(yelt):
    if yelt >= 7:
        ax = tetro[type_5][4]
        ay = tetro[type_5][5]
        base = color[str(type_5)]
        light = color_blend(base, "white")
        semi_shade = color_blend(base, "gray")
        shade = color_blend(base, "black")
        for i in range(int(len(tetro[type_5][0])/2)):
            x = (tetro[type_5][0][i*2]+ax+1)*SIZE_LANE
            y = (tetro[type_5][0][i*2+1]+ay+1+int(4*5))*SIZE_LANE
            lane.create_rectangle(x, y, x+SIZE_LANE, y+SIZE_LANE, fill=semi_shade, width=1, outline=shade)
            lane.create_polygon(x, y, x+SIZE_LANE, y, x+int(SIZE_LANE/2), y+int(SIZE_LANE/2), fill=light, width=0)
            lane.create_polygon(x, y+SIZE_LANE, x+SIZE_LANE, y+SIZE_LANE, x+int(SIZE_LANE/2), y+int(SIZE_LANE/2), fill=shade, width=1, outline="black")
            lane.create_rectangle(x+2, y+2, x+SIZE_LANE-2, y+SIZE_LANE-2, fill=base, width=0)
    if yelt >= 6:
        ax = tetro[type_4][4]
        ay = tetro[type_4][5]
        base = color[str(type_4)]
        light = color_blend(base, "white")
        semi_shade = color_blend(base, "gray")
        shade = color_blend(base, "black")
        for i in range(int(len(tetro[type_4][0])/2)):
            x = (tetro[type_4][0][i*2]+ax+1)*SIZE_LANE
            y = (tetro[type_4][0][i*2+1]+ay+1+int(4*4))*SIZE_LANE
            lane.create_rectangle(x, y, x+SIZE_LANE, y+SIZE_LANE, fill=semi_shade, width=1, outline=shade)
            lane.create_polygon(x, y, x+SIZE_LANE, y, x+int(SIZE_LANE/2), y+int(SIZE_LANE/2), fill=light, width=0)
            lane.create_polygon(x, y+SIZE_LANE, x+SIZE_LANE, y+SIZE_LANE, x+int(SIZE_LANE/2), y+int(SIZE_LANE/2), fill=shade, width=1, outline="black")
            lane.create_rectangle(x+2, y+2, x+SIZE_LANE-2, y+SIZE_LANE-2, fill=base, width=0)
    if yelt >= 5:
        ax = tetro[type_3][4]
        ay = tetro[type_3][5]
        base = color[str(type_3)]
        light = color_blend(base, "white")
        semi_shade = color_blend(base, "gray")
        shade = color_blend(base, "black")
        for i in range(int(len(tetro[type_3][0])/2)):
            x = (tetro[type_3][0][i*2]+ax+1)*SIZE_LANE
            y = (tetro[type_3][0][i*2+1]+ay+1+int(4*3))*SIZE_LANE
            lane.create_rectangle(x, y, x+SIZE_LANE, y+SIZE_LANE, fill=semi_shade, width=1, outline=shade)
            lane.create_polygon(x, y, x+SIZE_LANE, y, x+int(SIZE_LANE/2), y+int(SIZE_LANE/2), fill=light, width=0)
            lane.create_polygon(x, y+SIZE_LANE, x+SIZE_LANE, y+SIZE_LANE, x+int(SIZE_LANE/2), y+int(SIZE_LANE/2), fill=shade, width=1, outline="black")
            lane.create_rectangle(x+2, y+2, x+SIZE_LANE-2, y+SIZE_LANE-2, fill=base, width=0)
    if yelt >= 4:
        ax = tetro[type_2][4]
        ay = tetro[type_2][5]
        base = color[str(type_2)]
        light = color_blend(base, "white")
        semi_shade = color_blend(base, "gray")
        shade = color_blend(base, "black")
        for i in range(int(len(tetro[type_2][0])/2)):
            x = (tetro[type_2][0][i*2]+ax+1)*SIZE_LANE
            y = (tetro[type_2][0][i*2+1]+ay+1+int(4*2))*SIZE_LANE
            lane.create_rectangle(x, y, x+SIZE_LANE, y+SIZE_LANE, fill=semi_shade, width=1, outline=shade)
            lane.create_polygon(x, y, x+SIZE_LANE, y, x+int(SIZE_LANE/2), y+int(SIZE_LANE/2), fill=light, width=0)
            lane.create_polygon(x, y+SIZE_LANE, x+SIZE_LANE, y+SIZE_LANE, x+int(SIZE_LANE/2), y+int(SIZE_LANE/2), fill=shade, width=1, outline="black")
            lane.create_rectangle(x+2, y+2, x+SIZE_LANE-2, y+SIZE_LANE-2, fill=base, width=0)
    if yelt >= 3:
        ax = tetro[type_1][4]
        ay = tetro[type_1][5]
        base = color[str(type_1)]
        light = color_blend(base, "white")
        semi_shade = color_blend(base, "gray")
        shade = color_blend(base, "black")
        for i in range(int(len(tetro[type_1][0])/2)):
            x = (tetro[type_1][0][i*2]+ax+1)*SIZE_LANE
            y = (tetro[type_1][0][i*2+1]+ay+1+int(4))*SIZE_LANE
            lane.create_rectangle(x, y, x+SIZE_LANE, y+SIZE_LANE, fill=semi_shade, width=1, outline=shade)
            lane.create_polygon(x, y, x+SIZE_LANE, y, x+int(SIZE_LANE/2), y+int(SIZE_LANE/2), fill=light, width=0)
            lane.create_polygon(x, y+SIZE_LANE, x+SIZE_LANE, y+SIZE_LANE, x+int(SIZE_LANE/2), y+int(SIZE_LANE/2), fill=shade, width=1, outline="black")
            lane.create_rectangle(x+2, y+2, x+SIZE_LANE-2, y+SIZE_LANE-2, fill=base, width=0)
    if yelt >= 2:
        ax = tetro[type_0][4]
        ay = tetro[type_0][5]
        base = color[str(type_0)]
        light = color_blend(base, "white")
        semi_shade = color_blend(base, "gray")
        shade = color_blend(base, "black")
        for i in range(int(len(tetro[type_0][0])/2)):
            x = (tetro[type_0][0][i*2]+ax+1)*SIZE_LANE
            y = (tetro[type_0][0][i*2+1]+ay+1)*SIZE_LANE
            lane.create_rectangle(x, y, x+SIZE_LANE, y+SIZE_LANE, fill=semi_shade, width=1, outline=shade)
            lane.create_polygon(x, y, x+SIZE_LANE, y, x+int(SIZE_LANE/2), y+int(SIZE_LANE/2), fill=light, width=0)
            lane.create_polygon(x, y+SIZE_LANE, x+SIZE_LANE, y+SIZE_LANE, x+int(SIZE_LANE/2), y+int(SIZE_LANE/2), fill=shade, width=1, outline="black")
            lane.create_rectangle(x+2, y+2, x+SIZE_LANE-2, y+SIZE_LANE-2, fill=base, width=0)
    if yelt >= 1:
        ax = tetro[type_next][4]
        ay = tetro[type_next][5]
        base = color[str(type_next)]
        light = color_blend(base, "white")
        semi_shade = color_blend(base, "gray")
        shade = color_blend(base, "black")
        for i in range(int(len(tetro[type_next][0])/2)):
            x = (tetro[type_next][0][i*2]+ax+1)*SIZE_NEXT+88
            y = (tetro[type_next][0][i*2+1]+ay+1)*SIZE_NEXT
            nexted.create_rectangle(x, y, x+SIZE_NEXT, y+SIZE_NEXT, fill=semi_shade, width=1, outline=shade)
            nexted.create_polygon(x, y, x+SIZE_NEXT, y, x+int(SIZE_NEXT/2), y+int(SIZE_NEXT/2), fill=light, width=0)
            nexted.create_polygon(x, y+SIZE_NEXT, x+SIZE_NEXT, y+SIZE_NEXT, x+int(SIZE_NEXT/2), y+int(SIZE_NEXT/2), fill=shade, width=1, outline="black")
            nexted.create_rectangle(x+2, y+2, x+SIZE_NEXT-2, y+SIZE_NEXT-2, fill=base, width=0)

def drawHoldTetris():
    if type_hold != 100:
        ax = tetro[type_hold][4]
        ay = tetro[type_hold][5]
        base = color[str(type_hold)]
        light = color_blend(base, "white")
        semi_shade = color_blend(base, "gray")
        shade = color_blend(base, "black")
        for i in range(int(len(tetro[type_hold][0])/2)):
            x = (tetro[type_hold][0][i*2]+ax+1)*SIZE_NEXT+86
            y = (tetro[type_hold][0][i*2+1]+ay+1)*SIZE_NEXT
            holded.create_rectangle(x, y, x+SIZE_NEXT, y+SIZE_NEXT, fill=semi_shade, width=1, outline=shade)
            holded.create_polygon(x, y, x+SIZE_NEXT, y, x+int(SIZE_NEXT/2), y+int(SIZE_NEXT/2), fill=light, width=0)
            holded.create_polygon(x, y+SIZE_NEXT, x+SIZE_NEXT, y+SIZE_NEXT, x+int(SIZE_NEXT/2), y+int(SIZE_NEXT/2), fill=shade, width=1, outline="black")
            holded.create_rectangle(x+2, y+2, x+SIZE_NEXT-2, y+SIZE_NEXT-2, fill=base, width=0)

def drawField():
    for i in range(22):
        for j in range(13):
            if color[str(field[i+1][j])]!=color["40"] and color[str(field[i+1][j])]!=color["50"]:
                base = color[str(field[i+1][j])]
                light = color_blend(base, "white")
                semi_shade = color_blend(base, "gray")
                shade = color_blend(base, "black")
                can.create_rectangle(j*SIZE, i*SIZE, (j+1)*SIZE, (i+1)*SIZE, fill=semi_shade, width=1, outline=shade)
                can.create_polygon(j*SIZE, i*SIZE, (j+1)*SIZE, i*SIZE, j*SIZE+int(SIZE/2), i*SIZE+int(SIZE/2), fill=light, width=0)
                can.create_polygon(j*SIZE, (i+1)*SIZE, (j+1)*SIZE, (i+1)*SIZE, j*SIZE+int(SIZE/2), i*SIZE+int(SIZE/2), fill=shade, width=1, outline="black")
                can.create_rectangle(j*SIZE+3, i*SIZE+3, (j+1)*SIZE-3, (i+1)*SIZE-3, fill=base, width=0)
            else:
                can.create_rectangle(j*SIZE, i*SIZE, (j+1)*SIZE, (i+1)*SIZE, fill=color[str(field[i+1][j])], width=0)
    can.create_rectangle(5*SIZE+3, 3, 6*SIZE-2, 1*SIZE-2, width=2, outline="red")
    can.create_rectangle(3, 0, 12*SIZE, 21*SIZE, width=2, outline="black")
    
def drawNextField(yelt):
    if yelt >= 2:
        for i in range(int(1 + len(tetro[0][0])/2)*(yelt-1)):
            for j in range(int(1 + len(tetro[0][0])/2)):
                lane.create_rectangle(j*SIZE, i*SIZE, (j+1)*SIZE, (i+1)*SIZE, fill=color[str(50)], width=0)
    if yelt >= 1:
        for i in range(int(1 + len(tetro[0][0])/2)):
            for j in range(int(1 + len(tetro[0][0])/2)):
                nexted.create_rectangle(j*SIZE_NEXT+88, i*SIZE_NEXT, (j+1)*SIZE_NEXT+88, (i+1)*SIZE_NEXT, fill=color[str(50)], width=0)
    nexted.create_rectangle(88, 3, int(1 + len(tetro[0][0])/2)*SIZE_NEXT+88, int(1 + len(tetro[0][0])/2)*SIZE_NEXT, width=2, outline="black")
    
def drawHoldField():
    for i in range(int(1 + len(tetro[0][0])/2)):
        for j in range(int(1 + len(tetro[0][0])/2)):
            holded.create_rectangle(j*SIZE_NEXT+86, i*SIZE_NEXT, (j+1)*SIZE_NEXT+86, (i+1)*SIZE_NEXT, fill=color[str(50)], width=0)
    holded.create_rectangle(87, 3, int(1 + len(tetro[0][0])/2)*SIZE_NEXT+86, int(1 + len(tetro[0][0])/2)*SIZE_NEXT, width=2, outline="black")

def keyPress(event):   
    global moveX, moveY, replayed, pause, karl, parl, pause_time, scene, stone, type_0, type_1, type_2, type_3, type_4, type_5, score, tmini, field, spin, tspin, hdrop, dturn, turn, hardd, hcount, level, type_s, type_hold, type_c, type_next, hscore, line, rest_line
    afterX = moveX
    afterY = moveY
    afterTetro = []
    cond = []
    afterTetro.extend(tetro[type_c][turn])
    blocker = False
    parsed = False
    if scene == 0:
        if event.keysym=="Return" :
            pygame.mixer.music.play(-1)
            pause_s.play()
            sant.delete("all")
            sant.place_forget()
            game.place(x=0,y=0)
            game.create_image(455, 330, image=BG)
            geer.place(x=48,y=198)
            geer.create_rectangle(0,0,200,310,fill=color["background"])
            can.place(x=280, y=0)
            lab2.place(x=50, y=320)
            lab.place(x=80, y=350)
            lab3.place(x=50, y=380)
            lab1.place(x=80, y=410)
            lab10.place(x=50, y=260)
            lab9.place(x=80, y=290)
            if glob["hold"] == "true":
                holded.place(x=15, y=3)
                lab4a.place(x=17, y=5)
            if glob["show_next"] != "false":
                nexted.place(x=660, y=3)
                lab4.place(x=662, y=5)
                if yelt >= 2:
                    lane.place(x=760, y=150)
            if glob["show_high"] == "true":
                lab6.place(x=50, y=440)
                lab5.place(x=80, y=470)
            ver_lab.place_forget()
            menu_lab.place_forget()
            scene += 1
    elif scene == 1:
        if event.keysym==cont["M_Right"] :
            if hardd is False and pause is False:
                afterX += 1
                move_s.play()
                if judge(afterX, afterY - 1, afterTetro) is True and spin is True:
                    spin = False
                    tspin = False
                    tmini = False
        elif event.keysym==cont["M_Left"] :
            if hardd is False and pause is False:
                afterX -= 1
                move_s.play()
                if judge(afterX, afterY - 1, afterTetro) is True and spin is True:
                    spin = False
                    tspin = False
                    tmini = False
        elif event.keysym==cont["SDrop"] :
            if pause is False:
                afterY += 1
                stoke = judge(afterX, afterY, afterTetro) 
                if stoke is True:
                    spin = False
                    soft_s.play()
                    tspin = False
                    tmini = False
                    if glob["scoremode"] == "sega":
                        if level <= 2:
                            score += int(1)
                        elif level <= 4:
                            score += int(2)
                        elif level <= 6:
                            score += int(3)
                        elif level <= 8:
                            score += int(4)
                        else:
                            score += int(5)
                    elif glob["scoremode"] == "bps":
                        score += 0
                    else:
                        score += 1
        elif event.keysym==cont["HDrop"] :
            if pause is False:
                if glob["harddrop"] == "sonicdrop" or glob["harddrop"] == "harddrop":
                    Y = hard_drop(afterX, afterY, afterTetro)
                    if Y > 0:
                        spin = False
                        tspin = False
                        tmini = False
                        hdrop_s.play()
                        afterY += Y
        elif event.keysym==cont["T_Right"] :
            spin = True
            cout = []
            turn_s.play()
            if hardd is False and pause is False:
                parse = True
                if type_c in even_pic:
                    kick = wallkickC[turn+4]
                else:
                    kick = wallkickC[turn]
                turn += 1
                if turn > 3:
                    turn -= 4
                cout.extend(afterTetro)
                afterTetro.clear()
                afterTetro.extend(tetro[type_c][turn])
                if type_c not in sym_pic:
                    for (offX, offY) in kick:
                        parse = judge(afterX + offX, afterY + offY, afterTetro, 1, False)
                        if parse is True:
                            parsed = True
                            judge(afterX + offX, afterY + offY, afterTetro)
                            if kick.index((offX, offY)) < 4 and type_c in spin_pic:
                                tmini = True
                                tspin = False
                            elif kick.index((offX, offY)) >= 4 and type_c in spin_pic:
                                tmini = False
                                tspin = True
                            else:
                                tmini = False
                                tspin = False
                            break
                        elif parse is False:
                            parse = True
                            tspin = False
                            tmini = False
                    if parsed is False:
                        afterTetro.clear()
                        afterTetro.extend(cout)
                        turn -= 1
                        if turn < 0:
                            turn += 4
                        dturn += 1
                        if dturn <= 2 and glob["doublet"] == "true":
                            dturn = 0
                            turn += 2
                            if turn > 3:
                                turn -= 4
                            cout.extend(afterTetro)
                            afterTetro.clear()
                            afterTetro.extend(tetro[type_c][turn])
                            for (offX, offY) in kick:
                                parse = judge(afterX + offX, afterY + offY, afterTetro, 1, False)
                                if parse is True:
                                    parsed = True
                                    judge(afterX + offX, afterY + offY, afterTetro)
                                    if kick.index((offX, offY)) < 4 and type_c in spin_pic:
                                        tmini = True
                                        tspin = False
                                    elif kick.index((offX, offY)) >= 4 and type_c in spin_pic:
                                        tmini = False
                                        tspin = True
                                    else:
                                        tmini = False
                                        tspin = False
                                    break
                                elif parse is False:
                                    parse = True
                                    tspin = False
                            if parsed is False:
                                afterTetro.clear()
                                afterTetro.extend(cout)
                                turn -= 2
                                if turn < 0:
                                    turn += 4
                        else:
                            afterTetro.clear()
                            afterTetro.extend(cout)
                            tspin = False
                            tmini = False
                        tspin = False
                        tmini = False
        elif event.keysym==cont["T_Left"] :
            spin = True
            cout = []
            turn_s.play()
            if hardd is False and pause is False:
                parse = True
                if type_c in even_pic:
                    kick = wallkickCC[turn+4]
                else:
                    kick = wallkickCC[turn]
                turn -= 1
                if turn < 0:
                    turn += 4
                cout.extend(afterTetro)
                afterTetro.clear()
                afterTetro.extend(tetro[type_c][turn])
                if type_c not in sym_pic:
                    for (offX, offY) in kick:
                        parse = judge(afterX + offX, afterY + offY, afterTetro, 1, False)
                        if parse is True:
                            parsed = True
                            judge(afterX + offX, afterY + offY, afterTetro)
                            if kick.index((offX, offY)) < 4 and type_c in spin_pic:
                                tmini = True
                                tspin = False
                            elif kick.index((offX, offY)) >= 4 and type_c in spin_pic:
                                tmini = False
                                tspin = True
                            else:
                                tmini = False
                                tspin = False
                            break
                        elif parse is False:
                            parse = True
                            tspin = False
                    if parsed is False:
                        afterTetro.clear()
                        afterTetro.extend(cout)
                        turn += 1
                        if turn > 3:
                            turn -= 4
                        dturn -= 1
                        if dturn >= -2 and glob["doublet"] == "true":
                            dturn = 0
                            turn -= 2
                            if turn < 0:
                                turn += 4
                            cout.extend(afterTetro)
                            afterTetro.clear()
                            afterTetro.extend(tetro[type_c][turn])
                            for (offX, offY) in kick:
                                parse = judge(afterX + offX, afterY + offY, afterTetro, 1, False)
                                if parse is True:
                                    parsed = True
                                    judge(afterX + offX, afterY + offY, afterTetro)
                                    if kick.index((offX, offY)) < 4 and type_c in spin_pic:
                                        tmini = True
                                        tspin = False
                                    elif kick.index((offX, offY)) >= 4 and type_c in spin_pic:
                                        tmini = False
                                        tspin = True
                                    else:
                                        tmini = False
                                        tspin = False
                                    break
                                elif parse is False:
                                    parse = True
                                    tspin = False
                            if parsed is False:
                                afterTetro.clear()
                                afterTetro.extend(cout)
                                turn += 2
                                if turn > 3:
                                    turn -= 4
                        else:
                            afterTetro.clear()
                            afterTetro.extend(cout)
                            tspin = False
                            tmini = False
                            
        elif event.keysym==cont["Hold"] :
            if pause is False:
                if glob["hold"] == "true":
                    if hcount == 1:
                        hold_s.play()
                        moveX = 5
                        moveY = 1
                        afterX = moveX
                        afterY = moveY
                        afterTetro.clear()
                        hcount -= 1
                        hardd = False
                        turn = 0
                        dturn = 0
                        spin = False
                        tmini = False
                        tspin = False
                        if type_hold == 100:
                            type_hold = type_c
                            type_c = type_next
                            type_next = type_0
                            type_0 = type_1
                            type_1 = type_2
                            type_2 = type_3
                            type_3 = type_4
                            type_4 = type_5
                            type_5 = RMG()
                            afterTetro = []
                            afterTetro.extend(tetro[type_c][turn])
                        elif type_hold != 100:
                            type_s = type_hold
                            type_hold = type_c
                            type_c = type_s
                            type_s = 100
                            afterTetro = []
                            afterTetro.extend(tetro[type_c][turn])
                        
        elif event.keysym==cont["Reset"] :
            if pause is False:
                stone = True
                resume_replay()
                stone = False
                if replayed is True:
                    moveX = 5
                    moveY = 1
                    pygame.mixer.music.rewind()
                    afterX = moveX
                    afterY = moveY
                    replayed = False

        elif event.keysym==cont["pause"]:
            if pause is False:
                pause_s.play()
                karl = time.time()
                pygame.mixer.music.pause()
                lab12.place(x=330, y=50)
                pause = True
            elif pause is True:
                pause_s.play()
                lab12.place_forget()
                parl = time.time()
                pause_time += parl - karl
                parl = 0.0
                karl = 0.0
                pygame.mixer.music.unpause()
                can.after(50, gameLoop)
                pause = False
            
        if spin is False:     
            judge(afterX, afterY, afterTetro)   
 
def hard_drop(afterX, afterY, afterTetro, drop = True):
    global hdrop, score, hardd, add
    rest_grid = []
    for i in range(int(len(afterTetro)/2)):
        if type(afterTetro[i*2]) == float:
            add = 0.5
        else:
            add = 0
        x = int(afterTetro[i*2]+afterX + add)
        y = int(afterTetro[i*2+1]+afterY + add)
        j = 0
        while field[y+j+1][x]==50:
            j+=1
        rest_grid.append(j)

    if drop is True:
        hdrop = True
        if glob["harddrop"] == "harddrop":
            hardd = True
        elif glob["harddrop"] == "sonicdrop":
            hardd = False
        else:
            hardd = True
        if glob["scoremode"] == "bps":
            score += (min(rest_grid) - 1)
        else:
            score += 2*(min(rest_grid) - 1)
    return min(rest_grid) - 1
    
def judge(afterX, afterY, afterTetro, offsetY = 0, expand = True): 
    global moveX, moveY, turn, add, move_s
    result = True
    for i in range(int(len(afterTetro)/2)):
        if type(afterTetro[i*2]) == float:
            add = 0.5
        else:
            add = 0
        x = int(afterTetro[i*2]+afterX + add)
        y = int(afterTetro[i*2+1]+afterY + add)
        try:
            if field[y+1][x]!=50 :
                result = False
        except IndexError:
            result = False
                
    if result==True and expand==True:
        moveX = afterX
        moveY = afterY+offsetY
    return result

def t_turn(turn):
    if turn == 0:
        return [0, 1]
    elif turn == 1:
        return [1, 3]
    elif turn == 2:
        return [2, 3]
    elif turn == 3:
        return [0, 2]
    
def tspin_perser(x, y, turn, tspin, tmini):
    if glob["rotation"] != "original" and glob["rotation"] != "sega" and glob["rotation"] != "left nrs" and glob["rotation"] != "right nrs" and glob["rotation"] != "ars":
        try:
            slot = [field[y][x-1],field[y][x+1],field[y+2][x-1],field[y+2][x+1]]
        except IndexError:
            if x+1 > 11 and y+2 > 21:
                slot = [field[y][x-1],0,0,0]
            elif x+1 > 11:
                slot = [field[y][x-1],0,field[y+2][x-1],0]
            elif y+2 > 21:
                slot = [field[y][x-1],field[y][x+1],0,0]
        rot = t_turn(turn)
        spe = True
        if slot.count(50) > 1:
            return "false"
        elif slot.count(50) == 1:
            for i in range(2):
                if slot[rot[i]] == 50:
                    spe = False
                    break
        if spe is True:
            if tspin is True or tmini is True:
                return "spin"
        elif spe is False:
            if tmini is True:
                return "mini"
        else:
            return "false"
    else:
        return "false"
    
def dropTetris(hard=False):
    global moveX, moveY, pc, add, replayed, scene, stone, snow, type_0, type_1, type_2, type_3, type_4, type_5, tspin, pause, spin, tmini, btb, dturn, turn, hcount, hardd, type_c, type_next, combo, hdrop, timer, rest_line, line, listed, score, level, hscore
    afterTetro = []
    chain = []
    field_a = []
    field_b = []
    afterTetro.extend(tetro[type_c][turn])
    chain.extend(tetro[type_c][turn])
    if snow != 0:
        timer = snow
        snow = 0
    if pause is True or scene == 0 or stone is True:
        result = judge(moveX, moveY, afterTetro)
    else:
        result = judge(moveX, moveY+1, afterTetro)
    if spin is False and (result==False or hard is True):
        field_a = field
        if type_c in even_pic:
            add = 0.5
        else:
            add = 0
        for i in range(int(len(tetro[type_c][turn])/2)):
            x = int(tetro[type_c][turn][i*2]+moveX+add)
            y = int(tetro[type_c][turn][i*2+1]+moveY+add)
            field[y+1][x] = type_c
            if type_c in spin_pic and spin is True:
                tspin_perse = tspin_perser(moveX, moveY+1, turn, tspin, tmini)
                if tspin_perse == "mini":
                    tmini = True
                    tspin = False
                elif tspin_perse == "spin":
                    tspin = True
                    tmini = False
                else:
                    tspin = False
                    tmini = False
        if hardd is False:
            land_s.play()
        hardd = False
        field_b = field
        deleteLine()
        afterTetro = []
        hcount = 1
        if field == field0:
            pc = True
            perfect_s.play()
        type_c = type_next
        type_next = type_0
        type_0 = type_1
        type_1 = type_2
        type_2 = type_3
        type_3 = type_4
        type_4 = type_5
        type_5 = RMG()
        moveX = 5
        moveY = 1
        turn = 0
        dturn = 0
        if glob["scoremode"] == "modern":
            if listed[-1] != 0:
                if tspin is True:
                    tspin_s.play()
                    if listed[-1] == 1:
                        if pc is True:
                            score += int(800 * level)
                        score += int(800 * level * btb)
                        if btb == 1.5:
                            perfect_s.play()
                        btb = 1.5
                    elif listed[-1] == 2:
                        if pc is True:
                            score += int(1200 * level)
                        score += int(1200 * level * btb)
                        if btb == 1.5:
                            perfect_s.play()
                        btb = 1.5
                    elif listed[-1] == 3:
                        if pc is True:
                            score += int(1800 * level)
                        score += int(1600 * level * btb)
                        if btb == 1.5:
                            perfect_s.play()
                        btb = 1.5
                    elif listed[-1] >= 4:
                        if pc is True:
                            score += int(2000 * level * btb) + int(400 * (listed[-1] - 4) * level * btb)
                            if btb != 1.0:
                                score += int(200 * level)
                        score += int(800 * level * btb) + int(400 * (listed[-1] - 4) * level * btb)
                        btb = 1.5
                elif tmini is True:
                    tspin_s.play()
                    if listed[-1] == 1:
                        if pc is True:
                            score += int(800 * level)
                        score += int(200 * level * btb)
                        if btb == 1.5:
                            perfect_s.play()
                        btb = 1.5
                    elif listed[-1] == 2:
                        if pc is True:
                            score += int(1200 * level)
                        score += int(400 * level * btb)
                        if btb == 1.5:
                            perfect_s.play()
                        btb = 1.5
                    elif listed[-1] == 3:
                        if pc is True:
                            score += int(1800 * level)
                        score += int(800 * level * btb)
                        if btb == 1.5:
                            perfect_s.play()
                        btb = 1.5
                    elif listed[-1] >= 4:
                        if pc is True:
                            score += int(2000 * level * btb) + int(400 * (listed[-1] - 4) * level * btb)
                            if btb != 1.0:
                                score += int(200 * level)
                        score += int(1200 * level * btb) + int(400 * (listed[-1] - 4) * level * btb)
                        if btb == 1.5:
                            perfect_s.play()
                        btb = 1.5
                else:
                    if listed[-1] == 1:
                        if pc is True:
                            score += int(800 * level)
                        score += int(100 * level)
                        uline_s.play()
                        btb = 1.0
                    elif listed[-1] == 2:
                        if pc is True:
                            score += int(1200 * level)
                        score += int(300 * level)
                        dline_s.play()
                        btb = 1.0
                    elif listed[-1] == 3:
                        if pc is True:
                            score += int(1800 * level)
                        score += int(500 * level)
                        tline_s.play()
                        btb = 1.0
                    elif listed[-1] == 4:
                        if pc is True:
                            score += int(2000 * level * btb)
                            if btb != 1.0:
                                score += int(200 * level)
                        score += int(800 * level * btb)
                        qline_s.play()
                        if btb == 1.5:
                            perfect_s.play()
                        btb = 1.5
                    elif listed[-1] >= 5:
                        if pc is True:
                            score += int(2000 * level * btb) + int(400 * (listed[-1] - 4) * level * btb)
                            if btb != 1.0:
                                score += int(200 * level)
                        score += int(800 * level * btb) + int(400 * (listed[-1] - 4) * level * btb)
                        qline_s.play()
                        if btb == 1.5:
                            perfect_s.play()
                        btb = 1.5
                if len(listed) > 1:
                    combo = len(listed) - 1
                    if combo == 1:
                        c1_s.play()
                    elif combo == 2:
                        c2_s.play()
                    elif combo == 3:
                        c3_s.play()
                    elif combo == 4:
                        c4_s.play()
                    elif combo == 5:
                        c5_s.play()
                    elif combo >= 6:
                        c6_s.play()
                    score += int(50 * level * (len(listed) - 1))
                listed.append(0)
            elif listed[-1] == 0:
                if tspin is True:
                    tspin_s.play()
                    score += int(400 * level)
                elif tmini is True:
                    tspin_s.play()
                    score += int(100 * level)
                listed = [0]
                combo = 0
        elif glob["scoremode"] == "bps":
            if listed[-1] != 0:
                if listed[-1] == 1:
                    score += int(40)
                    uline_s.play()
                    btb = 1.0
                elif listed[-1] == 2:
                    score += int(100)
                    dline_s.play()
                    btb = 1.0
                elif listed[-1] == 3:
                    score += int(300)
                    tline_s.play()
                    btb = 1.0
                elif listed[-1] == 4:
                    score += int(1200)
                    qline_s.play()
                    btb = 1.5
                elif listed[-1] >= 5:
                    score += int(1200) + int(400 * (listed[-1] - 4))
                    qline_s.play()
                    btb = 1.5
                if len(listed) > 1:
                    combo = len(listed) - 1
                    if combo == 1:
                        c1_s.play()
                    elif combo == 2:
                        c2_s.play()
                    elif combo == 3:
                        c3_s.play()
                    elif combo == 4:
                        c4_s.play()
                    elif combo == 5:
                        c5_s.play()
                    elif combo >= 6:
                        c6_s.play()
                listed.append(0)
            elif listed[-1] == 0:
                listed = [0]
        elif glob["scoremode"] == "sega":
            if listed[-1] != 0:
                if listed[-1] == 1:
                    if level <= 2:
                        score += int(100)
                    elif level <= 4:
                        score += int(200)
                    elif level <= 6:
                        score += int(300)
                    elif level <= 8:
                        score += int(400)
                    else:
                        score += int(500)
                    uline_s.play()
                    btb = 1.0
                elif listed[-1] == 2:
                    if level <= 2:
                        score += int(400)
                    elif level <= 4:
                        score += int(800)
                    elif level <= 6:
                        score += int(1200)
                    elif level <= 8:
                        score += int(1600)
                    else:
                        score += int(2000)
                    dline_s.play()
                    btb = 1.0
                elif listed[-1] == 3:
                    if level <= 2:
                        score += int(900)
                    elif level <= 4:
                        score += int(1800)
                    elif level <= 6:
                        score += int(2700)
                    elif level <= 8:
                        score += int(3600)
                    else:
                        score += int(4500)
                    tline_s.play()
                    btb = 1.0
                elif listed[-1] == 4:
                    if level <= 2:
                        score += int(2000)
                    elif level <= 4:
                        score += int(4000)
                    elif level <= 6:
                        score += int(6000)
                    elif level <= 8:
                        score += int(8000)
                    else:
                        score += int(10000)
                    qline_s.play()
                    btb = 1.5
                elif listed[-1] >= 5:
                    if level <= 2:
                        score += int(100 * listed[-1] * listed[-1])
                    elif level <= 4:
                        score += int(100 * listed[-1] * listed[-1] * 2)
                    elif level <= 6:
                        score += int(100 * listed[-1] * listed[-1] * 3)
                    elif level <= 8:
                        score += int(100 * listed[-1] * listed[-1] * 4)
                    else:
                        score += int(100 * listed[-1] * listed[-1] * 5)
                    qline_s.play()
                    btb = 1.5
                if len(listed) > 1:
                    combo = len(listed) - 1
                    if combo == 1:
                        c1_s.play()
                    elif combo == 2:
                        c2_s.play()
                    elif combo == 3:
                        c3_s.play()
                    elif combo == 4:
                        c4_s.play()
                    elif combo == 5:
                        c5_s.play()
                    elif combo >= 6:
                        c6_s.play()
                listed.append(0)
            elif listed[-1] == 0:
                listed = [0]
        elif glob["scoremode"] == "nes":
            if listed[-1] != 0:
                if listed[-1] == 1:
                    score += int(40 * level)
                    uline_s.play()
                    btb = 1.0
                elif listed[-1] == 2:
                    score += int(100 * level)
                    dline_s.play()
                    btb = 1.0
                elif listed[-1] == 3:
                    score += int(300 * level)
                    tline_s.play()
                    btb = 1.0
                elif listed[-1] == 4:
                    score += int(1200 * level)
                    qline_s.play()
                    btb = 1.5
                elif listed[-1] >= 5:
                    score += int(1200 * level) + int(400 * (listed[-1] - 4) * level)
                    qline_s.play()
                    btb = 1.5
                if len(listed) > 1:
                    combo = len(listed) - 1
                    if combo == 1:
                        c1_s.play()
                    elif combo == 2:
                        c2_s.play()
                    elif combo == 3:
                        c3_s.play()
                    elif combo == 4:
                        c4_s.play()
                    elif combo == 5:
                        c5_s.play()
                    elif combo >= 6:
                        c6_s.play()
                listed.append(0)
            elif listed[-1] == 0:
                listed = [0]
        else:
            if listed[-1] != 0:
                if tspin is True:
                    tspin_s.play()
                    if listed[-1] == 1:
                        if pc is True:
                            score += int(800 * level)
                        score += int(800 * level * btb)
                        if btb == 1.5:
                            perfect_s.play()
                        btb = 1.5
                    elif listed[-1] == 2:
                        if pc is True:
                            score += int(1200 * level)
                        score += int(1200 * level * btb)
                        if btb == 1.5:
                            perfect_s.play()
                        btb = 1.5
                    elif listed[-1] == 3:
                        if pc is True:
                            score += int(1800 * level)
                        score += int(1600 * level * btb)
                        if btb == 1.5:
                            perfect_s.play()
                        btb = 1.5
                    elif listed[-1] >= 4:
                        if pc is True:
                            score += int(2000 * level * btb) + int(400 * (listed[-1] - 4) * level * btb)
                            if btb != 1.0:
                                score += int(200 * level)
                        score += int(800 * level * btb) + int(400 * (listed[-1] - 4) * level * btb)
                        btb = 1.5
                elif tmini is True:
                    tspin_s.play()
                    if listed[-1] == 1:
                        if pc is True:
                            score += int(800 * level)
                        score += int(200 * level * btb)
                        if btb == 1.5:
                            perfect_s.play()
                        btb = 1.5
                    elif listed[-1] == 2:
                        if pc is True:
                            score += int(1200 * level)
                        score += int(400 * level * btb)
                        if btb == 1.5:
                            perfect_s.play()
                        btb = 1.5
                    elif listed[-1] == 3:
                        if pc is True:
                            score += int(1800 * level)
                        score += int(800 * level * btb)
                        if btb == 1.5:
                            perfect_s.play()
                        btb = 1.5
                    elif listed[-1] >= 4:
                        if pc is True:
                            score += int(2000 * level * btb) + int(400 * (listed[-1] - 4) * level * btb)
                            if btb != 1.0:
                                score += int(200 * level)
                        score += int(1200 * level * btb) + int(400 * (listed[-1] - 4) * level * btb)
                        if btb == 1.5:
                            perfect_s.play()
                        btb = 1.5
                else:
                    if listed[-1] == 1:
                        if pc is True:
                            score += int(800 * level)
                        score += int(100 * level)
                        uline_s.play()
                        btb = 1.0
                    elif listed[-1] == 2:
                        if pc is True:
                            score += int(1200 * level)
                        score += int(300 * level)
                        dline_s.play()
                        btb = 1.0
                    elif listed[-1] == 3:
                        if pc is True:
                            score += int(1800 * level)
                        score += int(500 * level)
                        tline_s.play()
                        btb = 1.0
                    elif listed[-1] == 4:
                        if pc is True:
                            score += int(2000 * level * btb)
                            if btb != 1.0:
                                score += int(200 * level)
                        score += int(800 * level * btb)
                        qline_s.play()
                        if btb == 1.5:
                            perfect_s.play()
                        btb = 1.5
                    elif listed[-1] >= 5:
                        if pc is True:
                            score += int(2000 * level * btb) + int(400 * (listed[-1] - 4) * level * btb)
                            if btb != 1.0:
                                score += int(200 * level)
                        score += int(800 * level * btb) + int(400 * (listed[-1] - 4) * level * btb)
                        qline_s.play()
                        if btb == 1.5:
                            perfect_s.play()
                        btb = 1.5
                if len(listed) > 1:
                    combo = len(listed) - 1
                    if combo == 1:
                        c1_s.play()
                    elif combo == 2:
                        c2_s.play()
                    elif combo == 3:
                        c3_s.play()
                    elif combo == 4:
                        c4_s.play()
                    elif combo == 5:
                        c5_s.play()
                    elif combo >= 6:
                        c6_s.play()
                    score += int(50 * level * (len(listed) - 1))
                listed.append(0)
            elif listed[-1] == 0:
                if tspin is True:
                    tspin_s.play()
                    score += int(400 * level)
                elif tmini is True:
                    tspin_s.play()
                    score += int(100 * level)
                listed = [0]
                combo = 0
        tspin = False
        tmini = False
        if score >= hscore:
            hscore = score
    hdrop = False
    spin = False
    if result is False and timer < 500:
        snow = timer
        timer = 500
    can.after(timer, dropTetris)

    if glob["leveling"] == "normal":
        if rest_line <= 0:
            level_s.play()
            level += 1
            line -= 10
            rest_line += 10
            if glob["gamemode"] == "original" or glob["gamemode"] == "orlv15" or glob["gamemode"] == "limor" or glob["gamemode"] == "lolv15":
                timer = int(1000*((0.8-((level-1)*0.007))**(level-1)))
            else:
                timer = 850 - (50 * level)
    elif glob["leveling"] == "world":
        if line >= 5 * level:
            level_s.play()
            line -= 5 * level
            level += 1
            rest_line += 5 * level
            if glob["gamemode"] == "original" or glob["gamemode"] == "orlv15" or glob["gamemode"] == "limor" or glob["gamemode"] == "lolv15":
                timer = int(1000*((0.8-((level-1)*0.007))**(level-1)))
            else:
                timer = 850 - (50 * level)
    if glob["gamemode"] == "original" or glob["gamemode"] == "orlv15":
        if level > 9 :
            timer = int(1000*((0.8-(8*0.007))**8))
    elif glob["gamemode"] == "normal" or glob["gamemode"] == "level15":
        if timer < 150:
            timer = 150
    elif glob["gamemode"] == "limless" or glob["gamemode"] == "lesslv15":
        if timer < 10:
            timer = 10
            
def deleteLine():
    global level, line, listed, score, rest_line, pause_time, turn, log_name, former_time, start
    for i in range(1, 21):
        if 50 not in field[i]:
            for j in range(i):
                for k in range(12):
                    field[i-j][k] = field[i-j-1][k]
            listed[-1] = listed[-1] + 1
            line += 1
            rest_line -= 1
            turn = 0
    if glob["gamemode"] == "level15" or glob["gamemode"] == "lesslv15":
        if level == 16:
            pygame.mixer.music.stop()
            end = time.time()
            spent = float(end - start - pause_time)
            spented_time = spent_time(spent)
            if log_name != "":
                if former_time >= spent:
                    try:
                        log["LOG"][log_name + "_score"] = str(score)
                        log["LOG"][log_name + "_time"] = spented_time
                        with open("pytetris.log", "w") as file:
                            log.write(file)
                    except KeyError:
                        with open("pytetris.log", "a+") as file:
                            file.write(log_name + "_score = " + str(score) + "\n")
                            file.write(log_name + "_time = " + spented_time + "\n")
            messagebox.showinfo("information", "CONGRATULATION !\nYOU'VE PASSED LEVEL 15 !!\nTIME:"+spented_time+"\nSCORE:" + str(score))
            exit_replay()
    if 50 != field[1][5]:
        pygame.mixer.music.stop()
        if log_name != "":
            end = time.time()
            spent = float(end - start - pause_time)
            spented_time = spent_time(spent)
            if score >= hscore:
                try:
                    log["LOG"][log_name + "_score"] = str(score)
                    log["LOG"][log_name + "_time"] = spented_time
                    with open("pytetris.log", "w") as file:
                        log.write(file)
                except KeyError:
                    with open("pytetris.log", "a+") as file:
                        file.write(log_name + "_score = " + str(score) + "\n")
                        file.write(log_name + "_time = " + spented_time + "\n")
        messagebox.showinfo("information", "GAME OVER !\nSCORE:" + str(score) + "\nTIME:"+spented_time+"\nLEVEL:" + str(level))
        exit_replay()

def resume_replay():
    global moveX, moveY, replayed, pause, karl, parl, pause_time, tetro_bag, scene, stone, type_0, type_1, type_2, type_3, type_4, type_5, score, tmini, field, spin, tspin, hdrop, dturn, turn, hardd, hcount, level, type_s, type_hold, type_c, type_next, hscore, line, rest_line
    messagebox = tk.messagebox.askquestion('Replay/Resume','Do you want to reset?', icon='question')
    if messagebox == 'yes':
        replayed = True
        moveX = 5
        moveY = 1
        tetro_bag = [i for i in range(0, tl)]
        btb = 1.0
        pc = False
        hdrop = False
        hardd = False
        tspin = False
        spin = False
        tmini = False
        log.read('pytetris.log', encoding='utf-8')
        start = time.time()

        hcount = 1
        combo = 0
        type_hold = 100
        type_s = 100
        turn = 0
        karl = 0.0
        parl = 0.0
        pause_time = 0.0
        
        type_c = RMG()
        type_next = RMG()
        type_0 = RMG()
        type_1 = RMG()
        type_2 = RMG()
        type_3 = RMG()
        type_4 = RMG()
        type_5 = RMG()
        
            
        level = int(glob["SLevel"])

        if glob["gamemode"] == "original" or glob["gamemode"] == "orlv15" or glob["gamemode"] == "limor" or glob["gamemode"] == "lolv15":
            timer = int(1000*((0.8-((level-1)*0.007))**(level-1)))
        else:
            timer = 850 - (50 * level)
        if glob["gamemode"] == "original" or glob["gamemode"] == "orlv15":
            if level > 9 :
                timer = int(1000*((0.8-(8*0.007))**8))
        elif glob["gamemode"] == "normal" or glob["gamemode"] == "level15":
            if timer < 150:
                timer = 150
        elif glob["gamemode"] == "limless" or glob["gamemode"] == "lesslv15":
            if timer < 10:
                timer = 10
                
        score = 0
        line = 0

        if glob["leveling"] == "normal":
            rest_line = 10 * level
        elif glob["leveling"] == "world":
            rest_line = 5 * level
        else:
            rest_line = 10
            
        listed = [0]

        if log_name != "":
            try:
                hscore = int(log["LOG"][log_name+"_score"])
                former_time = num_time(log["LOG"][log_name+"_time"])
            except KeyError:
                hscore = 0
                former_time = 0.0
        else:
            hscore = 0
            former_time = 0.0
        if score >= hscore:
            hscore = score
        field = make_field()
        try:
            afterTetro.clear()
            afterTetro.extend(tetro[type_c][turn])
        except NameError:
            pass
    else:
        pass
        
def exit_replay():
    global moveX, moveY, pause, pause_time, karl, parl, tetro_bag, scene, stone, type_0, type_1, type_2, type_3, type_4, type_5, score, tmini, field, spin, tspin, hdrop, dturn, turn, hardd, hcount, level, type_s, type_hold, type_c, type_next, hscore, line, rest_line
    messagebox = tk.messagebox.askquestion('Replay/Exit','Do you want to play again?', icon='question')
    if messagebox == 'yes':
        moveX = 5
        moveY = 1
        afterX = moveX
        afterY = moveY
        tetro_bag = [i for i in range(0, tl)]
        btb = 1.0
        pc = False
        hdrop = False
        hardd = False
        tspin = False
        spin = False
        tmini = False
        pygame.mixer.music.play()
        log.read('pytetris.log', encoding='utf-8')
        start = time.time()

        hcount = 1
        combo = 0
        type_hold = 100
        type_s = 100
        turn = 0
        karl = 0.0
        parl = 0.0
        pause_time = 0.0
        
        type_c = RMG()
        type_next = RMG()
        type_0 = RMG()
        type_1 = RMG()
        type_2 = RMG()
        type_3 = RMG()
        type_4 = RMG()
        type_5 = RMG()
        
            
        level = int(glob["SLevel"])

        if glob["gamemode"] == "original" or glob["gamemode"] == "orlv15" or glob["gamemode"] == "limor" or glob["gamemode"] == "lolv15":
            timer = int(1000*((0.8-((level-1)*0.007))**(level-1)))
        else:
            timer = 850 - (50 * level)
        if glob["gamemode"] == "original" or glob["gamemode"] == "orlv15":
            if level > 9 :
                timer = int(1000*((0.8-(8*0.007))**8))
        elif glob["gamemode"] == "normal" or glob["gamemode"] == "level15":
            if timer < 150:
                timer = 150
        elif glob["gamemode"] == "limless" or glob["gamemode"] == "lesslv15":
            if timer < 10:
                timer = 10
                
        score = 0
        line = 0

        if glob["leveling"] == "normal":
            rest_line = 10 * level
        elif glob["leveling"] == "world":
            rest_line = 5 * level
        else:
            rest_line = 10
            
        listed = [0]

        if log_name != "":
            try:
                hscore = int(log["LOG"][log_name+"_score"])
                former_time = num_time(log["LOG"][log_name+"_time"])
            except KeyError:
                hscore = 0
                former_time = 0.0
        else:
            hscore = 0
            former_time = 0.0
        if score >= hscore:
            hscore = score
        field = make_field()
        try:
            afterTetro.clear()
            afterTetro.extend(tetro[type_c][turn])
        except NameError:
            pass
    else:
        win.destroy()
        exit()
def exit_game():
    global moveX, moveY, pause, tetro_bag, scene, stone, type_0, type_1, type_2, type_3, type_4, type_5, score, tmini, field, spin, tspin, hdrop, dturn, turn, hardd, hcount, level, type_s, type_hold, type_c, type_next, hscore, line, rest_line
    messagebox = tk.messagebox.askquestion('Exit','Do you want to end game?', icon='question')
    if messagebox == 'yes':
        pygame.mixer.music.stop()
        win.destroy()
        exit()
    else:
        pass
        
def about():
    sub_win = tk.Toplevel()
    sub_win.geometry("300x100")
    label_sub = tk.Label(sub_win, text="PyTetris\nMade by JackT 2022")
    label_sub.pack()
   
win = tk.Tk()
men = tk.Menu(win)
win.config(menu=men) 
menu_file = tk.Menu(win)
men.add_cascade(label='Help', menu=menu_file)
menu_file.add_command(label='About PyTetris', command=about) 
#men.add_cascade(label='Options', menu=menu_file)
#menu_file.add_command(label='Option', command=open_file)

win.configure(bg=color["Background"])
try:
    win.iconbitmap(default="icon.ico")
except tk.TclError:
    pass
win.geometry("910x660")
win.resizable(False, False)
win.title("PyTETRIS")

sant = tk.Canvas(win, width=910, height=660, bg=color["background"])
game = tk.Canvas(win, width=910, height=660)
can = tk.Canvas(win, width=12*SIZE, height=21*SIZE, bg=color["background"])
geer = tk.Canvas(win, width=200, height=310, bg=color["background"])
nexted = tk.Canvas(win, width=int(1 + len(tetro[0][0])/2)*SIZE_NEXT+88, height=int(1 + len(tetro[0][0])/2)*SIZE_NEXT, bg=color["background"])
holded = tk.Canvas(win, width=int(1 + len(tetro[0][0])/2)*SIZE_NEXT+86, height=int(1 + len(tetro[0][0])/2)*SIZE_NEXT, bg=color["background"])
if glob["show_next"] != "false":
    yelt = int(glob["show_next"])
    if yelt < 2:
        yelt = 1
else:
    yelt = 1
lane = tk.Canvas(win, width=int(1 + len(tetro[0][0])/2)*SIZE_LANE, height=int(1 + len(tetro[0][0])/2)*SIZE_LANE*(yelt-1), bg=color["background"])
var = tk.StringVar()
var1 = tk.StringVar()
var2 = tk.StringVar()
var3 = tk.StringVar()
var4 = tk.StringVar()
lab = tk.Label(win, textvariable=var, fg=color["Font"], font=(glob["Font"], "20"), bg=color["Background"])   
lab1 = tk.Label(win, textvariable=var1, fg=color["Font"], font=(glob["Font"], "20"), bg=color["Background"])   
lab2 = tk.Label(win, text="#LEVEL", fg=color["Font"], font=(glob["Font"], "20"), bg=color["Background"])
lab3 = tk.Label(win, text="#SCORE", fg=color["Font"], font=(glob["Font"], "20"), bg=color["Background"])
lab4 = tk.Label(win, text="NEXT>", fg=color["Font"], font=(glob["Font"], "20"), bg=color["Background"])
lab4a = tk.Label(win, text="HOLD>", fg=color["Font"], font=(glob["Font"], "20"), bg=color["Background"])
lab5 = tk.Label(win, textvariable=var2, fg=color["Font"], font=(glob["Font"], "20"), bg=color["Background"])
lab6 = tk.Label(win, text="#HIGH SCORE", fg=color["Font"], font=(glob["Font"], "20"), bg=color["Background"])
lab9 = tk.Label(win, textvariable=var3, fg=color["Font"], font=(glob["Font"], "20"), bg=color["Background"])   
lab10 = tk.Label(win, text="#LINES", fg=color["Font"], font=(glob["Font"], "20"), bg=color["Background"])
lab12 = tk.Label(win, text="*PAUSE", fg=color["Font"], font=(glob["Font"], "20"), bg=color["Background"])   
lab13 = tk.Label(win, textvariable=var4, fg=color["Font"], font=(glob["Font"], "20"), bg=color["Background"])   
lab14 = tk.Label(win, text="!COMBO!", fg=color["Font"], font=(glob["Font"], "20"), bg=color["Background"])

title = tk.PhotoImage(file = "title.png")
Logo = tk.PhotoImage(file = "icon_small.png")
BG = tk.PhotoImage(file = "bg.png")
menu_lab = tk.Label(win, text="Press Enter to Start", fg=color["Font"], font=(glob["Font"], "30"), bg=color["Background"])
ver_lab = tk.Label(win, text="v" + version + " @JackT 2022", fg=color["Font"], font=(glob["Font"], "10"), bg=color["Background"])
lab11 = tk.Label(win, text=glob["gamemode"].upper() + " MODE", fg=color["Font"], font=(glob["Font"], "20"), bg=color["Background"])   


win.bind("<Any-KeyPress>", keyPress)

def gameLoop():
    global pause, yelt, scene
    if scene == 0:
        drawField()
        drawNextField(yelt)
        if glob["hold"] == "true":
            holded.delete("all")
            drawHoldField()
    elif scene == 1:
        can.delete("all")
        nexted.delete("all")
        geer.delete("all")
        if yelt >= 2:
            lane.delete("all")
        var.set(level)
        var1.set(score)
        var2.set(hscore)
        var3.set(rest_line)
        var4.set(combo)
        drawField()
        drawNextField(yelt)
        if glob["hold"] == "true":
            holded.delete("all")
            drawHoldField()
            drawHoldTetris()
        drawGhostTetris()
        drawTetris()
        drawNextTetris(yelt)
        if combo != 0:
            lab14.place(x=50, y=200)
            lab13.place(x=80, y=230)
        elif combo == 0:
            lab13.place_forget()
            lab14.place_forget()
    if pause is False:
        can.after(30, gameLoop)


sant.place(x=0,y=0)
sant.create_image(455, 330, image=title)
sant.create_image(455, 220, image=Logo)
ver_lab.place(x=700, y=615)
menu_lab.place(x=210, y=550)
start = time.time()
gameLoop()
dropTetris()
win.mainloop()
