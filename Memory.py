import simplegui
import random

# helper function to initialize globals
def new_game():
    global index_dict, polydict, turns, clicks, cardeval
    polydict={}
    index_dict={}
    clicks = 0
    cardeval = {}
    turns = 0
    cards = range(8) + range(8)
    random.shuffle(cards)
    # create index_dictionary for card values and exposed status
    x=0
    for card in range(16):
        index_dict[x]=[cards[card],0]
        polydict[card]=[[(0+card*50, 0), (50+card*50, 0), (50+card*50, 100), (0+card*50,100)],0]
        x+=1    
       
# define event handlers
def mouseclick(pos):
    global clicks, cardeval, turns
    clicks += 1

    if clicks % 2 !=0:
        for p in polydict:
                (polydict[p])[1] = 0
    if polydict.has_key(int(pos[0]/50)) :             
        (polydict[int(pos[0]/50)])[1] = 1
        cardeval[int(pos[0]/50)] = (index_dict[int(pos[0]/50)])[0]

    if clicks % 2 == 0:
        if len(cardeval) == 2:
            turns +=1
            if cardeval.values()[0] == cardeval.values()[1]:
                for k in cardeval.keys():
                    (index_dict[k])[1] = 1               
                    del polydict[k]
            cardeval = {}
        else:
            clicks-=1
                                   
# cards are logically 50x100 pixels in size    
def draw(canvas):
      
    pos=10 # has to be relative to polygons to conserve positions
    label1.set_text("Turns = "+str(turns))
    for c in index_dict:
        canvas.draw_text(str((index_dict[c])[0]), (pos, 75), 50, "White")
        pos += 50
    
    for deck in polydict:
        if (polydict[deck])[1] == 0:
            canvas.draw_polygon((polydict[deck])[0], 2, "Gray", "Green")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label1 = frame.add_label("Turns = 0")

# initialize global variables
new_game()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()