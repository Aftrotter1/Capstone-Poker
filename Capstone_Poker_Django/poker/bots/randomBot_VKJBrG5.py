from ..pokerstrat import Strategy, calc_bet
import random
class Random(Strategy):
	def decide_play(self, player, pot, log):
		choice=random.randint(0,3)
               
                
		if choice==0:
			log = player.fold(pot, log)
		elif choice==1:
			if player.stack<=player.to_play:
				log = player.check_call(pot, log)
			else:
				bet, log = calc_bet(player, log)
				log = player.bet(pot, bet, log)
		elif choice==2:
			if player.stack<=player.to_play:
				log = player.check_call(pot, log)
			else:
				log = player.bet(pot, player.stack, log)
	
		return log