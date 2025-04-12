from ..pokerstrat import Strategy, calc_bet

class AllCallStacy22(Strategy):
    def decide_play(self, player, pot,log):
                log = player.check_call(pot, log)
                return log