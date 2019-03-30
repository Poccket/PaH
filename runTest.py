import modDisp
import modFile
import modList
import random

poker = modFile.read_list("cardFrench.txt")
cardA = random.randrange(0, 52)
cardB = random.randrange(0, 52)
cardADis = modDisp.as_block(poker[cardA], aslist=True)
cardBDis = modDisp.as_block(poker[cardB], aslist=True)
cardABDis = modList.merge_alternate([cardADis, cardBDis])
y = 2

for x in cardABDis:
    if y != 0:
        print(x, end='')
    else:
        print("")
        print(x, end='')
        y = 2
    y -= 1
print("", flush=True)
input("Enter to exit")
