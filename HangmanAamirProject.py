
from customtkinter import *
from PIL import ImageTk, Image
import random
import mysql.connector as m
from tkinter import ttk
from CTkTable import *
import time

w=CTk()
w.geometry('900x500')
w.configure(bg="#28282B")
w.resizable(0,0) # can't resize now (0 0) or (False False)
w.title('Hangman')
set_appearance_mode("Dark")

w_height = 500
w_width = 900
display_width = w.winfo_screenwidth()
display_height = w.winfo_screenheight()

left = int(display_width/2 - w_width/2)
top = int(display_height/2 - w_height/2)
w.geometry(f'{w_width}x{w_height}+{left}+{top}')

w.minsize(900,500)
w.maxsize(900,500)


Home = True
# Berlin Sans FB
# Dubai
# Franklin Gothic Book

# database

db_user = input("Enter the user for the mySQL database : ")
db_pass = input("Enter the password for the mySQL database : ")

db = m.connect(host="localhost",user=db_user, password=db_pass,database="mysql")

cur = db.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS userdata (
username VARCHAR(255) primary key,
password VARCHAR(255) NOT NULL,
highscore INTEGER default 0
)    
""")


# Hangman game

score= 0
hangman_art = [
    "   +---+\n   |   |\n       |\n       |\n       |\n       |\n=========",
    "   +---+\n   |   |\n   O   |\n       |\n       |\n       |\n=========",
    "   +---+\n   |   |\n   O   |\n   |   |\n       |\n       |\n=========",
    "   +---+\n   |   |\n   O   |\n  /|   |\n       |\n       |\n=========",
    "   +---+\n   |   |\n   O   |\n  /|\\  |\n       |\n       |\n=========",
    "   +---+\n   |   |\n   O   |\n  /|\\  |\n  /    |\n       |\n=========",
    "   +---+\n   |   |\n   O   |\n  /|\\  |\n  / \\  |\n       |\n========="
]

def choose_word():
    index = random.randint(0, 853)
    file = open('words.txt', 'r')
    l = file.readlines()
    return l[index].strip('\n') # index to select an item of list l (a word) and stripping \n from it
    # readlines function keeps the \n that's with multiple line text so u have to remove it


def update_hangman(mistakes):
    hangman_label.configure(text=hangman_art[mistakes])

def check_guess(guess):
    global word_with_blanks

    if guess in word:
        if guess in word_with_blanks:
            used = CTkLabel(w, text="You've already used this letter", fg_color="#28282B", bg_color="#28282B")
            used.configure(font=('Berlin Sans FB', 30))
            used.place(relx=0.5, rely=0.2, anchor="center")

        for i in range(len(word)):
            if word[i]==guess:
                word_with_blanks = word_with_blanks[:i] + guess + word_with_blanks[i+1:]
        word_label.configure(text=word_with_blanks)

        if '_' not in word_with_blanks:
            end_game("win")

    else:
        global mistakes

        mistakes += 1
        update_hangman(mistakes)
        if mistakes == 6:
            end_game("lose")


def end_game(result):
    global score

    if result == 'win':
        result_text = "YOU WIN!"

        next_button = CTkButton(w, text="NEXT", font=("Berlin Sans FB", 30), fg_color="#12c4c0", hover_color='#0f9d9a',
                               text_color="#262626", command=game_start)
        next_button.place(relx=0.75, rely=0.50, anchor="center")

        score +=1

    else:
        cur.execute("select * from userdata where username = '{}' and password = '{}'".format(username,password1))
        record = cur.fetchone()
        #print(record)
        if record[2] == None:
            cur.execute(
                "UPDATE userdata SET highscore = '{}' where username = '{}' and password = '{}'".format(score, username,
                                                                                                        password1))

            l2 = CTkLabel(w, text="NEW HIGHSCORE!", fg_color="#28282B", bg_color="#28282B")
            l2.configure(font=('Berlin Sans FB', 30))
            l2.place(relx=0.75, rely=0.33, anchor="center")

        elif score > int(record[2]):

            cur.execute("UPDATE userdata SET highscore = '{}' where username = '{}' and password = '{}'".format(score, username, password1))

            l2 = CTkLabel(w, text="NEW HIGHSCORE!", fg_color="#28282B", bg_color="#28282B")
            l2.configure(font=('Berlin Sans FB', 30))
            l2.place(relx=0.75, rely=0.33, anchor="center")

        elif score == int(record[2]):
            print("Same score")

        else:
            print("No new score")


        result_text = "YOU LOSE!, The word was " +"'"+ word+"'"
        retry_button = CTkButton(w, text="RETRY", font=("Berlin Sans FB", 30), fg_color="#12c4c0", hover_color='#0f9d9a',
                               text_color="#262626", command=game_start)
        retry_button.place(relx=0.75, rely=0.50, anchor="center")

        db.commit()
        score = 0

    result_label.configure(text=result_text)

    guess_entry.delete(0, 'end')
    guess_entry.configure(state="disabled")
    guess_button.configure(state="disabled")


def default():

    f2 = CTkFrame(w,width=900,height=455,fg_color="#28282B")
    f2.place(x=0,y=45)

    l2= CTkLabel(w,text="Hangman",fg_color="#28282B")
    l2.configure(font=('Berlin Sans FB',120))
    l2.place(relx=0.5,rely=0.3,anchor="center")

    l3 = CTkLabel(w, text="The best decision you'll ever take, literally.", fg_color="#28282B")
    l3.configure(font=('Dubai', 30))
    l3.place(relx=0.5, rely=0.6, anchor="center")

    l4 = CTkLabel(w, text="An experience you won't forget.", fg_color="#28282B")
    l4.configure(font=('Dubai', 20))
    l4.place(relx=0.5, rely=0.66, anchor="center")

    l4 = CTkLabel(w, text="(No, I'm not gaslighting you.)", fg_color="#28282B")
    l4.configure(font=('Dubai', 20))
    l4.place(relx=0.5, rely=0.9, anchor="center")

def default_home():
    global Home

    f1.destroy()

    f2 = CTkFrame(w, width=900, height=455, fg_color="#28282B")
    f2.place(x=0, y=45)

    l2 = CTkLabel(w, text="Hangman", fg_color="#28282B")
    l2.configure(font=('Berlin Sans FB', 120))
    l2.place(relx=0.5, rely=0.3, anchor="center")

    l3 = CTkLabel(w, text="The best decision you'll ever take, literally.", fg_color="#28282B")
    l3.configure(font=('Dubai', 30))
    l3.place(relx=0.5, rely=0.6, anchor="center")

    l4 = CTkLabel(w, text="An experience you won't forget.", fg_color="#28282B")
    l4.configure(font=('Dubai', 20))
    l4.place(relx=0.5, rely=0.66, anchor="center")

    l4 = CTkLabel(w, text="(No, I'm not gaslighting you.)", fg_color="#28282B")
    l4.configure(font=('Dubai', 20))
    l4.place(relx=0.5, rely=0.9, anchor="center")

    Home = True

def Play():
    global Home
    global f2
    global user
    global password

    f1.destroy()
    f2 = CTkFrame(w,width=900,height=455, fg_color="#28282B")
    f2.place(x=0,y=45)

    l2= CTkLabel(w,text="LOGIN",fg_color="#28282B",bg_color="#28282B")
    l2.configure(font=('Berlin Sans FB', 90,'underline'))
    l2.place(relx=0.5,rely=0.3,anchor="center")


    user = CTkEntry(w,width=200,height=30,fg_color="#28282B",bg_color="#28282B",placeholder_text="Username")
    user.place(relx=0.5,rely=0.55,anchor="center")

    password = CTkEntry(w, width=200, height=30, fg_color="#28282B", bg_color="#28282B", placeholder_text="Password")
    password.place(relx=0.5, rely=0.62, anchor="center")
    password.configure(show="*")

    submit = CTkButton(w,text="SUBMIT",fg_color="#12c4c0", hover_color='#0f9d9a',text_color="#262626",command=login)
    submit.configure(font=("Dubai",15,'bold'))
    submit.place(relx=0.5,rely=0.7,anchor="center")

    Home = False

def login():
    global username
    global password1
    username = user.get()
    password1 = password.get()

    cur.execute("""
    select EXISTS(select * from userdata where username = '{}' and password = '{}') as mycheck;
    """.format(username, password1))

    check = cur.fetchone()


    if check[0] == 0:

        try:
            cur.execute("""insert into userdata(username,password) values('{}','{}')""".format(username, password1))
            game_start()
        except:

            l2 = CTkLabel(w, text="Incorrect Password", fg_color="#28282B", bg_color="#28282B")
            l2.configure(font=('Berlin Sans FB', 15))
            l2.place(relx=0.5, rely=0.8, anchor="center")

    else:

        l2 = CTkLabel(w, text="Login Successful!", fg_color="#28282B", bg_color="#28282B")
        l2.configure(font=('Berlin Sans FB', 15))
        l2.place(relx=0.5, rely=0.8, anchor="center")

        game_start()

    db.commit()

def clear_text():
    guess_entry.delete(0, 'end')

def game_start():

    global hangman_label, word, word_label, result_label, score
    global guess_entry, guess_button, mistakes, word_with_blanks

    time.sleep(0.5)
    f1.destroy()

    f3 = CTkFrame(w, width=900, height=455, fg_color="#28282B", bg_color="#28282B")
    f3.place(x=0, y=45)

    hangman_label = CTkLabel(w, font=("Courier", 30),fg_color="#28282B", bg_color="#28282B")
    hangman_label.place(relx=0.23,rely=0.5,anchor="center")

    l1 = CTkLabel(w, text=("Score : " + str(score)), fg_color="#28282B", bg_color="#28282B")
    l1.configure(font=('Berlin Sans FB', 30))
    l1.place(relx=0.75, rely=0.6, anchor="center")

    word = choose_word()
    print(word)
    word_with_blanks = "_" * len(word)
    word_label = CTkLabel(w, text=word_with_blanks, font=("Courier", 30), fg_color="#28282B", bg_color="#28282B")
    word_label.place(relx=0.5,rely=0.33,anchor="center")

    guess_entry = CTkEntry(w, width=100, font=("Arial", 20))
    guess_entry.place(relx=0.5, rely=0.5,anchor="center")
    guess_button = CTkButton(w, text="GUESS!",fg_color="#12c4c0", hover_color='#0f9d9a',text_color="#262626", command=lambda: [check_guess(guess_entry.get()),clear_text()])
    guess_button.configure(font=("Dubai", 15, 'bold'))
    guess_button.place(relx=0.5, rely=0.60,anchor="center")

    result_label = CTkLabel(w, text="",font=("Berlin Sans FB", 30), fg_color="#28282B", bg_color="#28282B")
    result_label.place(relx=0.5, rely=0.80,anchor="center")

    mistakes = 0
    update_hangman(mistakes)



def Leaderboard():
    global Home
    f1.destroy()

    f2 = CTkFrame(w,width=900,height=455, fg_color="#28282B")
    f2.place(x=0,y=45)

    l2= CTkLabel(w,text="Leaderboard",fg_color="#28282B")
    l2.configure(font=('Berlin Sans FB', 90))
    l2.place(relx=0.5,rely=0.2,anchor="center")

    l3 = CTkLabel(w, text="Username", fg_color="#28282B")
    l3.configure(font=('Dubai', 30))
    l3.place(relx=0.36,rely=0.35,anchor="center")

    l4 = CTkLabel(w, text="Highscore", fg_color="#28282B")
    l4.configure(font=('Dubai', 30))
    l4.place(relx=0.595, rely=0.35,anchor="center")


    # Table

    cur.execute("select * from userdata")
    records = cur.fetchall()


    value = [["                                 USERNAME OF PLAYER                                    ","                                HIGHSCORE ATTAINED BY PLAYER                                 "]]


    for i in range(len(records)):
        value.append([records[i][0],records[i][2]])


    table = CTkTable(master=w, row=len(records)+1, column=2, values=value,bg_color="#28282B")

    table.place(relx=0.5,rely=0.4,anchor="n")

    Home = False

def switchmode():
    if get_appearance_mode()=="Dark":
        set_appearance_mode("light")
    else:
        set_appearance_mode("dark")

def Help():
    global Home
    f1.destroy()
    f2 = CTkFrame(w,width=900,height=455, bg_color="#28282B",fg_color="#28282B")
    f2.place(x=0,y=45)

    l2= CTkLabel(w,text="Help",
                 bg_color="#28282B",
                 fg_color="#28282B")
    l2.configure(font=('Berlin Sans FB', 90))
    l2.place(relx=0.5,rely=0.2,anchor="center")

    l3= CTkLabel(w,text="HOW TO PLAY",
                 bg_color="#28282B",
                 fg_color="#28282B")
    l3.configure(font=('Berlin Sans FB',30,'underline'))
    l3.place(relx=0.15,rely=0.33,anchor="center")

    l4 = CTkLabel(w, text='''1) The object of hangman is to guess the secret word''',
                  bg_color="#28282B",
                  fg_color="#28282B")

    l4.configure(font=('Berlin Sans FB', 17))
    l4.place(relx=0.01,rely=0.4)

    l11 = CTkLabel(w,text="    before the stick figure is hung.",
                   bg_color="#28282B",
                   fg_color="#28282B")

    l11.configure(font=('Berlin Sans FB', 17))
    l11.place(relx=0.01, rely=0.45)

    l5 = CTkLabel(w,text="2) Players take turns selecting letters to narrow the word down.",
                  bg_color="#28282B",
                  fg_color="#28282B")

    l5.configure(font=('Berlin Sans FB',17))
    l5.place(relx=0.01,rely=0.51)

    l6 = CTkLabel(w,text="3) Players can take turns or work together.",
                  bg_color="#28282B",
                  fg_color="#28282B")

    l6.configure(font=('Berlin Sans FB',17))
    l6.place(relx=0.01,rely=0.57)

    l7 = CTkLabel(w,text="4) Gameplay continues until the players guess the word",
                  bg_color="#28282B",
                  fg_color="#28282B")

    l7.configure(font=('Berlin Sans FB', 17))
    l7.place(relx=0.01, rely=0.63)

    l8 = CTkLabel(w,text="    or they run out of guesses and the stick figure is hung."
                  ,bg_color="#28282B",
                  fg_color="#28282B")

    l8.configure(font=('Berlin Sans FB', 17))
    l8.place(relx=0.01, rely=0.68)

    l9 = CTkLabel(w,text="5) If you want to play with younger kids, use a snowman",
                  bg_color="#28282B",
                  fg_color="#28282B")

    l9.configure(font=('Berlin Sans FB', 17))
    l9.place(relx=0.01, rely=0.74)

    l10 = CTkLabel(w,text="    instead of a hangman to avoid scaring or offending anyone.",
                   bg_color="#28282B",
                   fg_color="#28282B")

    l10.configure(font=('Berlin Sans FB', 17))
    l10.place(relx=0.01, rely=0.79)

    lsupport = CTkLabel(w,text="Customer Support",
                        bg_color="#28282B",
                        fg_color="#28282B",)

    lsupport.configure(font=('Berlin Sans FB',35,'underline'))
    lsupport.place(relx=0.8,rely=0.4,anchor="center")

    lsupport = CTkLabel(w, text="aamirhasmi199@gmail.com",
                        bg_color="#28282B",
                        fg_color="#28282B")

    lsupport.configure(font=('Berlin Sans FB', 20))
    lsupport.place(relx=0.8, rely=0.47,anchor="center")

    modeswitch = CTkButton(w,
                           text="SWITCH MODE",
                           fg_color="#0f9d9a",
                           bg_color="#28282B",
                           hover_color="#006D6F",
                           command= switchmode)

    modeswitch.configure(font=('Berlin Sans FB',30))
    modeswitch.place(relx=0.8,rely=0.75,anchor="center")

    Home = False

def Credits():
    global Home
    f1.destroy()
    f2 = CTkFrame(w,width=900,height=455,
                  fg_color="#28282B")

    f2.place(x=0,y=45)

    l2= CTkLabel(w,text="Credits",
                 fg_color="#28282B")

    l2.configure(font=('Berlin Sans FB', 60))
    l2.place(relx=0.5,rely=0.18,anchor="center")

    l3 = CTkLabel(w, text="Copyright (c) 2023 Aamir Hashmi",
                  bg_color="#28282B",
                  fg_color="#28282B")

    l3.configure(font=('Berlin Sans FB', 20))
    l3.place(relx=0.5, rely=0.3, anchor="center")

    l4 = CTkLabel(w, text="Permission is hereby granted, free of charge, to any person",
                  bg_color="#28282B",
                  fg_color="#28282B")

    l4.configure(font=('Berlin Sans FB', 20))
    l4.place(relx=0.5, rely=0.35, anchor="center")

    l5 = CTkLabel(w, text="obtaining a copy of this software and associated documentation",
                  bg_color="#28282B",
                  fg_color="#28282B")

    l5.configure(font=('Berlin Sans FB', 20))
    l5.place(relx=0.5, rely=0.4, anchor="center")

    l6 = CTkLabel(w, text="files (the 'Software'), to deal in the Software without",
                  bg_color="#28282B",
                  fg_color="#28282B")

    l6.configure(font=('Berlin Sans FB', 20))
    l6.place(relx=0.5, rely=0.45, anchor="center")

    l7 = CTkLabel(w, text="restriction, including without limitation the rights to use,",
                  bg_color="#28282B",
                  fg_color="#28282B")

    l7.configure(font=('Berlin Sans FB', 20))
    l7.place(relx=0.5, rely=0.5, anchor="center")

    l8 = CTkLabel(w, text="copy, modify, merge, publish, distribute, sublicense, and/or sell",
                  bg_color="#28282B",
                  fg_color="#28282B")

    l8.configure(font=('Berlin Sans FB', 20))
    l8.place(relx=0.5, rely=0.55, anchor="center")

    l9 = CTkLabel(w, text="copies of the Software, and to permit persons to whom the",
                  bg_color="#28282B",
                  fg_color="#28282B")

    l9.configure(font=('Berlin Sans FB', 20))
    l9.place(relx=0.5, rely=0.6, anchor="center")

    l10 = CTkLabel(w, text="Software is furnished to do so, subject to the following conditions:",
                   bg_color="#28282B",
                   fg_color="#28282B")

    l10.configure(font=('Berlin Sans FB', 20))
    l10.place(relx=0.5, rely=0.65, anchor="center")

    l11 = CTkLabel(w, text="The above copyright notice and this permission notice shall be included",
                   bg_color="#28282B",
                   fg_color="#28282B")

    l11.configure(font=('Berlin Sans FB', 20))
    l11.place(relx=0.5, rely=0.75, anchor="center")

    l12 = CTkLabel(w,text="in all copies or substantial portions of the Software.",
                   bg_color="#28282B",
                   fg_color="#28282B")

    l12.configure(font=('Berlin Sans FB', 20))
    l12.place(relx=0.5, rely=0.8, anchor="center")

    l13 = CTkLabel(w, text="THE ABOVE CREDIT ETIQUETTE HAS BEEN ADDED PURELY FOR A PROFESSIONAL DISPLAY AND HUMOUR.",
                   bg_color="#28282B",
                   fg_color="#28282B")

    l13.configure(font=('Dubai', 12))
    l13.place(relx=0.5, rely=0.9, anchor="center")

    l14 = CTkLabel(w, text="THERE IS NO REAL COPYRIGHT TO THE GAME.",
                   bg_color="#28282B",
                   fg_color="#28282B")

    l14.configure(font=('Dubai', 12))
    l14.place(relx=0.5, rely=0.94, anchor="center")


    Home = False

def toggle_win():
    global Home
    global f1

    f1=CTkFrame(w,fg_color="#28282B")
    f1.place(relx=0,rely=0, relwidth=0.33,relheight=1)

    def bttn(x, y, text, bcolor, fcolor, cmd):

        myButton1 = CTkButton(f1,text=text,

                           fg_color='#262626',
                           width=300,
                           height=50,
                           border_width=0,
                           bg_color="#262626",
                           command=cmd,
                              hover_color=bcolor)

        myButton1.place(x=x, y=y)

    if Home==False:
        bttn(0, 343, "H O M E", '#0f9d9a', '#12c4c0', default_home)

    bttn(0, 75,"P L A Y", '#0f9d9a', '#12c4c0', Play)
    bttn(0, 128,"L E A D E R B O A R D", '#0f9d9a', '#12c4c0', Leaderboard)
    bttn(0, 181,"H E L P", '#0f9d9a', '#12c4c0', Help)
    bttn(0, 234, "C R E D I T S", '#0f9d9a', '#12c4c0', Credits)
    bttn(0, 287,"Q U I T", '#0f9d9a', '#12c4c0', exit)
    #bttn(0, 265, '', '#0f9d9a', '#12c4c0', None)


    def dele():
        f1.destroy()

    global img2
    img2 = CTkImage(Image.open('close.png'))

    CTkButton(f1,text="C L O S E",
              image=img2,
              command=dele,
              border_width=0
              ,bg_color='#262626',
              fg_color="#28282B",
              hover_color='#0f9d9a').place(x=0,y=10)


default() # calling before so that it doesnt cover menu button and the commands executed by it
img1=CTkImage(Image.open('openmenu2.jpg'))
CTkButton(w,
          text="M E N U",
          command=toggle_win,
          image=img1,
          border_width=0,
          fg_color="#252424",
          hover_color="#0f9d9a").place(x=0,y=10)

db.commit()
w.mainloop()
