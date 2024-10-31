import random
import argparse
import math
import sys
import traceback

#############################
# Tables as weighted arrays #
#############################

# Cost Categories
COSTCAT = [10,20,50,100,500,1000,5000]

# Manufacturers - [Name, Note] - 1-100
MANUFACTURER = (
    [["A local Tech","-"]]*10 +
    [["A nomad weaponsmith","-"]]*2 +
    [["Arasaka","-"]]*8 +
    [["BudgetArms","Probably Poor Quality"]]*3 +
    [["Centurion Essentials","-"]]*2 +
    [["Chadran Arms","-"]]*2 +
    [["Constitutional Arms","-"]]*2 +
    [["Dai Lung","Probably Poor Quality"]]*2 +
    [["Eagletech","Probably a bow or crossbow"]] +
    [["Everest VentureWare","Probably a bow, crossbow, or rifle"]] +
    [["Faisal’s Customs","-"]] +
    [["Federated Arms","-"]]*3 +
    [["Georgia Arms","Probably Poor Quality"]] +
    [["GunMart","Probably Poor Quality"]]*16 +
    [["IMI","-"]] +
    [["Kendachi","-"]] +
    [["KTech","-"]]*2 +
    [["Magnum Opus","-"]]*2 +
    [["Malorian Arms","Probably Excellent Quality"]] +
    [["MetaCorp","-"]] +
    [["Midnight Arms","-"]]*3 +
    [["Militech","-"]]*11 +
    [["Mustang Arms","-"]]*2 +
    [["Nova Arms","-"]]*2 +
    [["Pursuit Security Inc.","-"]]*2 +
    [["Rostović","-"]]*3 +
    [["Sanroo Firearms of Tokyo","Make it cute!"]] +
    [["Segotari","Probably an Elflines Online tie-in"]] +
    [["Sternmeyer","Rarely Poor Quality"]]*2 +
    [["Stolbovoy","-"]]*2 +
    [["Techtronika Russia","-"]]*4 +
    [["Towa Manufacturing","-"]]*2 +
    [["Tsunami Arms","Probably Excellent Quality"]] +
    [["UrbanTech","Rarely Excellent Quality"]]*2
)

# Weapon Types - [Name, Cost category, Skill type index (for price calc)] - 1-60
WEAPONTYPE = (
    [["Medium Pistol", 2, 1]]*6 +
    [["Heavy Pistol", 3, 1]]*6 +
    [["Very Heavy Pistol", 3, 1]]*6 +
    [["SMG", 3, 1]]*6 +
    [["Heavy SMG", 3, 1]]*6 +
    [["Shotgun", 4, 2]]*6 +
    [["Assault Rifle", 4, 2]]*6 +
    [["Sniper Rifle", 4, 2]]*6 +
    [["Bow", 3, 4]]*3 +
    [["Crossbow",3, 4]]*3 +
    [["Grenade Launcher", 4, 3]]*4 +
    [["Rocket Launcher", 4, 3]]*2
)

# Qualities - [Name, Cost category change (for price calc)] - 1-6
QUALITY = (
    [["Poor Quality", -1]]*3 +
    [["Standard Quality", 0]]*2 +
    [["Excellent Quality", 1]]
)

# Handgun attachments - [Name, Price] - 1-60
HANDGUN = (
    [["Drum Magazine", 500]]*10 +
    [["Extended Magazine", 100]]*10 +
    [["Infrared Nightvision Scope", 500]]*10 +
    [["Silencer", 100]]*10 +
    [["Smartgun Link", 500]]*10 +
    [["Sniping Scope", 100]]*10
)

# Shoulder arm attachments - [Name, Price] - 1-60
SHOULDERARM = (
    [["Bayonet", 100]]*5 +
    [["Airhypo Bayonet", 100]] +
    [["Drum Magazine", 500]]*6 +
    [["Extended Magazine", 100]]*6 +
    [["Grapple Gun Underbarrel", 100]]*6 +
    [["Grenade Launcher Underbarrel", 500]]*6 +
    [["Infrared Nightvision Scope", 500]]*6 +
    [["Shotgun Underbarrel", 500]]*6 +
    [["Silencer", 100]]*6 +
    [["Smartgun Link", 500]]*6 +
    [["Sniping Scope", 100]]*6
)

# Heavy weapon attachments - [Name, Price] - 1-60
HEAVY = (
    [["Drum Magazine", 500]]*10 +
    [["Extended Magazine", 100]]*10 +
    [["Infrared Nightvision Scope", 500]]*10 +
    [["Silencer (if eligible, otherwise roll again)", 100]]*10 + # To-do change reroll to exception in attachement script
    [["Smartgun Link", 500]]*10 +
    [["Sniping Scope", 100]]*10
)

# Archery weapon attachments - [Name, Price] - 1-60
ARCHERY = (
    [["Infrared Nightvision Scope", 500]]*20 +
    [["Grapple Gun Underbarrel (if eligible, otherwise roll again)", 100]]*10 + # To-do change reroll to exception in attachement script
    [["Smartgun Link", 500]]*10 +
    [["Sniping Scope", 100]]*20
)

# Weapon name templates - [Template, Example] - 1-100
DESC = (
    [["<Letter(s)>-<Number(s)>","CP-2020"]]*9 +
    [["<Descriptor> <Number(s)>","Cyberpunk 2020"]]*6 +
    [["<Model/Mark/Version> <Number>","Mark 2020"]]*6 +
    [["<Deadly Animal Name>","Polar Bear"]]*3 +
    [["<Descriptor> <Deadly Animal Name>","Ballistic Polar Bear"]]*3 +
    [["<Deadly Animal Name> <Descriptor>","Polar Bear Deluxe"]]*3 +
    [["<Noun> <Deadly Animal Name>","Survival Polar Bear"]]*3 +
    [["<Deadly Animal Name> <Noun>","Polar Bear Rocket"]]*3 +
    [["<Mythological/Fictional Name>","Jabberwock"]]*3 +
    [["<Descriptor> <Mythological/Fictional Name>","Vorpal Jabberwock"]]*3 +
    [["<Mythological/Fictional Name> <Descriptor>","Jabberwock Mimsy"]]*3 +
    [["<Noun> <Mythological/Fiction Name>","Wrath Jabberwock"]]*3 +
    [["<Mythological/Fiction Name> <Noun>","Jabberwock Decapitator"]]*3 +
    [["<Descriptor> <Type of Person>","Weekend Warrior"]]*3 +
    [["<Type of Person> <Descriptor>","Warrior Special"]]*3 +
    [["<Type of Person> <Type of Person>","Corporate Warrior"]]*3 +
    [["<Noun> <Noun>","Urban Destroyer"]]*3 +
    [["<Noun> <Noun> No space","Urbandestroyer"]]*3 +
    [["<Noun><Noun> No space, camelcase","UrbanDestroyer"]]*3 +
    [["<Descriptor> <Descriptive Noun>","Shredding Shotgun"]]*3 +
    [["<Descriptive Noun> <Descriptor>","Shotgun Shredder"]]*3 +
    [["<Location>","Miami"]]*3 +
    [["<Location> <Descriptor>","Miami Topdown"]]*3 +
    [["<Descriptor> <Location>","Bloody Miami"]]*3 +
    [["<Location> <Noun>","Miami Rooster"]]*3 +
    [["<Noun> <Location>","Hotline Miami"]]*3 +
    [["<Technobabble Word> <Number>","Autoslicer 2020"]]*3 +
    [["<Technobabble Word> <Descriptor>","Autoslicer Modern"]]*3 +
    [["<Technobabble Word> <Noun>","Autoslicer Celebration"]]*3 +
    [["<Something Geeky>","+1 Very Heavy Pistol of Protection"]]*1
)

# Return weapon type table based on weapon type num
def ATTTABLE (wt_num):
    match wt_num:
        case 1:
            return HANDGUN
        case 2:
            return SHOULDERARM
        case 3: 
            return HEAVY
        case 4:
            return ARCHERY

# Randomises attachment based on weapon type
def ATTACHMENT(wt, arg, speed):
    out = None
    table = ATTTABLE(wt[2])
    
    if arg is not None :
        #print("Attachment")
        if arg > 0 :
            out = table[arg - 1]
            #print("Set")
        elif speed :
            out = random.choice(table)
            #print("Rolled")
        elif not speed :
            out = SELECT(table, "Select an attachment") # Replace with elseif to use TUI with right attachment table
            #print("User select mode")
    #else :
        #print("No Attachment")

    #print(UNIQUE(MANUFACTURER))
    
    return out

# Calculates Price
def PRICE(wt, qua, att=["None",0]):
    return COSTCAT[wt[1]+qua[1]] + att[1]

# Create a table of unique options
def UNIQUE(table):
    opt = table[0]
    start = 1
    out = []
    for index in range(len(table)):
        if table[index] != opt :
            out.append([opt, start, index])
            start = index + 1
            opt = table[index]
    out.append([opt, start, len(table)])
    return out

def INTIN(text, min, max):
    while True :
        out = input(text + " or leave blank to roll: ")
        if out == '':
            out = random.randint(min, max)
            break
        else:
            try:
                out = int(out)
                if out < min or out > max:
                    print("ERROR: Invalid input. Please input integer between " + min + " and " + max)
                    continue
                else :
                    break
            except:
                print("ERROR: Input not integer. Please input integer between " + min + " and " + max)
                continue
    return out

def SELECT(table, text):
    unitab = UNIQUE(table)
    for item in unitab:
        print(str(item[1]) + "-" + str(item[2]) + ": " + item[0][0])
    while True:
        choice=INTIN(text, 1, len(table))
        print("You selected: " + table[choice-1][0])
        retry=input("Press enter to continue or type to pick again: ")
        if retry:
            continue
        else:
            break
    return table[choice-1]

# Roll basic tables
def ROLL(arg, speed, table, text):
    if arg :
        return table[arg - 1]
    elif speed :
        return random.choice(table)
    else :
        return SELECT(table, text) # Replace with function to choose or roll in TUI

# Command line args
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--speed', action='store_true') # Flag for headless (just output)
parser.add_argument('-m', '--manufacturer', type=int, choices=range(1,101)) # Option for choosing manufacturer
parser.add_argument('-t', '--type', type=int, choices=range(1,61)) # Option for choosing type
parser.add_argument('-q', '--quality', type=int, choices=range(1,61)) # Option for choosing quality
parser.add_argument('-d', '--description', type=int, choices=range(1,101)) # Option for choosing description
parser.add_argument('-a', '--attachment', nargs='?', default=None, const=0, type=int, choices=range(1,61)) # Option for attachment, can take integer for table entry

# Parse arguments into variable
args = parser.parse_args()
#print(args)


rolled_man = ROLL(args.manufacturer, args.speed, MANUFACTURER, "Select a manufacturer")
rolled_wt  = ROLL(args.type, args.speed, WEAPONTYPE, "Select a weapon type")
rolled_qua = ROLL(args.quality, args.speed, QUALITY, "Select weapon quality")

if not args.speed and args.attachment is None:
    while True:
        argat = input("Include attachment (y/n (or blank)): ").lower()
        if argat == 'y' or argat== 'yes' :
            args.attachment = 0
            break
        elif argat == 'n' or argat == 'no' or argat == '' :
            break
        else :
            print("ERROR: Input not 'y' or 'n' or ''")
            continue
rolled_att = ATTACHMENT(rolled_wt, args.attachment, args.speed)

rolled_dsc = ROLL(args.description, args.speed, DESC, "Select a name template")

print()
print("===============================")

print("Manufacturer: " + rolled_man[0])
print("Weapon type: " + rolled_wt[0])
print("Quality: " + rolled_qua[0])
print("Name template: " + rolled_dsc[0] + " Example: " + rolled_dsc[1])

if rolled_att :
    print("Attachment: " + rolled_att[0])
    rolled_pri = PRICE(rolled_wt, rolled_qua, rolled_att)
else :
    rolled_pri = PRICE(rolled_wt, rolled_qua)

print("Cost: " + str(rolled_pri))

print("===============================")
print()