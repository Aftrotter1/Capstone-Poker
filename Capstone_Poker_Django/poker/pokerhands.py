#Pokerhand evaluator

#dictionary for value:name conversion

names={1:'deuce', 2:'three', 3:'four', 4:'five', 5:'six', 6:'seven', 7:'eight', 8:'nine', 9:'ten', 10:'jack', 11:'queen', 12:'king', 13:'ace'}

STRAIGHT_FLUSH = 8
FOUR_KIND = 7
FULL_HOUSE = 6
FLUSH = 5
STRAIGHT = 4
THREE_KIND = 3
TWO_PAIR = 2
PAIR = 1
HIGH_CARD = 0

from collections import Counter
from operator import attrgetter

#conversion function for values>names

def cn(value):
    name=names[value]
    return str(name)

#straight detector

def is_straight(values):
    unique = []
    for elem in values:
        if not elem in unique:
            unique.append(elem)
    unique.sort(reverse=True)

    if len(unique) < 5:
        return 0
    
    for i in range(len(unique)-4):
        if unique[i] - 1 == unique[i+1] and unique[i] - 2 == unique[i+2] and unique[i] - 3 == unique[i+3] and unique[i] - 4 == unique[i+4]:
            return unique[i]
    return 0


def from_straight(cards):
    in_5 = 1

    unique_vals = []
    for card in cards:
        if card.value not in unique_vals:
            unique_vals.append(card.value)
    unique_vals.sort(reverse=True)

    for i in range(len(unique_vals)):
        next_4 = 0
        for j in range(1, 5):
            if i + j < len(unique_vals) and unique_vals[i + j] >= unique_vals[i] - 4:
                next_4 += 1
        in_5 = max(in_5, 1+next_4)

    return 5 - in_5

def evaluate_hand(cards):
    hand_value = 0
    quality = [0, 0, 0, 0, 0]
    values = []
    unique_vals = []
    suits = {'s': [], 'c': [], 'h': [], 'd': []}

    for card in cards:
        values.append(card.value)
        if not card.value in unique_vals:
            unique_vals.append(card.value)
        suits[card.suit].append(card.value)
    values.sort(reverse=True)
    unique_vals.sort(reverse=True)

    for suit, vals in suits.items():        # Checking for flush
        if len(vals) >= 5:
            straight = is_straight(vals)
            vals.sort(reverse=True)
            if straight > 0:
                return STRAIGHT_FLUSH, vals                                         # Best outcome, can't be beaten
            hand_value = FLUSH                                                          # May be beaten by 4 of a kind or full house
            quality = vals

    multiples_l=[[], [], [], [], []] # first two lists will not be used

    value_hist=Counter(values)     # Histogram
    # print("{}".format(values)) ## 
    for rank, quant in value_hist.items():
        if quant > 1:
            multiples_l[quant].append(rank)
    
    if len(multiples_l[4]) > 0:     # Check for 4 of a kind
        foursome = max(multiples_l[4])
        high = unique_vals[0]
        if high == foursome:
            high = unique_vals[1]
        quality = [foursome, foursome, foursome, foursome, high]
        return FOUR_KIND, quality                                                       # Next best after straight flush
    
    if len(multiples_l[3]) > 0:     # Check for 3 of a kind
        if len(multiples_l[3]) > 1:
            multiples_l[3].sort(reverse=True)
            triplet = multiples_l[3][0]
            pair = multiples_l[3][1]      # Impossible to have 2 triplets and a pair
            quality = [triplet, triplet, triplet, pair, pair]
            return FULL_HOUSE, quality                                                  # Full house is next best hand
        else:
            triplet = multiples_l[3][0]
            if len(multiples_l[2]) > 0:
                pair = max(multiples_l[2])
                quality = [triplet, triplet, triplet, pair, pair]
                return FULL_HOUSE, quality                                              # Full house
            if hand_value == FLUSH:
                return FLUSH, quality                                                   # Flush is next best
            hand_value = THREE_KIND
            high = unique_vals[0]
            high2 = unique_vals[1]
            if high == triplet:
                high = high2
                high2 = unique_vals[2]
            elif high2 == triplet:
                high2 = unique_vals[2]
            quality = [triplet, triplet, triplet, high, high2]                              # Need to check for straight before returning this
    
    straight_qual = is_straight(values)
    if straight_qual > 0:
        return STRAIGHT, straight_qual
    
    if hand_value == THREE_KIND:
        return THREE_KIND, quality                                                      # Now send 3 of a kind through
    
    if len(multiples_l[2]) > 1:                                                         # 2 pair
        multiples_l[2].sort(reverse=True)
        pair1 = multiples_l[2][0]
        pair2 = multiples_l[2][1]
        high = unique_vals[0]
        if high == pair1:
            high = unique_vals[1]
        if high == pair2:
            high = unique_vals[2]
        quality = [pair1, pair1, pair2, pair2, high]
        return TWO_PAIR, quality
    elif len(multiples_l[2]) == 1:                                                      # 1 pair
        pair = multiples_l[2][0]
        highs = []
        i = 0
        while len(highs) < 3:
            if pair == unique_vals[i]:
                i += 1
            highs.append(unique_vals[i])
            i += 1
        quality = [pair, pair] + highs
        return PAIR, quality
    
    quality = 0
    return HIGH_CARD, unique_vals                                                           # High card

        

    '''
    #split cards into values and suits
    values=[]
    raw_values=[]
    suits=[]
    flush=False
    high_card=True #False if anything but a high card remains
        
    for card in cards:
        values.append(card.value)
        suits.append(card.suit)

    #keep raw data on values

    for v in values:
        raw_values.append(v)

    #perform histogram on values and suits

    value_count=Counter(values)
    suit_count=Counter(suits)

    #put values in order of rank
    values.sort(reverse=True)
    
    #set up variables
    
    pair_l=[]
    trip_l=[]
    quad_l=[]
    multiples_l=[0,0,pair_l, trip_l, quad_l] #0,0 are dummies
    remove_list=[] # list of multiples to be removed
    rep=''
    hand_value=0
    winning_cards=[] # Will collect any cards of which there are multiple

    limit=len(values)
    if limit>5:
        limit=5
        
    straight=is_straight(values)
    
    #iterate through values
    
    for key, value in value_count.items():

    #if histogram is more than one, it's pair, trip or quads
    
        if value>1:
            
            #key=int(key)
            multiples_l[value].append(key)
            
            for element in values:
            	#removes the valuable cards and leaves the rest in 'values'
            	if element==key:
                    remove_list.append(element)
                    #separate out the valuable 
                    winning_cards.append(element)
            
            for item in remove_list:
                values.remove(item)
            
            winning_cards.sort(reverse=True)

            #clear the remove list for the next histogram iteration
            remove_list=[]

    pair_l.sort(reverse=True)    

    # check for flush
    
    for key, value in suit_count.items():
    	
        flush_score=0
    		
        if value>=5: # >=
            flush=True
            high_card=False
        
        flush_score=value

    #find values     
 
        
    if len(pair_l)==1 and trip_l==[]:
        rep=('pair of '+cn(pair_l[0])+'s')
        hand_value=100+(sum(winning_cards[:2]))

    elif len(pair_l)>1:
        rep=('two pair -'+cn(pair_l[0])+'s and '+cn(pair_l[1])+'s ')
        hand_value=200+(sum(winning_cards[:4]))
    
    elif trip_l and pair_l==[]:
        rep=('trip '+cn(trip_l[0])+'s ')
        hand_value=300+(sum(winning_cards[:3]))

    elif straight>0 and not flush:
        rep=('Straight, '+cn(straight)+' high')
        hand_value=400+straight

    elif flush:

        flush_l=[]
        #find out the values of each flush card for comparison
        for card in cards:
            if key in card.suit:
                    flush_l.append(card.value)
        flush_l.sort(reverse=True)
        rep=('Flush, '+cn(flush_l[0])+' high')
        hand_value=500+(int(flush_l[0]))
    
    elif len(trip_l)==1 and len(pair_l)>=1:
        rep=('full house - '+cn(trip_l[0])+'s full of '+cn(pair_l[0])+'s')
        hand_value=600+(sum(winning_cards[:3]))
        

    elif quad_l:
        rep=('four '+cn(quad_l[0])+' s')
        hand_value=700+(sum(winning_cards[:4]))

    elif (straight in range (1,9)) and flush:
        rep=('Straight flush, '+cn(straight)+' high')
        hand_value=800+straight

  
   
        
    #if high_card is true:

    else:
        
        rep=('high card '+cn(values[0]))
        hand_value=values[0]
    
    
    
    gappers=(raw_values[0])-(raw_values[1])
    raw_data=(raw_values, flush_score, straight, gappers)
		
    return rep, hand_value, raw_data
        # String description, numerical hand quality index, 
    '''