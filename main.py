from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(symbols) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)

    password_output.insert(0, password)
    pyperclip.copy(password)

    print(f"Your password is: {password}")

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website_name = (website_input.get()).title()
    email_username = email_input.get()
    new_password = password_output.get()
    new_data = {
        website_name: {
            "email": email_username,
            "password": new_password
        }
    }

    if len(website_name) == 0 or len(new_password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        # is_ok = messagebox.askokcancel(title=website_name, message=f"These are details entered: \nEmail: {email_username} "
        #                                                    f"\nPassword: {new_password} \nIs it okay to save?")
        # if is_ok:

        try:
            with open("data.json", "r") as data_file:
                #Reading old data
                j_data = json.load(data_file)
                #Updating old data with new data

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        else:
            j_data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(j_data, data_file, indent=4)

        finally:
            website_input.delete(0, END)
            password_output.delete(0, END)


def find_password():
    website_name = (website_input.get()).title()
    try:
        with open("data.json", "r") as data_file:
            file_content = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message=f"No data file found")

    else:
        if website_name in file_content:

                print(file_content[website_name])
                messagebox.showinfo(title="Password Details", message=f"Email: {file_content[website_name]["email"]} \n"
                                                                      f"Password: {file_content[website_name]["password"]}")

        elif website_name not in file_content:
            messagebox.showinfo(title="Error", message=f"No data for {website_name} found")



# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

padlock_img = PhotoImage(file="logo.png")

canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=padlock_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
website_input = Entry(width=30)
website_input.grid(column=1, row=1)
website_input.focus()

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
email_input = Entry(width=30)
email_input.grid(column=1, row=2)
email_input.insert(0, "(edit_name)@gmail.com")

password_label = Label(text = "Password:")
password_label.grid(column=0, row=3)
password_output = Entry(width=30)
password_output.grid(column=1, row=3)

generate_password_button = Button(text="Generate Password", command=generate_password, width=15)
generate_password_button.grid(column=2, row=3)

add_password_button = Button(text="Add", width=42, command=save)
add_password_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=15, bg="blue", fg="white", command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()