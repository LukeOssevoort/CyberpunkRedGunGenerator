import random
import math
import sys
import traceback

COSTCAT = [10,20,50,100,500,1000,5000]

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

QUALITY = (
    [["Poor Quality", -1]]*3 +
    [["Standard Quality", 0]]*2 +
    [["Excellent Quality", 1]]
)

HANDGUN = (
    [["Drum Magazine", 500]] +
    [["Extended Magazine", 100]] +
    [["Infrared Nightvision Scope", 500]] +
    [["Silencer", 100]] +
    [["Smartgun Link", 500]] +
    [["Sniping Scope", 100]]
)

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

HEAVY = (
    [["Drum Magazine", 500]] +
    [["Extended Magazine", 100]] +
    [["Infrared Nightvision Scope", 500]] +
    [["Silencer (if eligible, otherwise roll again)", 100]] +
    [["Smartgun Link", 500]] +
    [["Sniping Scope", 100]]
)

ARCHERY = (
    [["Infrared Nightvision Scope", 500]]*2 +
    [["Grapple Gun Underbarrel (if eligible, otherwise roll again)", 100]] +
    [["Smartgun Link", 500]] +
    [["Sniping Scope", 100]]*2
)

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

def ATTACHMENT(wt):
    out = ""
    
    match wt[2]:
        case 1:
            out = random.choice(HANDGUN)
        case 2:
            out = random.choice(SHOULDERARM)
        case 3:
            out = random.choice(HEAVY)
        case 4:
            out = random.choice(ARCHERY)

    return out

def PRICE(wt, qua, att=["None",0]):
    return COSTCAT[wt[1]+qua[1]] + att[1]

rolled_man = random.choice(MANUFACTURER)
rolled_wt  = random.choice(WEAPONTYPE)
rolled_qua = random.choice(QUALITY)
rolled_att = ATTACHMENT(rolled_wt)
rolled_pri = PRICE(rolled_wt, rolled_qua, rolled_att)
rolled_dsc = random.choice(DESC)

print(rolled_qua[0] + " " + rolled_wt[0])
print(rolled_man[0] + " | Note: " + rolled_man[1])
print(rolled_dsc[0] + " | Example: " + rolled_dsc[1])
print("Attachment: " + rolled_att[0])
print("Cost: " + str(rolled_pri) + "eb")
