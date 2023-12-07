from tkinter import Tk, Button, Label, Entry, PhotoImage, messagebox, END, mainloop
from os import path
import random
import string
import json

FONT = "Franklin Gothic Demi"
BG = "#172532"
directory = path.dirname(path.abspath(__file__))
letters = list(string.ascii_letters)
integers = list(string.digits)
misc = ['!', '#', '@', '-', '.', '(', ',', ')', '*', '?', '=']


def label(text, font, position, color="black"):
    text_label = Label(text=text, font=font, fg=color)
    text_label.grid(column=position[0], row=position[1])
    text_label.config(padx=4, pady=8)


def entry(position, name, span=2):
    name.grid(column=position[0], row=position[1], columnspan=span)
    name.focus()


def save():
    site = website.get()
    user = "".join(username.get().split())
    key = "".join(passkey.get().split())
    message = f"Website: {site}\nUsername: {user}\nPassword: {key}\nContinue to save?"
    new_data = {site: {"Username/Email": user, "Password": key}}
    if (all(["".join(site.split()), user, key])
            and messagebox.askokcancel(title="Save", message=message)):
        try:
            with open("data.json", mode="r") as data:
                old_data = json.load(data)
                old_data.update(new_data)
            with open("data.json", mode="w") as data:
                json.dump(old_data, data, indent=4)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open("data.json", mode="w") as data:
                json.dump(new_data, data, indent=4)
        add.config(text="Record added", state="disabled")
        screen.after(2700, lambda: add.config(text="Add", state="normal"))
        website.delete(0, END)
        username.delete(0, END)
        passkey.delete(0, END)
    elif not any(["".join(site.split()), user, key]):
        messagebox.showerror(title="Error", message="Please fill all the empty fields")


def password():
    password_list = [random.choice(letters) for _ in range(random.randint(6, 9))]
    password_list += [random.choice(misc) for _ in range(random.randint(2, 4))]
    password_list += [random.choice(integers) for _ in range(random.randint(3, 5))]

    random.shuffle(password_list)

    passcode = "".join(password_list)
    passkey.delete(0, END)
    passkey.insert(0, string=passcode)
    passkey.focus()
    passkey.select_range(0, END)


def search():
    find = website.get()
    if len(find) < 1:
        messagebox.showerror(title="Error", message="Please fill all the empty fields")
    else:
        try:
            with open("data.json", "r") as data:
                data_dict = json.load(data)
                username.delete(0, END)
                passkey.delete(0, END)
                username.insert(0, string=data_dict[find]["Username/Email"])
                passkey.insert(0, string=data_dict[find]["Password"])
                passkey.focus()
                passkey.select_range(0, END)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = open("data.json", mode="w")
            data.close()
            messagebox.showerror(title="No Records found",
                                 message=f"You have no saved passwords")
        except KeyError:
            messagebox.showerror(title="No Records found",
                                 message=f"No saved password found for {find}")


screen = Tk()
screen.title("Password Manager")
screen.geometry("800x600")
screen.resizable(False, False)
screen.config(pady=70, padx=70)
screen.iconbitmap(path.join(directory, "art", "appicon.ico"))
image = PhotoImage(file=path.join(directory, "art", "password_manager.png"))
icon = Label(image=image)
icon.grid(column=1, row=0)

label(text="Password Manager", font=(FONT, 24, "bold"), color=BG, position=(1, 1))
label(text="Website:", font=(FONT, 14), position=(0, 2))
label(text="Username/Email:", font=(FONT, 14), position=(0, 3))
label(text="Password:", font=(FONT, 14), position=(0, 4))

generate = Button(text="Generate", command=password, font=(FONT, 10), width=11, fg="white", bg=BG)
add = Button(text="Add", command=save, font=(FONT, 10), width=60, fg="white", bg=BG)
fetch = Button(text="Fetch", command=search, font=(FONT, 10), width=11, fg="white", bg=BG)
generate.grid(column=2, row=4)
add.grid(column=1, row=5, columnspan=2)
fetch.grid(column=2, row=2)

username = Entry(width=70)
entry((1, 3), name=username)
passkey = Entry(width=55)
entry((1, 4), name=passkey, span=1)
website = Entry(width=55)
entry((1, 2), name=website, span=1)

mainloop()
