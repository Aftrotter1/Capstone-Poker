from ..pokerstrat import Strategy
from ..pokerhands import flush_value as flush
from ..hand_values import *

class SklanskySys2(Strategy):

    #sklansky all-in tournament strategy

    def decide_play(self, player, pot, log):

        total_blinds=(pot.blinds[0]+pot.blinds[1])
        score=(player.stack/total_blinds)
        score*=pot.yet_to_play
        score*=(pot.limpers+1)
        score=int(score)
        
        hand_value, quality=player.get_value()
        raw_values = list(map(lambda x: x.value, player.total_cards))
        raw_values.sort(reverse=True)
        raw_values = tuple(raw_values)
        flush_value = flush(player.cards)
        
        key=((range(0,19)), (range(20,39)), (range(40,59)), (range(60,79)), (range(80,99)), (range(100,149)), (range(150,199)), (range(200, 399)), (range(400, 1000)))

        for k in key:
            if score in k:
                pointer=key.index(k)

        GAI=False

        log += 'score='+str(score)
        log += 'pot raised='+str(pot.raised)
        
        if pot.raised:

            if raw_values in ((13,13), (12,12)):
                GAI=True

            elif raw_values in (13,12) and flush_value==2:
                GAI=True

            else:
                GAI=False
        
        elif score>400 and raw_values in (13,13):
            GAI=True
        elif score in range (200,399) and raw_values in ((13,13),(12,12)):
            GAI=True
        elif score in range (150,199) and raw_values in ((13,13),(12,12), (11,11), (13,12)):
            GAI=True
        elif score in range (100,149) and raw_values in ((13,13),(12,12),(11,11),(10,10),(9,9),(13,12),(13,11),(12,11)):
            GAI=True
        elif score in range (80,99):
            if hand_value in (PAIR, TWO_PAIR):
                GAI=True
            elif raw_values in ((13,12),(13,11),(12,11)):
                GAI=True
            elif flush_value==2 and 13 in raw_values:
                GAI=True
            elif flush_value==2 and hand_value == STRAIGHT:
                GAI=True
        elif score in range (60,79):
            if hand_value in (PAIR, TWO_PAIR):
                GAI=True
            elif 13 in raw_values:
                GAI=True
            elif flush_value==2 and 12 in raw_values:
                GAI=True
            elif flush_value==2:# and gappers<=1:
                GAI=True
        elif score in range (40,59):
            if hand_value in (PAIR, TWO_PAIR):
                GAI=True
            elif 13 or 12 in raw_values:
                GAI=True
            elif flush_value==2 and 12 in raw_values:
                GAI=True
            elif flush_value==2:# and gappers<=1:
                GAI=True
        elif score in range (20,39):
            if hand_value in (PAIR, TWO_PAIR):
                GAI=True
            elif 13 or 12 in raw_values:
                GAI=True
            elif flush_value==2:
                GAI=True
        elif score in range(0,19):
            GAI=True

        else:
            GAI=False


        if GAI:
            if player.stack<=player.to_play:
                log = player.check_call(pot, log)
            else:
                log = player.bet(pot, player.stack, log)
        else:
            log = player.fold(pot, log)

        return log
            
            
 