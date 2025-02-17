from ..pokerstrat import Strategy, calc_bet
import random
class Random(Strategy):

    
        def decide_play(self, player, pot):

                
             
                choice=random.randint(0,3)
               
                
                if choice==0:
                	player.fold(pot)
                
                elif choice==1:
                	if player.stack<=player.to_play:
                		player.check_call(pot)
                	else:
                		player.bet(pot, calc_bet(player))
                elif choice==2:
                	if player.stack<=player.to_play:
                		player.check_call(pot)
                	else:
                		player.bet(pot, player.stack)