import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os
import pickle


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.my_screen_width = self.winfo_screenwidth
        self.my_screen_height = self.winfo_screenheight
        MyLeftPos = (self.winfo_screenwidth() - 1000) / 2
        myTopPos = (self.winfo_screenheight() - 500) / 2
        self.geometry("%dx%d+%d+%d" % (1000, 500, MyLeftPos, myTopPos))
        self.title('Notepad Alfaz - Untitled')

        # Variables
        self.bg_color = '#382929'
        self.fg_color = '#FFFFFF'
        self.bg_menu_color = '#474747'
        self.bg_dark_theme_color = '#2D2D2D'
        self.fg_dark_theme_color = '#FFFFFF'

        self.configurations = self.loadConfigurations()
        self.configurations['saved'] = 0

        self.dark_theme_var = tk.IntVar()
        self.fit_text_horizontally_var = tk.IntVar()
        self.text_var = tk.StringVar()

        self.filetypes_to_use = (('All files', '*.*'),
                                 ('CSV files', '.csv'),
                                 ('Text files', '.txt'),
                                 ('HTML', '.html'))
        # Text Field
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.textField = tk.Text(self, relief=tk.FLAT)

        self.scroll = tk.Scrollbar(self)
        self.textField.configure(yscrollcommand=self.scroll.set,
                                 border=0, relief=tk.FLAT,
                                 highlightthickness=0,
                                 wrap=tk.WORD,
                                 pady=5,
                                 padx=5,
                                 tabs=(25)
                                 )
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
                              command=self.createNewFile)

        self.menu.add_command(label='Open File',
                              underline=0,
                              command=self.openFile)
        self.menu.add_separator()
        self.menu.add_command(label='Save',
                              underline=0,
                              command=self.saveFile)
        self.menu.add_command(label='Save As',
                              underline=5,
                              command=self.saveFileAs)

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

    # variables and functions
    callReset = False

    def createNewFile(self):
        filename = os.path.join(
            self.configurations['path'], self.configurations['filename'])
        if self.configurations['saved'] == 0 and not self.textField.get('1.0', 'end-1c') == '' or \
                self.configurations['saved'] == 1 and not self.readTextFile(filename) == self.textField.get('1.0', 'end-1c'):
            # that is
            # file was not saved and the text field is not empty
            # or
            # file was saved but some new changes were made to the text
            result = messagebox.askyesnocancel(
                'Do you want to Save the changes?', 'Your changes will be lost if you don\'t save them.')
            if result:
                self.saveFile()
                if self.callReset:
                    self.resetEverything()
            elif result ==None:
                pass
            elif not result:
                self.resetEverything()
        else:
            self.resetEverything()
    

    def openFile(self):
        can_open_file =False
        # First check the conditions same as checked when creating a new file.
        filename = os.path.join(
            self.configurations['path'], self.configurations['filename'])
        if self.configurations['saved'] == 0 and not self.textField.get('1.0', 'end-1c') == '' or \
                self.configurations['saved'] == 1 and not self.readTextFile(filename) == self.textField.get('1.0', 'end-1c'):
            # that is
            # file was not saved and/but the text field is not empty
            # or
            # file was saved and/but some new changes were made to the text
            result = messagebox.askyesnocancel(
                'Do you want to Save the changes?', 'Your changes will be lost if you don\'t save them.')
            if result:
                self.saveFile()
                if self.callReset:
                    can_open_file=True
            elif result ==None:
                pass
            elif not result:
                can_open_file=True
        else:
            can_open_file=True
        
        if can_open_file:
            
            file_to_open = filedialog.askopenfilename(initialdir=self.configurations['path'],
                                                  title='Choose file',
                                                  filetypes=self.filetypes_to_use)
            if file_to_open:
                self.resetEverything()
                path_for_future_use,filename=os.path.split(file_to_open)
                self.configurations['path']=path_for_future_use
                self.saveConfigurations
                
                with open(file_to_open,'r') as f:
                    text = f.read()
                self.textField.insert('1.0',text)
                self.title('Notepad Alfaz - '+filename)
                self.configurations['filename'] = filename
                self.configurations['saved'] = 1
                
                

    def saveFile(self):
        # self.configurations['saved']=0
        text = self.textField.get('1.0', 'end-1c')
        if self.configurations['saved'] == 0:
            self.saveFileAs()
        else:
            # that is already saved once, now make changes in the same file
            path = os.path.join(
                self.configurations['path'], self.configurations['filename'])
            self.writeTextFile(path, text)
            self.callReset = True

    def saveFileAs(self):

        text = self.textField.get('1.0', 'end-1c')
        file_to_save = filedialog.asksaveasfilename(initialdir=self.configurations['path'],
                                                    title="Save file",
                                                    filetypes=self.filetypes_to_use)
        if file_to_save:
            path_for_next_time, filename = os.path.split(file_to_save)
            self.configurations['path'] = path_for_next_time
            self.configurations['filename'] = filename
            self.saveConfigurations()
            self.writeTextFile(file_to_save, text)
            self.configurations['saved'] = 1
            self.title('Notepad Alfaz - '+filename)

            self.callReset = True

    def writeTextFile(self, filename, text):
        with open(filename, 'w') as f:
            f.write(text)

    def readTextFile(self, filename):
        with open(filename, 'r') as f:
            return f.read()

    def quitApplication(self):
        filename = os.path.join(
            self.configurations['path'], self.configurations['filename'])
        if self.configurations['saved'] == 0 and not self.textField.get('1.0', 'end-1c') == '' or \
                self.configurations['saved'] == 1 and not self.readTextFile(filename) == self.textField.get('1.0', 'end-1c'):
            # that is
            # file was not saved and the text field is not empty
            # or
            # file was saved but some new changes were made to the text
            result = messagebox.askyesno(
                'Quit without Saving', 'Are you sure, you want to quit without saving?')
            if result:
                self.destroy()
        else:
            # also used and called when window X/quit button is clicked from on_closing()
            result = messagebox.askyesno(
                'Quit Notepad Alfaz', 'Are you sure, you want to quit?')
            if result:
                app.destroy()

    def testCommand(self):
        print('clicked')

    def fitTextHorizontally(self):
        print('Horizontal set')

    def darkTheme(self):
        # Storing the value of darktheme checkbox variable for future use.
        # TODO: use different method for storing
        self.configurations['darktheme'] = self.dark_theme_var.get()
        self.saveConfigurations()
        self.setTheme()

    def setTheme(self):
        # changing the value of self.dark_theme_var, that is the dark theme checkbox variable
        try:
            val = self.configurations['darktheme']
        except KeyError:
            val = 0
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

    def saveConfigurations(self):
        with open('configurations.bin', 'wb') as f:
            pickle.dump(self.configurations, f)

    def loadConfigurations(self):
        try:
            with open('configurations.bin', 'rb') as f:
                data = pickle.load(f)
                return data
        except FileNotFoundError:
            data = {'path': '/',
                    'filename':'',
                    'saved':0}
            return data

    def resetEverything(self):
        self.textField.delete('1.0', 'end')
        self.title('Notepad Alfaz - Untitled')
        self.configurations['filename'] = ''
        self.configurations['saved'] = 0
        self.callReset = False
        # self.textField.insert('end','')


if __name__ == "__main__":
    app = App()

    def on_closing():
        app.quitApplication()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
