from ..pokerstrat import Strategy, calc_bet

class Mandy(Strategy):
    def decide_play(self, player, pot,log):
                log = player.check_call(pot, log)
                return log
		  