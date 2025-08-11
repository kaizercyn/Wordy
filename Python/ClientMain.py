import sys
from omniORB import CORBA
import wordyApp
import threading
import time
from AtomicBoolean import AtomicBoolean
from io import StringIO
from multiprocessing import Value


# from Wordy_idl import Word

class WordyClient:

    def __init__(self):
        self.orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
        obj = self.orb.string_to_object("corbaname::localhost:10000#WordyApp")
        self.servant = obj._narrow(wordyApp.Wordy)
        self.player = None
        self.timer_event = threading.Event()
        self.valid_words = []

    def display_menu(self):

        print("""
        ============================================
        |       Welcome to the Console Menu!       |
        |             1. PLAY                      |
        |             2. TOP PLAYERS               |
        |             3. TOP WORDS                 |
        |             4. LOGOUT                    |
        |             5. EXIT                      |
        |                                          |
        ============================================
        
        """)

    def get_user_choice(self):
        with StringIO() as buffer:
            choice = input("Enter your choice: ")
            return choice

    def get_entered_word(self, room_game, stop_flag):
        while not stop_flag.is_set():
            with StringIO() as buffer:
                entered_word = input("Enter word: ")
                word_entry_success = self.servant.userEnteredWord(entered_word, self.player, room_game)

            if (word_entry_success):
                self.valid_words.append(entered_word)
            else:
                print(f"Player's {entered_word} is invalid.")

    def perform_action(self, choice, player):

        def play():
            try:
                print("Waiting for other players...")
                room = self.servant.play(player)
                self.servant.addRoom(room.gameRoomID, room)
                print("Game found!")

                is_round_finished = AtomicBoolean(False)
                is_game_finished = AtomicBoolean(False)
                not_on_break = AtomicBoolean(True)
                accept_user_input = AtomicBoolean(True)
                round_number = 1

                while not is_game_finished.get():

                    if self.servant.getPlayerCount(room.gameRoomID) < 2:
                        print("\nNot Enough players remaining. Exiting game...")
                        self.servant.deleteRoom(room.gameRoomID)

                    if not_on_break.get():
                        accept_user_input.set(True)
                        room_random_letters = self.servant.getRoomRandomLetters(room.gameRoomID)
                        random_letters_length = len(room_random_letters)
                        print(f"\nRound {round_number}")
                        print("\n\nYou have 10 seconds to enter as much words as you can!")
                        print("Here are your letters: ")
                        print(room_random_letters)

                        stop_flag = threading.Event()
                        input_thread = threading.Thread(target=self.get_entered_word, args=(room, stop_flag))
                        if accept_user_input.get():
                            input_thread.start()

                        # start 10 second timer for the round
                        self.servant.startRoundTimer(room, 10)
                        # set initial time value on timer (10 seconds)
                        round_time_left = int(self.servant.getRoundTimer(room.gameRoomID))
                        round_timer_value = round_time_left

                        while round_timer_value >= 0:

                            try:

                                time.sleep(1)
                                round_time_left = int(self.servant.getRoundTimer(room.gameRoomID))
                                round_timer_value = round_time_left

                            except KeyboardInterrupt:
                                print("\nRound time thread was interrupted! >:o")

                            if round_timer_value == 0:
                                is_round_finished.set(True)
                                accept_user_input.set(False)
                                stop_flag.set()
                                print("\nTime's up! The round is over.")
                                break

                        # Wait for the input thread to finish before continuing
                        # print(f"Is the thread accepting user inputs before join? {input_thread.is_alive()}")
                        # input_thread.join()
                        # print(f"Is the thread accepting user inputs after join? {input_thread.is_alive()}")

                        if is_round_finished.get():
                            round_number += 1
                            stop_flag.set()
                            # Prints all of the player's entered words / dictates otherwise
                            if len(self.valid_words) > 0:
                                print("\nHere are your entered words for the round: ")
                                for e in self.valid_words:
                                    print(e)
                            else:
                                print("\nYou didn't enter any words this round:((")

                            # clear the player's valid_words for the round

                            self.valid_words.clear()
                            no_round_winner = False

                            try:
                                player_round_winner = self.servant.roundWinnerChecker(room)
                                print(f"\nRound Winner: {player_round_winner.username}")
                                if player_round_winner.username == self.player.username:
                                    print(
                                        f"\nYou won! Congratulations for winning the round {player_round_winner.username}.")
                                else:
                                    no_round_winner = True
                                    print("\nYou lost, better luck next round!")

                                print(f"Round log:")

                                if player_round_winner.username == self.player.username:
                                    print(f"Round Winner: {player_round_winner.username}")
                                    print("You won!")
                                else:
                                    no_round_winner = True
                                    print(f"Round Winner: {player_round_winner.username}")
                                    print(f"You Lost, better luck next round!")

                            except wordyApp.NoWinner as e:
                                if no_round_winner:
                                    print("\nNo round winner. Better luck next round.")
                            except wordyApp.TieResult as e:
                                if no_round_winner:
                                    print("A tie was detected. Better luck next round.")

                            # Check if a game winner is found:

                            # Game winner is found:
                            print(f"\nAnalyzing if a player has won... {self.servant.gameWinStateChecker(room)}")
                            if self.servant.gameWinStateChecker(room):
                                game_winner_player = self.servant.getGameWinner(room)
                                print(f"We have a winner! Victory goes to {game_winner_player.username}")
                                self.servant.decreasePlayerCount(room.gameRoomID)
                                is_game_finished.set(True)

                                # Start 5 second timer break before game ends

                                self.servant.startBreakTimer(room)

                                break_time_left = int(self.servant.getBreakTimer(room.gameRoomID))
                                round_break_timer_value = break_time_left

                                while round_break_timer_value >= 0:
                                    try:
                                        time.sleep(1)
                                        break_time_left = int(self.servant.getBreakTimer(room.gameRoomID))
                                        round_break_timer_value = break_time_left
                                    except KeyboardInterrupt:
                                        print("Break Timer thread has been interrupted >:o")

                                    if round_break_timer_value == 0:
                                        break
                                # end of while

                            # No game winner yet: continue
                            else:
                                room = self.servant.nextRoundHandler(room)

                                # get the next round's random letters
                                next_round_random_letters = self.servant.getRoomRandomLetters(room.gameRoomID)

                                # Start the 5 second break timer
                                self.servant.startBreakTimer(room)

                                # Initially sets the value of the break timer (always 5 seconds)
                                break_time_left = int(self.servant.getBreakTimer(room.gameRoomID))
                                round_break_timer_value = break_time_left

                                while round_break_timer_value >= 0:
                                    try:
                                        time.sleep(1)
                                        break_time_left = int(self.servant.getBreakTimer(room.gameRoomID))
                                        round_break_timer_value = break_time_left
                                    except KeyboardInterrupt:
                                        print("Break Timer thread has been interrupted >:o")

                                    if round_break_timer_value == 0:
                                        print("Preparing to start new round...")
                                        is_round_finished.set(False)
                                        not_on_break.set(True)
                                        break
                                # end of while
                            # end of else
                        # end of isRoundFinished

                        if is_game_finished.get():
                            self.servant.finishGame(player, room)
                            input_thread.join()
                            break
                # self.start_game(room)

            except wordyApp.NoPlayerJoined as e:
                print("\nNo player joined the game :(\n\n", str(e), "\n")
                self.run()
                # self.display_menu()
                # choice = self.get_user_choice()

        if choice == "1":
            play()

        elif choice == "2":
            print("TOP PLAYERS")
            leaderboards = self.servant.showLeaderBoard()
            for leaderboard in leaderboards:
                print(f"Rank: {leaderboard.rank}")
                print(f"Username: {leaderboard.playerName}")
                print(f"Wins: {leaderboard.numberOfWins}")
                print()

        elif choice == "3":
            print("TOP WORDS")
            longest_winners = self.servant.top5longestWords()
            for winner in longest_winners:
                print(f"Word Length: {winner.wordLength}")
                print(f"Username: {winner.playerName}")
                print(f"Word: {winner.longestWord}")
                print()

        elif choice == "4":
            print("\nTHANK YOU FOR USING OUR PROGRAM!\n ")
            if self.player:
                self.player = self.servant.logOffUser(self.player.username)
            sys.exit()

        elif choice == "5":
            if self.player:
                self.player = self.servant.logOffUser(self.player.username)
            print("FAREWELL!")
            sys.exit()

        else:
            print("Invalid choice. Please try again.")

    def prompt_for_input(self, prompt):
        while True:
            user_input = input(prompt)
            if user_input:
                return user_input

    def run_timer(self, timer_finished):
        self.servant.startTenSecondTimer(10)
        timer_finished.set()

    def display_message(self, message):
        print(message)

    def run(self):

        while True:
            # Check if the user is already logged in
            if self.player is not None:
                self.display_message("User is already logged in")
                self.display_menu()
                choice = self.get_user_choice()
                if not self.perform_action(choice, self.player):
                    break  # Exit the loop if user selects option 4
            else:
                username = self.prompt_for_input("Enter your username: ")
                password = self.prompt_for_input("Enter your password: ")

                try:
                    self.player = self.servant.login(username, password)
                    self.display_message(f"Logged in as player {self.player.username}")
                    while True:
                        self.display_menu()
                        choice = self.get_user_choice()
                        if self.perform_action(choice, self.player):
                            break  # Exit the loop if user selects option 4

                except wordyApp.IncorrectCredentials as e:
                    print("\nInvalid credentials. Please try again.\n\n")
                except wordyApp.AlreadyLoggedIn as e:
                    print("\nUser is already logged in.\n\n")


# Create an instance of WordyClient and run it
client = WordyClient()
client.run()
