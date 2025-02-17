from ..pokerstrat import Strategy, calc_bet

class bot1(Strategy): ## want to be agressive early, play conservative near money line, check raise if we bet first with a good hand
    
    def decide_play(self, player, pot):
                total_blinds=(pot.blinds[0]+pot.blinds[1])
                score=(player.stack/total_blinds)
                score*=pot.yet_to_play
                score*=(pot.limpers+1)
                score=int(score)

                hand_value, rep, tie_break, raw_data=player.get_value()
                raw_values, flush_score, straight, gappers=raw_data
                raw_values.sort()

                print ('score='+str(score))

                RB=False ## RB stands for raise bet. I use raise bet rather than an all in tactic because all in scares players into folding.

                if player.big_blind:
                        self.aggression = 1
                        player.check_call(pot)

                elif player.small_blind:
                        self.aggression = 1
                        player.check_call(pot)

                        ## change to check call in instances where there isn't a possible flush, gapper, or straight, or pair/ triplet or full house


                if pot.raised:

                        if raw_values in ((13,13), (12,12)): ## Set of Aces or Kings in starting values 
                                RB=True

                        elif raw_values in (13,12) and flush_value==2: ##Ace and a King of the same suit
                                RB=True

                        else:
                                RB=False

                elif score>400 and raw_values in (13,13): ## means you have a flush or higher with two Aces in your deck. High win chance.
                        RB=True
                elif score in range (200,399) and raw_values in ((13,13),(12,12)): ## set of Aces or Kings but not the same suit and possibility of a triple. two pair 
                        RB=True
                elif score in range (150,199) and raw_values in ((13,13),(12,12), (11,11), (13,12)): ## A pair of two  from Ace to Queen, or having An Ace and king (chance of having a pair of one of them)
                        RB=True
                elif score in range (100,149) and raw_values in ((13,13),(12,12),(11,11),(10,10),(9,9),(13,12),(13,11),(12,11)): ## A higher order pair or a set of royal cards with a chance of a pair in deck
                        RB=True
                elif score in range (80,99): ##cards that are not a match in your hand
                        if 'pair' in rep:
                                RB=True
                        elif raw_values in ((13,12),(13,11),(12,11)):
                                RB=True
                        elif flush_score==2 and 13 in raw_values:               ## flush = all cards of the same suit. high end flush
                                RB=True
                        elif flush_score==2 and straight>=5:                    ## straight flush 
                                RB=True
                elif score in range (60,79): ## cards that are not a match in your hand 
                        if 'pair' in rep: ## avaliable pair with the cards you have
                                RB=True
                        elif 13 in raw_values:
                                RB=True
                        elif flush_score==2 and 12 in raw_values:
                                RB=True
                        elif flush_score==2 and gappers<=1: ##gappers are non consecutive cards of the same suit which could potentially end with a straight
                                RB=True
                elif score in range (40,59):
                        if 'pair' in rep:
                                RB=True
                        elif 13 or 12 in raw_values:
                                RB=True
                        elif flush_score==2 and 12 in raw_values:
                                RB=True
                        elif flush_score==2 and gappers<=1:
                                RB=True
                elif score in range (20,39):
                        if 'pair' in rep:
                                RB=True
                        elif 13 or 12 in raw_values:
                                RB=True
                        elif flush_score==2:
                                RB=True
                elif score in range(0,19):
                        RB=True

                else:
                        RB= False


                if RB:
                        if player.stack<=player.to_play:
                                player.check_call(pot)
                        else:
                                player.bet(pot, calc_bet(player))
                else:
                        player.fold(pot)