from ..pokerstrat import Strategy, calc_bet

class AllCall(Strategy):
  	def decide_play(self, player, pot):
		  return player.check_call(pot)