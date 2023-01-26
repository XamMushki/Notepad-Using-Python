import tkinter as tk
from tkinter import messagebox


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.my_screen_width = self.winfo_screenwidth
        self.my_screen_height = self.winfo_screenheight
        MyLeftPos = (self.winfo_screenwidth() - 1000) / 2
        myTopPos = (self.winfo_screenheight() - 500) / 2
        self.geometry("%dx%d+%d+%d" % (1000, 500, MyLeftPos, myTopPos))
        self.title('Notepad - Untitled')

        # Variables
        self.bg_color = '#382929'
        self.fg_color = '#FFFFFF'
        self.bg_menu_color = '#474747'
        self.bg_dark_theme_color = '#2D2D2D'
        self.fg_dark_theme_color = '#FFFFFF'

        self.dark_theme_var = tk.IntVar()
        self.fit_text_horizontally_var = tk.IntVar()

        # Text Field
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.textField = tk.Text(self, relief=tk.FLAT)

        self.scroll = tk.Scrollbar(self)
        self.textField.configure(yscrollcommand=self.scroll.set,
                                 border=0, relief=tk.FLAT,
                                 highlightthickness=0,
                                 wrap=tk.WORD)
        self.textField.config(insertwidth=3, font=('Arial', 13))

        self.textField.grid(sticky='nsew')

        self.scroll.config(command=self.textField.yview)
        self.scroll.grid(row=0, column=1, sticky='nse')

        self.textField.focus_set()

        # self.menu = tk.Menu(self)
        self.menu = tk.Menu(self, bg=self.bg_menu_color,
                            fg=self.fg_color,
                            font=("Verdana", 10),
                            activebackground="#53728E",
                            activeforeground="white",
                            )
        self.configure(menu=self.menu, border=0, relief=tk.FLAT,)

        self.menu.add_command(label='New File',
                              underline=0,
                              command=self.testCommand)

        self.menu.add_command(label='Open File',
                              underline=0,
                              command=self.testCommand)
        self.menu.add_separator()
        self.menu.add_command(label='Save',
                              underline=0,
                              command=lambda: self.testCommand())
        self.menu.add_command(label='Save As',
                              underline=5,
                              command=self.testCommand)

        self.preferences = tk.Menu(self, tearoff=0,
                                   background=self.bg_menu_color,
                                   activebackground="#53728E",
                                   activeforeground="white",
                                   foreground='white')
        self.menu.add_cascade(menu=self.preferences,
                              label='Preferences',
                              underline=0)

        self.preferences.add_checkbutton(label='Dark Theme',
                                         underline=0,
                                         variable=self.dark_theme_var,
                                         command=self.darkTheme,
                                         )

        self.setTheme()
        # add horizontal continous text with scrollbar functinality
        # add x-axis scrollbar
        # change textField configurations
        self.fit_text_horizontally_var.set(1)
        self.preferences.add_checkbutton(label='Fit Text Horizontally',
                                         command=self.fitTextHorizontally,
                                         underline=9,
                                         variable=self.fit_text_horizontally_var,
                                         state='disabled')

        self.menu.add_command(label='Quit',
                              underline=0,
                              command=self.quitApplication)

    def quitApplication(self):
        on_closing()

    def testCommand(self):
        print('clicked')

    def fitTextHorizontally(self):
        print('Horizontal set')

    def darkTheme(self):
        # Storing the value of darktheme checkbox variable for future use.
        # TODO: use different method for storing
        with open('darktheme', 'w') as f:
            f.write(str(self.dark_theme_var.get()))
        self.setTheme()

    def setTheme(self):
        # changing the value of self.dark_theme_var, that is the dark theme checkbox variable
        with open('darktheme', 'r') as f:
            val = int(f.read())
            if val == 1:
                self.dark_theme_var.set(1)
                self.textField.config(background=self.bg_dark_theme_color,
                                      foreground='white',
                                      insertbackground='white')
                self.scroll.config()    # change color etc
            else:
                self.dark_theme_var.set(0)
                self.textField.config(background='white',
                                      foreground='black',
                                      insertbackground='black',
                                      )
                self.scroll.config()    # change color etc


if __name__ == "__main__":
    app = App()

    def on_closing():
        result = messagebox.askyesno('Quit', 'Are you sure, you want to quit?')
        if result:
            app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
