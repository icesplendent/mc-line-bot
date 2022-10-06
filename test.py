import random

times=1000

up2600=0
up2800=0
up2500=0
up2000=0
up2400=0
up1900=0


while times > 0:
    init = 0
    company = 12
    while company>0:
        x=random.randrange(100,301,100)
        init = init + x
        company = company -1
    print(init)
    if init >= 2600:
        up2600=up2600+1
    if init >= 2800:
        up2800=up2800+1
    if init >= 2500:
        up2500=up2500+1
    if init >= 2000:
        up2000=up2000+1
    if init >= 2400:
        up2400=up2400+1
    if init >= 1900:
        up1900=up1900+1
    #print("\n")
    times = times - 1

print("2600=")
print(up2600)
print("2800=")
print(up2800)
print("2500=")
print(up2500)
print("2000=")
print(up2000)
print("2400=")
print(up2400)
print("1900=")
print(up1900)

