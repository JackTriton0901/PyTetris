import matplotlib
import configparser
    
def color_blend(color1, color2):
    try:
        color_get1 = (matplotlib.colors.cnames[color1.replace(" ","")]).replace("#","")
    except KeyError:
        color_get1 = color1.replace("#","")
    try:
        color_get2 = (matplotlib.colors.cnames[color2.replace(" ","")]).replace("#","")
    except KeyError:
        color_get2 = color2.replace("#","")
    colorR = int((int(color_get1[0:2], 16) + int(color_get2[0:2], 16)) / 2)
    colorG = int((int(color_get1[2:4], 16) + int(color_get2[2:4], 16)) / 2)
    colorB = int((int(color_get1[4:6], 16) + int(color_get2[4:6], 16)) / 2)
    color_return = "#{:02X}{:02X}{:02X}".format(colorR, colorG, colorB) #"#{:0>X}".format(int((color_get1 + color_get2)/2))
    return color_return

def spent_time(spent):
    hour = 0
    minute = 0
    second = 0
    mili = 0.0
    text = ""
    if spent >= 359999.99:
        hour = 99
        minute = 59
        second = 59
        mili = 99
        text = "+99:59:59.99"
    if spent >= 3600:
        hour += int(spent // 3600)
        spent -= 3600 * hour
        text += "{:02d}:".format(hour)
    if spent >= 60:
        minute += int(spent // 60)
        spent -= 60 * minute
        text += "{:02d}:".format(minute)
    second = int(spent)
    mili = int((spent - second) * 100)
    text += "{:02d}.{:02d}".format(second, mili)
    return text

def num_time(spent):
    hour = 0
    minute = 0
    second = 0
    mili = 0.0
    ret = 0.0
    if spent == "+99:59:59.99":
        ret = 359999.99
    else:
        if spent.count(":") == 2:
            hour = int(spent[0:2])
            minute = int(spent[3:5])
            second = int(spent[6:8])
            mili = int(spent[9:11])
        elif spent.count(":") == 1:
            minute = int(spent[0:2])
            second = int(spent[3:5])
            mili = int(spent[6:8])
        else:
            second = int(spent[0:2])
            mili = int(spent[3:5])
        ret = hour*3600+minute*60+second+mili/100
    return ret

def log_namer(config):
    text = ""
    output = True
    glob = config["GLOBAL"]
    harddrop = ["false","harddrop","sonicdrop"]
    rotation = ["srs","pentomino","arika srs","tbrs","trrs","ars tbrs",
                "dtet","ars","sega","left nrs","right nrs","original"]
    scoremode = ["modern","bps","sega","nes"]
    gamemode = ["original","orlv15","normal","level15","limless","lesslv15",
                "limor","lolv15"]
    
    if glob["show_next"] == "false":
        text += "0"
    else:
        if int(glob["show_next"]) > 7:
            rot = 7
        else:
            rot = int(glob["show_next"])
        text += "{:X}".format(rot)
    if glob["harddrop"] in harddrop:
        text += "{:X}".format(harddrop.index(glob["harddrop"]))
    else:
        text += "0"
    if "15" not in glob["gamemode"]:
        if int(glob["slevel"]) > 15:
            output = False
        else:
            text += "{:02X}".format(int(glob["slevel"]))
    else:
        if int(glob["slevel"]) > 255:
            slevel = 255
        else:
            slevel = int(glob["slevel"])
        text += "{:02X}".format(slevel)
    if glob["rotation"] in rotation:
        text += "{:02X}".format(rotation.index(glob["rotation"]))
    else:
        text += "00"
    if glob["doublet"] == "true":
        text += "1"
    else:
        text += "0"
    if glob["leveling"] == "world":
        text += "1"
    else:
        text += "0"
    if glob["hold"] == "true":
        text += "1"
    else:
        text += "0"
    if glob["scoremode"] in scoremode:
        text += "{:X}".format(scoremode.index(glob["scoremode"]))
    else:
        text += "0"
    if glob["gamemode"] in gamemode:
        text += "{:02X}".format(gamemode.index(glob["gamemode"]))
    else:
        text += "00"
    if output is False:
        return ""
    else:
        return text
    
