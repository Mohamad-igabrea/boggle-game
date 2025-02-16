from tkinter import *
from ex12_utils import *
import tkinter.messagebox


class Game:
    def __init__(self):
        self.window = Tk()
        self.window.iconbitmap("pr_source.ico")
        self.window.title("Boggle Game")
        self.main_page()
        self.again = False
        self.user_name = ""
        self.current_word = ""
        self.founded_words = []
        self.current_path = []
        self.minutes = 3
        self.score = 0
        self.seconds = 00
        self.board = randomize_board()
        self.board_words = filtered_words(load_words_dict("boggle_dict.txt"), self.board)
        self.length_of_board_words = len(self.board_words)
        self.graph_of_board = [[Button, Button, Button, Button], [Button, Button, Button, Button]
            , [Button, Button, Button, Button], [Button, Button, Button, Button]]

    def main_page(self):
        "this is the main method that builds all the gestures of the game on the screeen"

        def delete_content(event):
            self.nik_name_box.delete(0, END)

        self.canvas = Canvas(self.window, width=1100, height=650)
        self.canvas_background = PhotoImage(file="op2.png")
        self.canvas.create_image(0, 0, image=self.canvas_background, anchor=NW)
        self.canvas.pack()
        self.frame = Frame(self.canvas, height=80, width=625, background="gray", highlightthickness=4
                           , highlightbackground="black")
        self.frame.place(x=267, y=80)
        label = Label(self.frame, text="welcome to our Boggle Game", font=("Arial", 32, "bold", "italic"), bg="gray")
        label.place(x=5, y=5)
        self.nik_name_box = Entry(self.canvas, bg="gray", fg="black", width=36, borderwidth=5, font=("family", 15)
                                  , highlightthickness=1)
        self.nik_name_box.place(x=310, y=305, height=65)
        self.nik_name_box.insert(0, "please enter your name then start:")
        self.nik_name_box.bind("<FocusIn>", delete_content)
        start_game_button = Button(self.canvas, text="Start Game!", width=15, font=("family", 11, "italic"), height=3,
                                   borderwidth=3, bg="gray", command=self.game_page)
        start_game_button.place(y=305, x=722)

    def game_page(self):
        "this method builds the game page and prints the rules of the game to the screen of the game"
        if self.again is False:
            if self.nik_name_box.get() == "please enter your name then start:" or len(self.nik_name_box.get()) == 0:
                self.user_name = "Ghost01"
                tkinter.messagebox.showinfo("The rules of the game", "in the game you should find words from the board"
                                                                     " as much as you could."
                                                                     "every button you pick should be beside last button you have picked."
                                                                     "\nyou can not pick the same button twice in one path "
                                                                     "every button 'legal' you pick will turn black."
                                                                     "\nif you pick the the last button you have chosen"
                                                                     " again you will delete it."
                                                                     "\nif you pick any another black button the whole word will"
                                                                     " be deleted."
                                                                     " \nif the path you have chosen turn green that is mean"
                                                                     "that this word is a legal word in the path to save it and"
                                                                     " earn points press any green button")
            else:
                self.user_name = self.nik_name_box.get()
                tkinter.messagebox.showinfo("The rules of the game", "in the game you should found words from the board"
                                                                     " as much as you could."
                                                                     "every button you pick should be beside last button you have picked."
                                                                     "\nyou can not pick the same button twice in one path "
                                                                     "every button 'legal' you pick will turn black."
                                                                     "\nif you pick the the last button you have chosen"
                                                                     " again you will delete it."
                                                                     "\nif you pick any another black button the whole word will"
                                                                     " be deleted."
                                                                     " \nif the path you have chosen turn green that is mean"
                                                                     "that this word is a legal word in the path to save it and"
                                                                     " earn points press any green button")
        self.canvas.destroy()
        self.canvas = Canvas(self.window, width=1100, height=650)
        self.canvas_background = PhotoImage(file="op1.png")
        self.canvas.create_image(0, 0, image=self.canvas_background, anchor=NW)
        self.canvas.pack()
        self.build_board()
        self.set_name(self.user_name)
        self.build_timer()
        self.change_time()
        self.build_score()
        self.build_exit_button()
        self.founded_words_frame()
        self.correct = Label(self.founded_frame, text="you did not found any word yet",
                        font=("family", 15), bg="black", fg="white")
        self.correct.place(y=5, x=5)
        self.founded_label = Label(self.canvas, text="Words you have found: "
                                        + str(len(self.founded_words)) + "/"
                                        + str(self.length_of_board_words), font=("family", 15), bg="black", fg="white")
        self.founded_label.place(x=50, y=115)

    def end_page(self):
        "this method ends the game page "
        self.canvas.destroy()
        self.canvas = Canvas(self.window, width=300, height=550, bg="black")
        self.canvas_background = PhotoImage(file="final_image.png")
        self.canvas.create_image(0, 0, image=self.canvas_background, anchor=NW)
        self.canvas.pack()
        game_over_frame = Label(self.canvas, text="Game Over", bg="black", fg="white", font=("family", 23))
        game_over_frame.place(x=68, y=10)
        text_over_frame = Label(self.canvas, text="Hi " + self.user_name + ", your score:", bg="black",
                                fg="white", font=("family", 15))
        text_over_frame.place(x=45, y=50)
        score_over_frame = Label(self.canvas, text=str(self.score), bg="black", fg="white", font=("family", 30))
        score_over_frame.place(x=130, y=90)
        words_over_frame = Frame(self.canvas, bg="black", width=280, height=155, highlightthickness=3,
                                 highlightbackground="skyblue")
        words_over_frame.place(x=11, y=335)
        if len(self.founded_words) == 0:
            label = Label(words_over_frame, text="you did not fond any word ", font=("family", 11), bg="black", fg="white")
            label.place(x=5, y=5)
        else:
            x = 3
            y = 3
            c = 0
            for i in range(len(self.founded_words)):
                c += 1
                if c == 22:
                    break
                label = Label(words_over_frame, text=self.founded_words[i], font=("family", 11), bg="black", fg="white")
                label.place(x=x, y=y)
                if y > 110:
                    y = 3
                    x += 90
                else:
                    y += 20
        again = Button(self.canvas, text="Play Again", font=("family", 12), bg="skyblue", command=self.play_again)
        again.place(y=500, x=11)
        again = Button(self.canvas, text="Exit Game", font=("family", 12), bg="#E75480", command=self.end_all)
        again.place(y=500, x=205)

    def end_all(self):
        "this method ends all builds you have builde to the game appear"
        self.window.destroy()

    def build_exit_button(self):
        "this method builds your exit button on the screen"
        self.exit_button = Button(self.canvas, text="End Game", width=13, font=("family", 11, "italic"), height=2,
                                   borderwidth=3, bg="gray", command=self.end_game_by_click)
        self.exit_button.place(y=580, x=925)

    def add_founded_words(self):
        "this method adds the words you have founded to your text box"
        y = 5
        x = 2
        self.correct.config(text="")
        for word in self.founded_words:
            self.correct = Label(self.founded_frame, text=word, font=("family", 15), bg="black", fg="white")
            self.correct.place(y=y, x=x)
            y += 30
            if y > 370:
                x = x + 90
                y = 5

    def build_frame_for_text(self):
        "this method builds the frame for your text box in the screen"
        self.text_box_frame = Frame(self.board_frame, width=342, height=50, bg="black")
        self.text_box_frame.place(x=0, y=0)

    def build_frame_for_letters(self):
        "this method builds your frame for the letters in the board"
        self.letters_frame = Frame(self.board_frame, width=342, height=342, bg="black")
        self.letters_frame.place(x=0, y=50)

    def build_board(self):
        "this method builds your board of letters"
        self.board_frame = Frame(self.canvas, width=350, height=400, bg="black", highlightthickness=4,
                                 highlightbackground="green")
        self.board_frame.place(x=700, y=155)
        self.build_frame_for_letters()
        x = 0
        y = 0
        for i in range(4):
            for j in range(4):
                self.graph_of_board[i][j] = Button(self.letters_frame, width=9, height=4, text=self.board[i][j]
                                                   , bg='gray', font=("family", 13),
                                                   command=self.help_change_board(self.board[i][j], (i, j)))
                self.graph_of_board[i][j].place(x=x, y=y)
                x += 85.5
                if x == 342:
                    y += 85.5
                    x = 0
        self.build_frame_for_text()
        self.build_text_box()

    def end_game_by_time(self):
        "this method ends the game if the time ends"
        tkinter.messagebox.showinfo("Time Over", "your time ran out do you want to play again?")
        self.end_page()

    def end_game_by_click(self):
        answer = tkinter.messagebox.askyesno("Game Over", "Are you sure?")
        if answer:
            self.window.after_cancel(self.after_timer)
            self.end_page()

    def win_the_game(self):
        self.window.after_cancel(self.after_timer)
        self.end_page()

    def build_timer(self):
        "this method builds your time appearence on the screnn"
        self.time_label = Label(self.canvas, text="3:00", width=8, height=2, font=("family", 23, "bold"),
                                fg="red", bg="black")
        self.time_label.place(x=790, y=20)

    def build_text_box(self):
        "this method builds your text of words on the game screen"
        self.text_box = Label(self.text_box_frame, text="", bg="white",
                              fg="black", width=31, height=2, font=("family", 14), justify=CENTER)
        self.text_box.place(x=0, y=0)

    def edit_text_box(self, name):
        "the method updates your text book when you find a word on the board"
        self.text_box.config(text=name)

    def change_time(self):
        "this method controls the time you have left on your screen"
        self.time_label.config(text=str(self.minutes) + ":" + str(self.seconds))
        if self.minutes == 0 and self.seconds == 00:
            self.window.after_cancel(self.after_timer)
            self.end_game_by_time()
        if self.seconds == 00:
            self.minutes -= 1
            self.seconds = 59
        else:
            self.seconds -= 1
        self.after_timer = self.window.after(1000, self.change_time)

    def build_score(self):
        self.score_label = Label(self.canvas, text="Your score: " + str(self.score), font=("family", 15),
                                 bg="black", fg="white")
        self.score_label.place(x=50, y=580)

    def change_points(self):
        "this method changes your total points when you guess a word right"
        self.score_label.config(text="Your score: " + str(self.score))

    def set_name(self, name):
        self.user_name_label = Label(self.canvas, text="Hello, " + name,
                               font=("family", 19), fg="white", bg="black")
        self.user_name_label.place(x=5, y=5)

    def change_founded_words(self, word):
        self.board_words.remove(word)
        self.founded_words.append(word)
        self.add_founded_words()
        self.founded_label.config(text="Words you have found: "
                                                 + str(len(self.founded_words)) + "/" + str(self.length_of_board_words))
        self.score = self.score + len(self.current_path) ** 2
        self.change_points()
        if len(self.board_words) == 0:
            self.win_the_game()

    def help_change_board(self, letter, coord):
        def change_board():
            coord_color = self.graph_of_board[coord[0]][coord[1]].cget("bg")
            board = self.graph_of_board
            if len(self.current_path) == 0:
                self.current_word += letter
                self.edit_text_box(self.current_word)
                self.current_path.append(coord)
                if self.current_word in self.board_words:
                    for cord in self.current_path:
                        board[cord[0]][cord[1]].config(bg="green", fg="white")
                else:
                    self.graph_of_board[coord[0]][coord[1]].config(bg="black", fg="white")
            elif coord_color == "green":
                for cord in self.current_path:
                    board[cord[0]][cord[1]].config(bg="gray", fg="black")
                self.change_founded_words(self.current_word)
                self.current_word = ""
                self.current_path = []
                self.edit_text_box(self.current_word)
            elif coord not in self.current_path and coord in legal_path(self.current_path[-1]):
                self.current_word += letter
                self.current_path.append(coord)
                self.edit_text_box(self.current_word)
                if self.current_word in self.board_words:
                    for cord in self.current_path:
                        self.graph_of_board[cord[0]][cord[1]].config(bg="green", fg="white")
                else:
                    for cord in self.current_path:
                        self.graph_of_board[cord[0]][cord[1]].config(bg="black", fg="white")
            elif coord == self.current_path[-1]:
                board[coord[0]][coord[1]].config(bg="gray", fg="black")
                self.current_path.pop()
                self.current_word = self.current_word[:-1]
                if self.current_word in self.board_words:
                    for cord in self.current_path:
                        self.graph_of_board[cord[0]][cord[1]].config(bg="green", fg="white")

                self.edit_text_box(self.current_word)
            elif coord_color == "black":
                for i in self.current_path:
                    self.graph_of_board[i[0]][i[1]].config(bg="gray", fg="black")
                self.current_word = ""
                self.current_path = []
                self.edit_text_box(self.current_word)
            elif coord not in self.current_path and coord not in legal_path(self.current_path[-1]):
                self.illegal_path()
        return change_board

    def illegal_path(self):
        "this method raises an error when you try to pick aletter that is not beside the last letter you have chosed"
        tkinter.messagebox.showerror("illegal path", "you have to pick a letter beside last letter you have chosen.")

    def play_again(self):
        "this method asks if you want to play the game again or not"
        self.current_word = ""
        self.founded_words = []
        self.current_path = []
        self.minutes = 3
        self.score = 0
        self.seconds = 00
        self.board = randomize_board()
        self.board_words = filtered_words(load_words_dict("boggle_dict.txt"), self.board)
        self.length_of_board_words = len(self.board_words)
        self.graph_of_board = [[Button, Button, Button, Button], [Button, Button, Button, Button]
            , [Button, Button, Button, Button], [Button, Button, Button, Button]]
        self.again = True
        self.game_page()

    def founded_words_frame(self):
        self.founded_frame = Frame(self.canvas, width=350, height=400, bg="black", highlightthickness=4,
                                   highlightbackground="green")
        self.founded_frame.place(y=155, x=50)

    def start_game(self):
        "this method starts the game"
        self.window.mainloop()


if __name__ == '__main__':
    game1 = Game()
    game1.start_game()
