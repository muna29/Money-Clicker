import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pickle
import time
import math

class Player:
    def __init__(self):
        self.money = 0
        self.income_per_click = 1
        self.passive_income = 0
        self.click_multiplier = 1
        self.auto_clicker_level = 0

class Upgrade:
    def __init__(self, name, cost, income_increase, click_multiplier=1):
        self.name = name
        self.cost = cost
        self.income_increase = income_increase
        self.click_multiplier = click_multiplier

upgrades = [
    Upgrade("Basic Upgrade", 10, 2),
    Upgrade("Advanced Upgrade", 50, 5),
    Upgrade("Super Upgrade", 100, 10),
    Upgrade("Income Booster", 500, 50),
]

achievements = {
    100: "Hundredaire",
    1000: "Thousandaire",
    10000: "Ten-thousandaire",
    100000: "Hundred-thousandaire",
    1000000: "Millionaire"
}

milestones = {
    1000: "K",
    1000000: "M",
    1000000000: "B",
    1000000000000: "T"
}

def format_money(money):
    return f"${int(money):,}"

def click_to_earn_money(player, money_label):
    player.money += player.income_per_click * player.click_multiplier
    money_label.config(text=f"Money: {format_money(player.money)}")

def buy_upgrade(player, upgrade, money_label, income_label):
    if player.money >= upgrade.cost:
        player.money -= upgrade.cost
        player.income_per_click += upgrade.income_increase
        player.click_multiplier += upgrade.click_multiplier
        money_label.config(text=f"Money: {format_money(player.money)}")
        income_label.config(text=f"Income per click: {format_money(player.income_per_click * player.click_multiplier)}")
        messagebox.showinfo("Congratulations!", f"You bought {upgrade.name} for {format_money(upgrade.cost)}.")
    else:
        messagebox.showerror("Insufficient Funds", "Not enough money to buy this upgrade.")

def prestige(player, money_label):
    prestige_multiplier = 1 + (player.money // 1000000)  # Example: Prestige bonus for every million dollars
    player.money = 0
    player.income_per_click = 1
    player.click_multiplier = 1
    player.auto_clicker_level = 0
    money_label.config(text=f"Money: {format_money(player.money)}")
    messagebox.showinfo("Prestige", f"You have prestige! You earned a x{prestige_multiplier} bonus. Your progress has been reset.")
    player.money = prestige_multiplier

def update_notes():
    notes = """
    Version 1.5.5:
    - Fixed the glitch where the initial amount of money had two dollar signs.
    """
    messagebox.showinfo("Update Notes", notes)

def show_about():
    about_text = """
    Make Money Clicker Game v1.5.5

    Click the button to earn money and purchase upgrades to 
    increase your income per click. 
    Have fun and become a virtual millionaire!

    Developed by MCSN
    """
    messagebox.showinfo("About", about_text)

def show_known_bugs():
    bugs_text = """
    Known Bugs:
    
    1. Save Game button gives an error in the terminal.
    2. The window may not close on command.
    3. Progress may not be saved on window closure.
    """
    messagebox.showinfo("Known Bugs", bugs_text)

# Create and configure the main window
root = tk.Tk()
root.title("Make Money Clicker Game")
root.geometry("400x300")

# Initialize the player or load saved data
player = None
try:
    with open("savegame.dat", "rb") as file:
        player = pickle.load(file)
except Exception as e:
    print(f"Error loading game: {e}")
if player is None:
    player = Player()

# Create a Notebook (tabbed interface) to manage the game tabs
tab_control = ttk.Notebook(root)
tab_control.pack(fill="both", expand=1)

# Click Tab
click_tab = ttk.Frame(tab_control)
tab_control.add(click_tab, text='Click to Earn')

money_label = tk.Label(click_tab, text=f"Money: {format_money(player.money)}", font=("Helvetica", 16))
money_label.pack(pady=20)

income_label = tk.Label(click_tab, text=f"Income per click: {format_money(player.income_per_click * player.click_multiplier)}", font=("Helvetica", 12))
income_label.pack()

earn_button = tk.Button(click_tab, text="Click to Earn Money", command=lambda: click_to_earn_money(player, money_label))
earn_button.pack(pady=10)

# Upgrade Tab
upgrade_tab = ttk.Frame(tab_control)
tab_control.add(upgrade_tab, text='Upgrades')

def on_buy_upgrade(index):
    if index < len(upgrades):
        buy_upgrade(player, upgrades[index], money_label, income_label)

for index, upgrade in enumerate(upgrades):
    upgrade_button = tk.Button(upgrade_tab, text=f"Buy {upgrade.name} ({format_money(upgrade.cost)})", command=lambda i=index: on_buy_upgrade(i))
    upgrade_button.pack(pady=5)

prestige_button = tk.Button(upgrade_tab, text="Prestige", command=lambda: prestige(player, money_label))
prestige_button.pack(pady=10)

# Menu Bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Update Notes", command=update_notes)
help_menu.add_command(label="Help", command=lambda: messagebox.showinfo("Help", "Click the 'Click to Earn Money' button to earn money. Purchase upgrades to increase your income per click."))
help_menu.add_command(label="Save Progress", command=lambda: save_game(player))
help_menu.add_command(label="Known Bugs", command=show_known_bugs)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Save game on closing
def on_closing():
    try:
        with open("savegame.dat", "wb") as file:
            pickle.dump(player, file)
    except Exception as e:
        print(f"Error saving game: {e}")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main loop
root.mainloop()
