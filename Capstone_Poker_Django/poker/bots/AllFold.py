from ..pokerstrat import Strategy, calc_bet

class AllFold(Strategy):
    def decide_play(self, player, pot,log):
                log = player.fold(pot, log)
                return log
		  