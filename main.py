import tkinter as tk


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        MyLeftPos = (self.winfo_screenwidth() - 1000) / 2
        myTopPos = (self.winfo_screenheight() - 500) / 2
        self.geometry("%dx%d+%d+%d" % (1000, 500, MyLeftPos, myTopPos))
        self.title('Notepad')

        bg_color = '#382929'
        fg_color = '#FFFFFF'

        self.menu = tk.Menu(self, bg=bg_color, fg=fg_color)
        self.configure(menu=self.menu)

        self.menu_file = tk.Menu(self, tearoff=False)
        self.menu.add_cascade(menu=self.menu_file,
                              background=bg_color,
                              foreground=fg_color,
                              compound='right',
                              label='File')
        self.menu_file.add_command(label='  New File',
                                   command=lambda: self.testCommand())
        self.menu_file.add_command(label='  Open File',
                                   command=self.testCommand)
        self.menu_file.add_separator()
        self.menu_file.add_command(label='  Save',
                                   command=lambda: self.testCommand())
        self.menu_file.add_command(label='  Save As         ',
                                   command=self.testCommand)
        self.menu_file.add_separator()
        self.menu_file.add_command(label='  Quit',
                                   command=self.testCommand)
        self.menu.add_separator()

        self.menu.add_command(label='About',
                              command=self.testCommand)

    def testCommand(self):
        print('clicked')


if __name__ == "__main__":
    app = App()

    app.mainloop()
