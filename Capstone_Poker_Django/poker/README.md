# Poker

---
The "Poker" repository found at https://github.com/philipok-1/Poker was used as a starting point for the implementation of the poker tournament and game in this repository. The source files were extended to fit in with the Django framework, and additional changes were made for correctness and to eliminate bugs

#### __Changes from Source__

##### pokerhands\.py
- is_straight() was replaced with __straight_quality()__ which returns the list of 5 card values making up a straight, if there is one, otherwise None. 
- __from_straight()__ was added not for the execution of the game, but can be used in writing poker AI. It returns the minimum number of cards needed to complete a straight. __flush_value()__ determines the suit of which the hand has the most cards and returns the number of cards of that suit and a list of the corresponding values.
- __evaluate_hand()__ was reworked to ensure accurate evaluation, including proper prioritization. The new function checks for the tiers of hands listed in [this reference](https://www.cardplayer.com/rules-of-poker/hand-rankings) (with royal flush combined into straight flush) in the order listed, so the hands qualifying for multiple tiers are awarded the better. The new function returns an integer representing the hand tier and a list of 5 integers representing hand quality. 
- __quality__ lists the five card values comprising a hand for evaluation purposes. The values are in priority order, so a tie between multiple hands of the same tier can be broken by comparing elements of their respective qualities starting at the first index. For example, a player with the seven-card hand [7&diams; 2&hearts; A&diams; J&hearts; 2&clubs; K&spades; 4&spades;] would get a quality of [2, 2, A, K, J]. The twos must come first because they make up the pair, and they are followed by the highest remaining cards. For another example, a flush's quality would be the five (highest) cards in the flush suit in descending order.

##### poker\.py
 - __quality__ and __total_cards__ fields were added to Hand class and tie_break field removed. Tie-breaking procedure was adjusted accordingly in __showdown()__. __total_cards__ is a list containing the player's cards and the table cards.
 - __get_rep__ function was added for debugging and reporting purposes.
 - __out_string__ added as argument and return value to many functions to log events in the poker game.
 - __run_game()__ was reworked to incorporate other changes and parameterized for number of bots, blinds, starting stack size, and a custom configuration dictionary containing information about players and corresponding strategies. The new function returns the game winner and corresponding strategy name and the game log.
 - __run_tournament()__ was added to sequentially call __run_game()__ and assemble results. The function takes the same parameters as __run_game()__ in addition to number of games, number of players per game, and minimum number of distinct bots per game. It returns a map from strategy subclass to number of game wins, along with additional information needed for the database.