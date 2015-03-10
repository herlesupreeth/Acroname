from tkinter import *
from tkinter import ttk
from tkinter import font
import sqlite3 as lite
import sys

#acro_dict = {}
con = lite.connect('acronym_data.db')

with con:
	cur = con.cursor()
	#cur.execute("DROP TABLE IF EXISTS Acronym")
	cur.execute("CREATE TABLE IF NOT EXISTS Acronym(Acro TEXT PRIMARY KEY, Exp TEXT)")

root = Tk()
root.title("Acronym Finder")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

acronym = StringVar()
acronym_expansion = StringVar()
edit_exp = StringVar()
program_output_message = StringVar()

acro_entry = ttk.Entry(mainframe, width=7, textvariable=acronym)
acro_entry.grid(column=2, row=1, sticky=(W, E))

appHighlightFont = font.Font(family='Cambria', size=12, weight='bold')
exp_entry = ttk.Entry(mainframe, width=50, textvariable=acronym_expansion, font=appHighlightFont)
exp_entry.grid(column=2, row=2, columnspan=3, sticky=(W, E))
exp_entry.state(['disabled'])

ttk.Label(mainframe, text="Acronym").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Acronym Expansion").grid(column=1, row=2, sticky=W)
ttk.Label(mainframe, textvariable=program_output_message).grid(column=1, row=3, columnspan=3, sticky=W)

def edit_checkbox_changed(*args):
	if edit_exp.get() == "edit":
		exp_entry.state(['!disabled'])
		acro_search_edit_button["text"] = "Edit"
	else:
		acro_search_edit_button["text"] = "Search"
		exp_entry.state(['disabled'])
	program_output_message.set("")

edit_check = ttk.Checkbutton(mainframe, text='Edit', command=edit_checkbox_changed, variable=edit_exp, onvalue="edit", offvalue="")
edit_check.grid(column=6, row=2, sticky=W)
edit_check.state(['disabled'])

def is_acronym_present(acro):
	with con:
		cur = con.cursor()
		cur.execute("SELECT * FROM Acronym WHERE Acro=?",(acro,))
		rows = cur.fetchall()
		if len(rows) > 0:
			return True
		else:
			return False
	#return acro in acro_dict

def edit_acronym(acro, edited_acro_exp):
	with con:
		cur = con.cursor()
		cur.execute("UPDATE Acronym SET Exp=? WHERE Acro=?", (edited_acro_exp, acro))
		con.commit()
		#print("Number of rows updated: %d" % cur.rowcount)
	#acro_dict[acro] = edited_acro_exp

def get_acro_expansion(acro):
	with con:
		cur = con.cursor()
		cur.execute("SELECT * FROM Acronym WHERE Acro=?",(acro,))
		row = cur.fetchone()
		if row != None:
			return row[1]
	#return acro_dict[acro]

def add_acro_expansion(acro, acro_exp):
	with con:
		cur = con.cursor()
		cur.execute("INSERT INTO Acronym VALUES(?, ?)", (acro, acro_exp))
		con.commit()
		#print("Number of rows updated: %d" % cur.rowcount)
	#acro_dict[acro] = acro_exp

def button_press(*args):
	if is_acronym_present(acronym.get()) and acronym.get() != "":
		edit_check.state(['!disabled'])
		if edit_exp.get() == "":
			acronym_expansion.set(get_acro_expansion(acronym.get()))
		elif edit_exp.get() == "edit":
			edit_acronym(acronym.get(), acronym_expansion.get())
			program_output_message.set("Edited Successfully!!")
	elif acronym.get() != "" and acro_search_edit_button["text"] != "Add":
		edit_check.state(['disabled'])
		exp_entry.state(['!disabled'])
		acro_search_edit_button["text"] = "Add"
		program_output_message.set("")
	elif acronym.get() != "" and acro_search_edit_button["text"] == "Add":
		edit_check.state(['disabled'])
		add_acro_expansion(acronym.get(), acronym_expansion.get())
		program_output_message.set("Added Successfully!!")

acro_search_edit_button = ttk.Button(mainframe, text="Search", command=button_press)
acro_search_edit_button.grid(column=6, row=3, sticky=W)

def reset_all(*args):
	edit_exp.set("")
	acronym_expansion.set("")
	program_output_message.set("")
	acro_search_edit_button["text"] = "Search"
	exp_entry.state(['disabled'])
	edit_check.state(['disabled'])

acronym.trace("w", reset_all)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

acro_entry.focus()
root.bind('<Return>', button_press)

root.mainloop()