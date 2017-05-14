#Connect Four
from tkinter import *
from random import randrange
import time
import sys


"""
Displays a loading bar in console
"""
#LoadingBar no longer needed if file is .pyw but makes no difference
class LoadingBar:
    def __init__(self, num_images):
        self.num_images = num_images
        self.length = num_images * 21 #frame count of each GIF image
        self.bar = ["-"] * self.length

    def increment_bar(self):
        for i in range(len(self.bar)):
            if self.bar[i] == "-":
                self.bar[i] = "|"
                print ('[%s]' % ''.join(map(str, self.bar)), "Loading")
                break


"""
GUI and logic class
"""
class ConnectFour:
    def __init__(self, parent):
        
        self.labels = [] #list of all 42 pieces
        self.turn_counter = 0 #keeps track of number of turns
        self.win_status = 0 #0 when playing, 1 when won
        
        self.empty_image = PhotoImage(file = "assets/empty.gif") #All slots begin with an "empty" image
        #self.empty_image.convert()
        self.blue_image = PhotoImage(file = "assets/blue.gif") #Blue slots
        self.red_image = PhotoImage(file = "assets/red.gif") #Red slots

        if randrange(0,5) == 0:
            self.blue_image = PhotoImage(file = "assets/blue_alt.gif")
            self.red_image = PhotoImage(file = "assets/red_alt.gif")

        #define piece dimensions
        self.height = 100
        self.width = 100

        for i in range(42):
            self.labels.append(Label(parent,
                                     image = self.empty_image,
                                     bg = "white", #background is white, can be changed
                                     width = self.width,
                                     height = self.height, #restricted to 96 so the images have no gaps
                                     ))
           
        #Places slots in grid
        piece_index = 0 #every piece has a unique identifier
        for c in range(7): #pieces are numbered from left to right
            for r in range(6,0,-1): #pieces are numbered bottom to top (hence the -1)
                self.labels[piece_index].grid(row = r,
                                              column = c,
                                              padx = 0,
                                              pady = 0,
                                              sticky = S) #places pieces in grid
                self.labels[piece_index].bind("<Button-1>", lambda event, coords = (r,c): self.column_click(event, coords)) #coordinates of each piece are passed to column_click
                piece_index += 1

    #Send a click to a specific column
    def column_click(self, event, coords):
        print("Turn", game.turn_counter + 1, "request to column", coords[1])
        if game.win_status == 0:
            columns[coords[1]].drop_piece(coords[1])
        else:
            print("Game has already been won!")
            
    #update an individual piece
    def redraw(self, c_ord, r_ord, piece_state): 

        self.c_ord = c_ord
        self.r_ord = r_ord
        self.piece_state = piece_state

        piece_index = r_ord + 6 * c_ord #recalculate unique piece identifier from 0 to 42 by row and column

        if self.piece_state == 1:
            self.labels[piece_index].configure(image = self.blue_image)
            for i in range(42):
                root.configure(cursor="@assets/cursor_red.cur")
        elif self.piece_state == -1:
            self.labels[piece_index].configure(image = self.red_image)
            for i in range(42):
                root.configure(cursor="@assets/cursor_blue.cur")
        #print("Drawing to column", self.c_ord, "and row", self.r_ord)
        
    #check all possible positions for a win
    def check_win(self):
        for i in range(len(columns)):
            print(columns[i].column)

        #check vertical conditions
        self.blue_vertical = [1, 1, 1, 1]
        self.red_vertical = [-1, -1, -1, -1]
        
        for i in range(len(columns)):
            if any(self.blue_vertical == columns[i].column[j:j+4] for j in range(3)): #Blue verticals
                blue_win.display_win_message()
            if any(self.red_vertical == columns[i].column[j:j+4] for j in range(3)): #Red verticals
                red_win.display_win_message()

        #check horizontal conditions
        for i in range(4): #only needs to check the first 4 columns
            for j in range(6): #check all 6 rows of each column

                subtotal = columns[i].column[j] + columns[i+1].column[j] + columns[i+2].column[j] + columns[i+3].column[j]
                if subtotal == 4: #Blue horizontals
                    blue_win.display_win_message()
                if subtotal == -4: #Red horizontals
                    red_win.display_win_message()

        #check diagonal conditions
        for i in range(4): #check the first 4 columns
            for j in range(3): #check the bottom 3 rows. A SW->NE diagonal can only start from the bottom three, or else it will not fit.
                subtotal = columns[i].column[j] + columns[i+1].column[j+1] + columns[i+2].column[j+2] + columns[i+3].column[j+3]
                if subtotal == 4: #Blue diagonals SW->NE
                    blue_win.display_win_message()
                if subtotal == -4: #Red diagonals SW->NE
                    red_win.display_win_message()

            for j in range(3, 6): #check the top 3 rows for the same reason as above.
                subtotal = columns[i].column[j] + columns[i+1].column[j-1] + columns[i+2].column[j-2] + columns[i+3].column[j-3]
                if subtotal == 4: #Blue diagonals NW->SE
                    blue_win.display_win_message()       
                if subtotal == -4: #Red diagonals NW->SE
                    red_win.display_win_message()

        #check if board is full (and do something about it)
        board_full = 1
        for i in range(7):
            for j in range(6):
                board_full *= columns[i].column[j]
        #print(board_full)
        if board_full != 0: #No pieces are empty because it only takes one piece == 0 to make the total 0.
            tie_win.display_win_message()


"""
Display appropriate win message for red, blue or tie, and run animations
"""
class Win_message:
    def __init__(self, root, team):
        
        self.root = root
        self.team = team
        self.frame_status = 0
        self.total_frame_num = 21 #length of GIF anim in frames
        self.frame_delay = 30 #in ms
        #grid contraction variables
        self.grid_total_frame_num = 9 #controls duration of contraction
        self.grid_multiplier = 3 #controls speed of contraction
        #button slide variables
        self.current_height = -0.1 #also the starting height
        self.final_height = 0.32 #actual stopping height will be greater and a multiple of increment_height
        self.increment_height = 0.02 #as a proportion of the window space
        #cursor animation variables
        self.cursor_state = 0
        self.cursor_total_states = 17 #multiples of 8 + 1 for the full loop
        self.cursor_delay = 100

        #refresh button, does the same as "play again"
        self.refresh_image = PhotoImage(file = "assets/refresh.gif")
        self.refresh_button = Label(image = self.refresh_image, bg = "#FFFFFF")
        self.refresh_button.place(relx = 0, rely = 0)
        self.refresh_button.bind("<Button-1>", lambda event: self.again())      

    #load animation frames. This is an individual method because it does not need to be called on 'Play Again', whereas everything else in __init__() needs to be reset.
    def load_frames(self):
        
        self.frames = []    
        #loads each frame to the list self.frames
        for i in range(self.total_frame_num):
            
            self.frames.append(PhotoImage(file = self.team, format = "gif -index " + str(i)))
            loading.increment_bar()

    #create the two buttons just once
    def place_buttons(self):
        
        game.win_status = 1 #game has been won, prevents slots from being clicked
        self.button_again = Button(text = "Play Again",
                                   command = self.again,
                                   height = 4,
                                   width = 20)
        self.button_again.place(relx = 0.25, rely = self.current_height)

        self.button_quit = Button(text = "Quit",
                                  command = self.quit_game,
                                  height = 4,
                                  width = 20)
        self.button_quit.place(relx = 0.55, rely = self.current_height)
        
        self.animate_buttons() #begin animation of buttons

    #animate the two buttons
    def animate_buttons(self):
        #drop the play again / quit buttons down
        if self.current_height < self.final_height:
            self.button_again.place(rely = self.current_height)
            self.button_quit.place(rely = self.current_height)
            self.current_height += self.increment_height
            
            self.root.after(self.frame_delay, self.animate_buttons)

    #animate the main win banner   
    def win_animation(self):
        
        self.winlabel = Label(background = "white", image = self.frames[self.frame_status])#creates label from first frame
        self.winlabel.place(relx = 0.5, rely = 1, anchor = S)
        
        for i in range(42):
            game.labels[i].lift() #pulls banner below the pieces
        
        if self.frame_status < self.total_frame_num:
            self.frame_status += 1 #cycles to next frame
            
        self.winlabel.configure(image = self.frames[self.frame_status - 1]) #refreshes frame
        #print("Displaying frame", self.frame_status)

        if self.frame_status < self.grid_total_frame_num:            
            for i in range(42):
                game.labels[i].configure(height = 100 - self.frame_status * self.grid_multiplier) #contracts grid at the same time as animated banner
        
        if self.frame_status < self.total_frame_num:
            self.root.after(self.frame_delay, self.win_animation) #keeps updating the image every 20ms
        else:
            self.place_buttons() #triggers button fall AFTER animation is complete to avoid a bug

    #JUST BECAUSE!
    def cursor_animate(self):
        self.cursors = ["@assets/frame0.cur",
                        "@assets/frame1.cur",
                        "@assets/frame2.cur",
                        "@assets/frame3.cur",
                        "@assets/frame4.cur",
                        "@assets/frame5.cur",
                        "@assets/frame6.cur",
                        "@assets/frame7.cur",
                        "@assets/frame0.cur"]
        root.configure(cursor = self.cursors[self.cursor_state % 8])
        self.cursor_state += 1
        
        if self.cursor_state < self.cursor_total_states:
            self.cursoranim = self.root.after(self.cursor_delay, self.cursor_animate)

    #initiates animations. Allows them to be split into their own methods.
    def display_win_message(self):
        self.win_animation()
        self.cursor_animate()
        
    def again(self):
        root.configure(cursor = "@assets/cursor_blue.cur")
        #restart board and memory
        for i in range(0,42):
            game.labels[i].grid_forget()
        game.__init__(root)
        blue_win.__init__(root, "blue")
        red_win.__init__(root, "red")
        for i in range(7):
            columns[i].__init__()
                
    def quit_game(self): #Contains both methods because one does not work in the IDE?
        root.destroy()
        sys.exit()         


"""
Manages individual columns 0-6
"""
class Memory:
    def __init__(self):
        #sets default state of empty
        self.column = [0 for i in range(6)] #Six pieces, from bottom to top

    def drop_piece(self, c_ord):

        self.c_ord = c_ord
        
        for i in range(len(self.column)):
            if self.column[i] == 0: #check if slot is empty
                if game.turn_counter % 2 == 0: #either make slot blue (1) or red (-1)              
                    self.column[i] = 1
                else:
                    self.column[i] = -1

                self.r_ord = i
                self.piece_state = self.column[i]
                #print("Column state:", self.column) #debug
            
                game.turn_counter += 1
                #print("Turn number:", game.turn_counter)

                game.redraw(self.c_ord, self.r_ord, self.piece_state) #draws colored piece at given coordinates
                game.check_win()
                
                break
            elif self.column[5] != 0:
                print("column full")
                break

        
"""
Main routine
"""
if __name__ == "__main__":
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    root.geometry("728x624")
    root.configure(bg="white", cursor="@assets/cursor_blue.cur")
    root.title("Connect Four | Logan Wu")
    loading = LoadingBar(3)
    game = ConnectFour(root)
    blue_win = Win_message(root, 'assets/bluewin.gif')
    red_win = Win_message(root, 'assets/redwin.gif')
    tie_win = Win_message(root, 'assets/tiewin.gif')
    blue_win.load_frames()
    red_win.load_frames()
    tie_win.load_frames()
    columns = []
    
    for i in range(7):
        columns.append(Memory())
    root.mainloop()
