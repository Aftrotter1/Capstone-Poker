from ..pokerstrat import Strategy, calc_bet

class Human(Strategy):
    
    options=[['x', 'f', 'b'], ['c', 'r', 'f'], ['c', 'f']]
    choices={0:'check, fold or bet', 1:'call, raise, fold', 2:'call all-in or fold'}
    
    def decide_play(self, player, pot):
        
        player.get_value()
        
        options=Human.options
        choices=Human.choices
        action=''
        op=0


        if player.to_play==0:
                op=0
        elif player.to_play<player.stack:
                op=1
        else: op=2

        

        while action not in options[op]:

                try:
                        action=input(str(choices[op]))
                except NameError:
                 print ('enter a valid choice')

    
        if action=='x':
                player.check_call(pot)
        elif action=='f':
                player.fold(pot)
        elif action=='c':
                player.check_call(pot)
        elif action=='b' or action=='r':
                stake=0
                max_bet=player.stack
                print ('max '+str(max_bet))
                while stake not in range (10,(max_bet+1), 5):
                        try:
                                stake=int(input('stake..'))
                        except:
                                print ('input a stake')
                print ('stake '+str(stake))                                
                player.bet(pot, stake)