
import random
from .pokerhands import evaluate_hand
from operator import attrgetter
# import time
# from . import pokerstrat


class Card:             # Defines a card object

    RANKS=['2','3','4','5','6','7','8','9','10','J', 'Q', 'K', 'A']

    SUITS=['h', 'c', 's', 'd']

    def __init__(self,rank, suit, faceup=True):

        self.rank=rank
        self.suit=suit
        self.values=[]
        self.__value=(Card.RANKS.index(self.rank)+1)    # Numerical value (J,Q,K,A are 10, 11, 12, 13)
        
        self.faceup=faceup

    def __str__(self):                                  # Describes card only if face up

        if self.faceup:
            
            return str(self.rank)+str(self.suit)
        else:
            return 'XX'

    @property

    def value(self):                                    # Getter function for value

        v=self.__value

        return v

#hand class (also used for Player)

class Hand:

    serial=0

    def __init__(self, name, table, strategy_cls,stack):

        
        self.strategy=[]
        self.stratname = strategy_cls.__name__
        strat = strategy_cls(self)
        self.strategy.append(strat)
               
        
        self.cards=[]
        self.total_cards=(self.cards+table.cards)
        self.table_cards = table.cards
        table.players.append(self)
        self.name=name
        
        Hand.serial+=1
        self.position=Hand.serial
        self.small_blind=False
        self.big_blind=False
        self.dealer=False
        self.hand_value=0
        self.rep=''
        self.quality=[0, 0, 0, 0, 0]
        self.raw_data=0
        self.is_folded=False
        self.stack=1000
        
        self.stake=0
        self.in_pot=0
        self.to_play=0
        self.all_in=False
        self.first_all_in=False
        self.raised=0
        self.carry_over=0

        #data points for play analysis:

        self.history=[]

        self.pots_played=0
        self.win=0
        self.raises=0
        self.calls=0
        self.checks=0

    @property

    def play_analysis(self):

        pass

    # @property

    # def get_position(self):

    #     return self.position%pot.table_size
    
    def __str__(self):


        rep='\n'+str(self.name)+' ['+str(self.stack)+']'
        
        if self.small_blind:
            rep+=' [small]'
        elif self.big_blind:
            rep+=' [big]'
        elif self.dealer:
            rep+=' [dealer]'
        

        return rep
   
        
    
    def get_value(self):        
        hand_value, quality=evaluate_hand(self.total_cards)
        
        self.hand_value=hand_value
        self.quality = quality

        if not type(self.quality) is list:
            str_cards = self.print_cards("", self.table_cards)
            raise TypeError("non-list quality: " + str(self.quality) + " | " + str(hand_value) + ", " + str_cards)
        
    
        return hand_value, quality
    

    def get_rep(self):
        desc_list = ['High Card', 'Pair', '2 Pair', '3 of a Kind', 'Straight', 'Flush', 'Full House', '4 of a Kind', 'Straight Flush']
        card_list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        rep = desc_list[self.hand_value]

        if self.hand_value in (0, 1, 3, 7):
            rep += ' ['+ card_list[self.quality[0]] +']'
        elif self.hand_value in (2, 6):
            rep += ' ['+ card_list[self.quality[0]] + ', ' + card_list[self.quality[3]] +']'
        elif self.hand_value in (4, 5, 8):
            rep += ' ['+ card_list[self.quality[0]] +' high]'

        return rep

   
    def print_cards(self, out_string, table_cards=None):

        rep=self.name + ': '

        if self.is_folded:
            rep += 'FF'

        else:

            for card in self.cards:

                rep+=' '+str(card)

        if not table_cards is None:
            rep += ' ' + str(table_cards)

        out_string += rep + '\n'
        return out_string
        
        
    def flip(self):
            
        for card in self.cards: card.faceup=not card.faceup

    def fold(self, pot, out_string):

        self.is_folded=True
        self.in_pot=0
        self.stake=0
        self.raised=0
        
     
        out_string += str(self.name)+' folds' + '\n'

        pot.folded_players.append(self)
        if self in pot.active_players:
        
            pot.active_players.remove(self)
        
                
        if pot.one_remaining:
            pot.stage=5
        return out_string

    def no_play(self, pot):
    	
        next_player(pot)
        self.stake=0
    	
   	
    def check_call(self, pot, out_string):
    	
        
        
        if self.to_play==0:
            out_string += str(self.name)+' checks' + '\n'
        else:
                if self.to_play>self.stack:
                    self.stake=self.stack
                else:
                    self.stake=self.to_play
                out_string += str(self.name)+' calls '+str(self.stake) + '\n'
                if pot.stage==0 and pot.raised==False:
                    pot.limpers+=1

        next_player(pot)
        return out_string
    
    
    def bet(self, pot, stake, out_string):
        
        if pot.already_bet:
            out_string += str(self.name)+' raises '+str(stake-self.to_play) + '\n'
            self.raised+=1
            pot.limpers=0
            pot.raised=True
        else:
            out_string += str(self.name)+' bets '+str(stake) + '\n'
        
            pot.already_bet=True
      
        self.stake=stake
        pot.to_play+=(self.stake-self.to_play)
        
        next_player(pot, True)
        return out_string
        
    def ante(self, pot):
        
        if self.small_blind:
            self.stack-=pot.blinds[0]
            pot.total+=pot.blinds[0]
            self.in_pot+=pot.blinds[0]
            
        if self.big_blind:
            self.stack-=pot.blinds[1]
            pot.total+=pot.blinds[1]
            pot.to_play=pot.blinds[1]
            self.in_pot+=pot.blinds[1]
        
                    
    def bust(self, table, out_string):

        out_string += str(self.name)+' is bust' + '\n'
        list_index=table.players.index(self)
        table.busted.append((self.name, table.hands))
        for p in table.players[list_index+1:]:
            p.position-=1
            
        table.players.remove(self)
        return out_string
        
        
    def clear(self):

      self.cards=[]
      self.total_cards = []
      self.table_cards = []
      self.is_folded=False
      self.all_in=False
      self.raised=0
      

    def add(self, cards):

      self.cards.append(cards)
      self.total_cards.append(cards)

    def values(self):
        values = []
        for card in self.total_cards:
            values.append(card.value)
        return values

#__________represents the card deck - shuffled each round            
        
class Deck(Hand):

    def __init__(self):

        self.cards=[]

    def populate(self):

        for rank in Card.RANKS:

            for suit in Card.SUITS:

                card=Card(rank, suit)
                self.cards.append(card)

    def shuffle(self):

        random.shuffle(self.cards)

    def print_cards(self, out_string):

        rep=''

        for card in self.cards:

            rep+=str(card)+' '

        out_string += rep + '\n'
        return out_string

    def deal_to(self, hand, out_string, cards=1, faceup=True):

        if len(self.cards)<cards:
                out_string += 'not enough cards to deal' + '\n'
                
        elif len(self.cards)==0:
                out_string += 'deck empty' + '\n'
                
        else:
                dealt=[]
                if not faceup:
                    for card in self.cards:
                         card.faceup=False
                
                for i in range (0,cards):
                        dealt.append(self.cards.pop())
                
                        
                for card in dealt:
                    
                    hand.add(card)

        return out_string

#__________________represents the overall game    

class Table(Hand):                  # Table is a Hand subclass because it has cards (similar functionality)

    def __init__(self, blinds=[10,20]):

                
        self.cards=[]
        self.players=[]
        self.is_folded=False
        self.button=0
        self.hands=0
        self.blinds_timer=0
        self.blinds = blinds
        self.busted = []
        
    def print_cards(self, out_string):

        rep='['

        if self.is_folded:
            rep='FF'

        else:

            for card in self.cards:
                card.faceup=True
                rep+=str(card)+' '

        out_string += rep + ']\n'
        return out_string

    def print_players(self, out_string):
    	
        for player in self.players:
            out_string += str(player) + '\n'

        return out_string
    		
    def clear(self):

      self.cards=[]

    def add(self, cards):
        self.cards.append(cards)
        for player in self.players:
            player.total_cards.append(cards)
            player.table_cards.append(cards)
      
      

#_______________POT represents the pot for each individual round of play

class Pot(object):
    
    stage_dict={0:'pre-flop bet', 1:'dealing the flop', 2:'dealing the turn', 3:'dealing the river'}
    deal_sequence=[0,3,1,1]
    pot_number=0
    
    def __init__(self, table, name):
        
   
        self.players=[]
        self.folded_players=[]
        self.active_players=[]
        self.limpers=0
        self.name=name
        self.blinds=table.blinds
                    
        self.total=0
        
        self.button=table.button
        #the amount each player has to call
        self.to_play=0
        #0=antes+ pre-flop, 1=post-flop, 2=turn, 3=river
        self.stage=0
        #defines turn within each betting stage
        self.turn=0
        #self.no_raise
        self.no_raise=0
        #already bet - works out if the round starts with 0 bet 
        self.already_bet=False
        self.raised=False
        

    @property

    def is_frozen(self):

        if len(self.active_players)<=1:
            self.active_players=[]
            return True
        else:
            return False

    @property

    def yet_to_play(self):

        ytp=self.table_size-(self.turn+1)
        if ytp<1: ytp=1

        return ytp

    @property

    def one_remaining(self):

        if len(self.folded_players)==(self.table_size-1):

            return True

        else:

            return False
        
    @property
    
    def table_size(self):
        
        
        return len(self.players)
        
    def __str__(self):

            rep='Pot= '+str(self.total)+'.  to play:'+str(self.to_play)
            return rep
            
    def set_blinds(self):
        
        dealer=(self.button)%self.table_size
        
        small_blind=(self.button+1)%self.table_size

        big_blind=(self.button+2)%self.table_size

        self.players[dealer].dealer=True

        self.players[small_blind].small_blind=True

        self.players[big_blind].big_blind=True

        return
    	

    @property

    def who_plays(self):

        next_up=0

        if self.stage==0:

            next_up=(self.button+3)%self.table_size

            return next_up

        else:

            next_up=(self.button+1)%self.table_size
            return next_up


class Side_pot(Pot):
    
    serial=0
    
    def __init__(self, parent):
        
        Pot.__init__(self, parent, Pot)
        
        self.button=parent.button
        Side_pot.serial+=1
        self.name='side pot '+str(Side_pot.serial)
        
        self.players=[]
           



#________________FUNCTIONS____________________________________________________

#clears the players hands, comm cards, deck and moves the button on

def debug(pot):

    print('debug______________________')
    for player in pot.players:
        
        print (str(player.name)+' Stack='+str(player.stack)+' Stake='+str(player.stake)+' Player in pot='+str(player.in_pot)+'  Pot total='+str(pot.total)+'  all_in='+str(player.all_in)+'first all in'+str(player.first_all_in))
        print ('is folded'+str(player.is_folded))
        print ('raw data='+str(player.raw_data))
        print ('position='+str(player.position))

    print (str(pot.name)+' total '+ str(pot.total))
    print ('yet to play:'+str(pot.yet_to_play))
    print ('active players')
    for player in pot.active_players:
        print (str(player.name))

    print ('table size '+str(pot.table_size))
    print ('limpers='+str(pot.limpers))
    print ('no raise '+str(pot.no_raise))
    print ('frozen='+str(pot.is_frozen))
    print ('one remaining='+str(pot.one_remaining))
    print ('Pot to play:  '+str(pot.to_play))
    print ('turn'+str(pot.turn)+'  no_raise'+str(pot.no_raise))
    print ('______________________________')

#helper function to move the play on

def next_player(pot, is_raise=False):

	pot.turn+=1
	if is_raise:
		pot.no_raise=1
	else:
		pot.no_raise+=1
		
	return


def next_hand(table, deck):

    table.clear()
    
    deck.clear()
    
    Side_pot.serial=0

    for hand in table.players:
        hand.clear()
        hand.small_blind=False
        hand.big_blind=False
        hand.dealer=False
        hand.first_all_in=False

    table.button+=1
    

#calculates the values and payouts

def ante_up(pot, deck, out_string):

    for player in pot.players:
                
        player.ante(pot)
        out_string += str(player) + '\n'
        out_string = deck.deal_to(player, out_string, 2)
        if player.stratname=='Human':
            player.flip()
        out_string = player.print_cards(out_string)
        pot.already_bet=True

    out_string += str(pot) + '\n'
    out_string += '\n\n\n'

    return out_string


def betting_round(pot, table, out_string):

    pots = [pot]
    
    is_side_pot=False
    create_side_pot=False
    side_potters=[]
    
    while pot.no_raise<(pot.table_size):
        
                
        next_up=(int(pot.who_plays)+(pot.turn))%pot.table_size
        player=pot.players[next_up]
        player.to_play=(pot.to_play-player.in_pot)
        if player.to_play<0:
            player.to_play=0
        
        

        #is the player folded? decide action

        if pot.is_frozen==False:

            if player in pot.active_players:
                  
                out_string += str(player.name)+' to play'+ str(player.to_play)+'\n\n'

                for strategy in player.strategy:

                      out_string = strategy.decide_play(player, pot, out_string)

            else:
                
                player.no_play(pot)
            
        else:
            player.no_play(pot)

#adjust player totals and check for all-ins
        
        pot.total+=player.stake
        player.in_pot+=player.stake
        player.stack-=player.stake
         
        if player.stack==0 and player.first_all_in==False:
            
            out_string += str(player.name)+' is all in\n'
            
            is_side_pot=True
            player.all_in=True
            player.first_all_in=True
            
            
    
        
        
        #debug(pot)
        
        
    if pot.one_remaining:
        is_side_pot=False
            
    #deal with refunds_____________________________
                
    if is_side_pot:
        
        for player in pot.players:
            if player.is_folded==False:
        		
                side_potters.append(player)
            
        side_potters.sort(key=attrgetter('in_pot'), reverse=True)
        big_bet=side_potters[0].in_pot
        

        next_pot_players=[]
    
        
        
    #main pot refund_____________________
        
        out_string += 'side pot\n'
        out_string += 'high bet'+str(big_bet) + '\n'
        low_bet=side_potters[-1].in_pot
        out_string += 'low bet'+str(low_bet) + '\n'
        
        for player in side_potters:
            
               
            refund=(player.in_pot-low_bet)
            if len(next_pot_players)>1:
                create_side_pot=True

            player.in_pot-=refund
            pot.total-=refund
            player.stack+=refund
            player.carry_over=refund

            out_string += 'player in side pot - '+str(player.name) + '\n'
            
            if player.carry_over>0:
                next_pot_players.append(player)
            else:
                if player in pot.active_players:
                    pot.active_players.remove(player)
      
            
            out_string += str(player.name) + '\n'
            out_string += 'refund...'+str(refund) + '\n'

#create side pots _________________________________________________

        if create_side_pot:

            sidepot=Side_pot(pot)
            
            for player in next_pot_players:
                
                sidepot.players.append(player)
                
                sidepot.total+=player.carry_over
                player.in_pot+=player.carry_over
                player.stack-=player.carry_over
                
                if player.stack>0:
                    player.first_all_in=False
                    player.all_in=False
                    pots[-1].active_players.append(player)
                
                
                
            pots.append(sidepot)
            
                   

 #print out pot totals at the end of the round______________________________
       
    for pot in pots:
        out_string += str(pot.name) + '\n'
        pot.to_play=0
        
        out_string += 'pot size= '+str(pot.total) + '\n'

#zero the player cash in the pot
        
        for player in pot.players:
            player.in_pot=0
            player.stake=0
            player.raised=0
        
  
#reset various pot variables for next betting round

    pots[0].no_raise=0
    pots[0].to_play=0
    pots[0].turn=0
    pots[0].stage+=1
    pots[0].already_bet=False
    pots[0].limpers=0

    return out_string


def showdown(pot, out_string):
        
    scoring=[]

    
    if pot.one_remaining:
        for player in pot.players:
            if player.is_folded==False:
                
                out_string += str(player.name)+' wins'+str(pot.total) + '\n'
                player.stack+=pot.total
            

    else:

        for player in pot.players:
            if player.is_folded==False:
                player.get_value()
                player.rep = player.get_rep()
                scoring.append(player)
                 
                 
                 
        #rank hands in value+tie break order
                 
        scoring.sort(key=lambda x: evaluate_hand(x.total_cards), reverse=True)
        split_pot=[]
        out_string += '\n\n\n'
        for player in scoring:

                # if player.stratname!='Human':
                #     player.flip()
                out_string = player.print_cards(out_string, list(map(lambda x: str(x), player.table_cards)))
                out_string += player.name+' has '+str(player.rep) + '\n'
                
                
        #check for split pot

        split_stake=0
        split=False
        
        for player in scoring[1:]:
            
            if (player.hand_value, player.quality) == (scoring[0].hand_value, scoring[0].quality):

                split=True
                split_pot.append(scoring[0])
                split_pot.append(player)


        if split:

            out_string += 'split pot\n'
            
            
            split_stake=int((pot.total/(len(split_pot))))
            for player in split_pot:
                     out_string += str(player.name)+' wins '+str(split_stake) + '\n'
                     player.stack+=split_stake
                     
        else:
                
                scoring[0].stack+=pot.total
                out_string += str(scoring[0].name)+' wins '+str(pot.total) + '\n'

    return out_string

#_______________________________________________________________________gameplay
        ######################

#set up the game and players
def run_game(
    botnumber: int = None,
    smallblind: int = 10,
    stack: int = 1000,
    custom_config: dict = None
):
    """
    Runs the poker game simulation.

    If custom_config is provided and not empty, we create players based on
    the {StrategyName: count} dictionary.
    Otherwise, if botnumber is provided, we create that many random players.

    :param botnumber: (int) number of random bots if no custom_config is given
    :param custom_config: (dict) e.g. {"SklanskySys2": 2, "Random": 3}
    :param smallblind: (int) small blind
    :param stack: (int) starting stack
    :return: A tuple of (winner, log). If an error occurs, returns (None, error_message).
    """
    import io
    import sys
    import random
    from . import bots
    from .pokerstrat import discoverStrats

    # Discover all Strategy subclasses in the bots package.
    bot_classes = discoverStrats(bots)
    # Build a quick lookup for strategies by name.
    strategy_dict = {cls.__name__: cls for cls in bot_classes}

    # Capture print output to return as a string
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer

    log = ''
    summary = ''

    try:
        table = Table()
        table.blinds[0] = int(smallblind)
        table.blinds[1] = int(smallblind) * 2

        name_map = dict()

        # If no strategies are found, return error as a tuple
        if not bot_classes:
            print("No bot strategies found! Cannot proceed.")
            return None, "No bot strategies found! Cannot proceed."

        # Decide how to create players
        if custom_config:
            # Use custom_config dictionary
            for strat_name, count in custom_config.items():
                if strat_name not in strategy_dict:
                    print(f"Warning: Strategy '{strat_name}' not found.")
                    # Return two values to avoid unpack errors
                    return None, f"Warning: Strategy '{strat_name}' not found."
                chosen_cls = strategy_dict[strat_name]
                for i in range(count):
                    player_name = f"{strat_name}{i+1}"
                    Hand(name=player_name, table=table, strategy_cls=chosen_cls, stack=int(stack))
                    name_map[player_name] = strat_name
        else:
            # Fall back to random if custom_config is None or empty
            if not botnumber:
                botnumber = 4
            print(f"Creating {botnumber} random bots.")
            strategy_counts = {}
            for i in range(int(botnumber)):
                chosen_cls = random.choice(bot_classes)
                cls_name = chosen_cls.__name__
                strategy_counts[cls_name] = strategy_counts.get(cls_name, 0) + 1
                player_name = f"{cls_name}{strategy_counts[cls_name]}"
                Hand(name=player_name, table=table, strategy_cls=chosen_cls, stack=int(stack))
                name_map[player_name] = cls_name

        # Ensure at least 2 players
        if len(table.players) < 2:
            print("Need at least 2 players to run a game.")
            return None, "Need at least 2 players to run a game."

        status = 'play'
        deck = Deck()
        max_hands = 50

        while status == 'play' and table.hands < max_hands:
            log += f"--- Starting Hand {table.hands} ---"
            deck.populate()
            deck.shuffle()
            pots = []

            pot = Pot(table, 'main')
            for player in table.players:
                pot.players.append(player)
                pot.active_players.append(player)
            pots.append(pot)

            pot.set_blinds()

            log += ' Blinds: ' + str(table.blinds)

            log = ante_up(pot, deck, log)

            while pot.stage < 4:
                log = deck.deal_to(table, log, Pot.deal_sequence[pot.stage], True)
                log += str(Pot.stage_dict[pot.stage]) + ' -- table: '
                log = table.print_cards(log)
                log = betting_round(pots[-1], table, log)

            if len(table.players) > 1:
                for p in pots:
                    log = showdown(p, log)

            # Increment hand count and update blinds every 6 hands
            table.hands += 1
            table.blinds_timer = table.hands % 6
            if table.blinds_timer == 5:
                table.blinds[:] = [x * 2 for x in table.blinds]

            # Remove busted players
            for player in table.players[:]:
                if player.stack <= table.blinds[1]:
                    log = player.bust(table, log)

            # End game if only one player remains
            if len(table.players) == 1:
                status = 'winner'

            log += '\n\n\n'
            next_hand(table, deck)
            log += f"--- Finished Hand {table.hands} ---\n"

        if table.hands >= max_hands:
            log += "Maximum hand limit reached, ending simulation."

        # If there's at least one player left, declare them winner
        for player in table.players:
            log += str(player.name) + ' wins the game!'
            table.winner = str(player.name)

        # Summarize results
        summary += "Game Summary:\n\n" + table.winner + " wins after " + str(table.hands) + " hands\n\n"
        for (player, hands) in table.busted:
            summary += player + " busted on round " + str(hands) + '\n'

    finally:
        sys.stdout = old_stdout

    # Combine summary and full log
    log = summary + '\n===========================================================================================================\n\nFull game log:\n\n' + log
    return (table.winner, name_map[table.winner]), log


def run_tournament(
    num_games: int,
    custom_config: dict,
    smallblind: int = 10,
    stack: int = 100,
    game_size: int = 8,     # How many players per game.
    min_players: int = 2    # Minimum number of distinct bots required.
):
    """
    Runs a tournament with a fixed number of games.
    Each game has game_size seats.
    
    The tournament distributes the total seats (game_size * num_games)
    as equally as possible among the selected bots from custom_config.
    
    custom_config is a dictionary like: {"StrategyName": (count, bot_info), ...}
    
    Returns:
       (scores, logs) -> (dict, str)
       - scores: a dict mapping winner's name to number of wins
       - logs: a complete log string for all games
    """
    import random
    from .poker import run_game

    # Build a list of players from custom_config.
    # Each entry is a tuple: (strategy name, unique bot id).
    player_list = []
    bot_info_map = {k: v[1] for k, v in custom_config.items()}
    for strat_name, (count, bot_info) in custom_config.items():
        for i in range(count):
            player_list.append((strat_name, f"{strat_name}{i+1}"))
    
    total_players = len(player_list)
    if total_players < min_players:
        raise Exception(f'{total_players} < {min_players}')
        # Return two values: empty scores + error message
        return {}, "Not enough players in config."

    total_seats = game_size * num_games

    # Determine how many times each bot should appear.
    base_count = total_seats // total_players
    remainder = total_seats % total_players

    # Build a seat pool: for each bot, include it base_count times,
    # plus one more if we still have 'remainder' seats left.
    seat_pool = []
    num_rounds_dict = dict()
    for bot in player_list:
        count_for_bot = base_count + (1 if remainder > 0 else 0)
        num_rounds_dict[bot[0]] = count_for_bot
        if remainder > 0:
            remainder -= 1
        for _ in range(count_for_bot):
            seat_pool.append(bot)

    # Shuffle the seat pool so that game groupings are random
    # random.shuffle(seat_pool) 

    new_seat_pool = [] # Smart shuffle
    while seat_pool:
        copies_in_game = {player[0]: 0 for player in player_list}
        for j in range(game_size):
            rand = random.choice(list(filter(lambda x: copies_in_game[x[0]] == min(copies_in_game.values()), seat_pool)))
            new_seat_pool.append(rand)
            seat_pool.remove(rand)
            copies_in_game[rand[0]] += 1
    seat_pool = new_seat_pool
    
    logs = []
    scores = dict()

    # Divide the seat pool into num_games chunks of game_size players
    for g in range(num_games):
        chunk = seat_pool[g * game_size: (g + 1) * game_size]
        # Build a mini_config for this game based on the chunk
        mini_config = {}
        for (sname, _) in chunk:
            mini_config[sname] = mini_config.get(sname, 0) + 1

        # run_game must return a two-element tuple
        (winner, winner_bot), game_log = run_game(
            custom_config=mini_config,
            smallblind=smallblind,
            stack=stack
        )

        # If 'winner' is None, it means run_game returned an error
        if not winner:
            # Optionally, handle error if needed
            logs.append(f"Game {g+1}: {game_log}\n\n")
            continue

        scores[winner] = (scores.get(winner, (0, (), 0))[0] + 1, bot_info_map[winner_bot], num_rounds_dict[winner_bot])
        # {bot: #wins, bot_info, #rounds}
        logs.append(f"=== Game {g+1}/{num_games} ===\n{game_log}\n\n")
    # raise Exception(str(scores))

    return scores, "".join(logs)


if __name__ == '__main__':
    # Example usage of run_game
    winner, full_log = run_game(4, 10, 1000)
    print(full_log)



"""
status='setup'

BLINDS=[10,20]

table=Table()

player1=Hand('Philip', table, 'SklanskySys2')
player2=Hand('Igor', table, 'SklanskySys2')
player3=Hand('Carol', table, 'SklanskySys2')
player4=Hand('Johnboy', table, 'SklanskySys2')
player5=Hand('Rob', table, 'SklanskySys2')
player6=Hand('Alex', table, 'SklanskySys2')
player7=Hand('Wynona', table, 'SklanskySys2')
player8=Hand('Timur', table, 'SklanskySys2')

deck=Deck()

status='play'

#for i in range (0,2):

while status=='play':

    #increment the table hand#

     
        
    

    #shuffle the deck
    
    deck.populate()
    deck.shuffle()

    #create pot for this hand
    pots=[]
    pot=Pot(table, 'main')
    
    
    
    for player in table.players:
            pot.players.append(player)
            pot.active_players.append(player)
            
    pots.append(pot)
    
    #allocate blinds and ante up

    pot.set_blinds()

    print ('Hand#'+str(table.hands))
    print ('Blinds: '+str(BLINDS))
    
    ante_up(pot)

    #debug(pot)
    #table.print_players()

    while pot.stage<4:
            
        deck.deal_to(table, Pot.deal_sequence[pot.stage], True)

        print (str(Pot.stage_dict[pot.stage]))
        
        table.print_cards()        	
             
        betting_round(pots[-1], table)
        
        #table.print_players()
       

    
    if len(table.players)>1:

        for pot in pots:
        
            showdown(pot)
            
         
    
    table.hands+=1
    table.blinds_timer=table.hands%6
    if table.blinds_timer==5:
        BLINDS[:] = [x*2 for x in BLINDS]
        
    for player in table.players[:]:
        	print (player.name, player.stack, BLINDS[1])
        	if player.stack<=BLINDS[1]:
        		
        		player.bust()
        		
    if len(table.players)==1:
    	status='winner'
    
          
    print ('\n\n\n')
    
    next_hand(table, deck)
    
for player in table.players:
	
	print (str(player.name)+' wins the game')
"""


