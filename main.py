import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
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
        self.minsize(500, 300)
        self.title('Alfaaz - *untitled')

        # Variables
        self.bg_color = '#382929'
        self.fg_color = '#FFFFFF'
        self.bg_menu_color = '#2C2C2C'
        self.bg_menu_item_color = '#161616'
        self.bg_dark_theme_color = '#1E1E1E'
        self.fg_dark_theme_color = '#FFFFFF'
        self.color_light_blue = '#424141'

        self.configurations = self.loadConfigurations()
        self.configurations['saved'] = 0

        self.recent_file_to_open_var = tk.StringVar()
        self.dark_theme_var = tk.IntVar()
        self.text_var = tk.StringVar()
        self.fit_text_horizontally_var = tk.IntVar()
        self.font_type_var = tk.StringVar()
        self.font_color_var = tk.StringVar()
        self.font_color_var.set(self.configurations['fontColor'])
        self.font_type_var.set(self.configurations['fontType'])
        self.fit_text_horizontally_var.set(self.configurations['hScroll'])

        self.filetypes_to_use = (('Text files', '.txt'),
                                 ('CSV files', '.csv'),
                                 ('HTML', '.html htm'),
                                 ('All files', '*. *'))

        self.fonts = ['Arial', 'Bomber_Escort_Condensed', 'Courier', 'DejaVu_Sans_Mono', 'Droid_Sans_Fallback',
                      'Gayathri', 'Gayathri', 'Gubbi', 'Gurajada', 'KacstQurn', 'Kalimati', 'Khmer_OS_System',
                      'Lohit_Kannada', 'Lohit_Tamil_Classical', 'Lohit_Telugu', 'Mandali', 'Mukti',
                      'OpenSymbol', 'Pagul', 'Peddana', 'Purisa', 'Rachana', 'Rasa', 'Robot_Invaders',
                      'Samanata', 'Samyak_Devanagari', 'Standard_Symbols_PS', 'Tibetan_Machine_Uni', 'Timmana',
                      'Umpush']

        self.font_colors = ['White', 'Black', 'Blue', 'Cyan', 'DarkSlateGray', 'DarkCyan', 'Lightblue',
                            'PowderBLue', 'Purple', 'Indigo', 'DarkOrange', 'Orange', 'OrangeRed',
                            'Green', 'Red', 'Yellow', 'DimGray', 'Gray', 'Lavender', 'Tan']
        # Text Field
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.textField = tk.Text(self, relief=tk.FLAT)

        self.scroll_y = tk.Scrollbar(self,
                                     background='dimgray',
                                     activebackground='dimgray',
                                     width=10,
                                     bg='slategrey',
                                     troughcolor=self.bg_menu_color
                                     )
        self.scroll_x = tk.Scrollbar(self,
                                     background='dimgray',
                                     activebackground='dimgray',
                                     bg='slategrey',
                                     troughcolor=self.bg_menu_color,
                                     orient='horizontal'
                                     )

        self.textField.configure(yscrollcommand=self.scroll_y.set,
                                 xscrollcommand=self.scroll_x.set,
                                 border=0, relief=tk.FLAT,
                                 highlightthickness=0,
                                 wrap=tk.WORD,
                                 pady=5,
                                 padx=5,
                                 tabs=(25),

                                 )
        self.textField.config(insertwidth=3, font=(
            self.configurations['fontType'], self.configurations['fontSize']))
        self.textField.grid(sticky='nsew')

        self.scroll_y.config(command=self.textField.yview)
        self.scroll_x.config(command=self.textField.xview)

        self.scroll_y.grid(row=0, column=1, sticky='nse')

        # Decide whether hScroll is enabled or disabled
        self.fitTextHorizontally()

        self.textField.focus_set()

        # self.menu = tk.Menu(self)
        self.menu = tk.Menu(self, bg=self.bg_menu_color,
                            fg=self.fg_color,
                            font=("Verdana", 10),
                            activebackground=self.color_light_blue,
                            activeforeground="White",
                            activeborderwidth=0,
                            selectcolor='White',
                            border=0)
        self.configure(menu=self.menu, border=0, relief=tk.FLAT,)

        self.files_menu = tk.Menu(self,
                                  tearoff=0,
                                  background=self.bg_menu_color,
                                  activebackground=self.color_light_blue,
                                  activeforeground="White",
                                  foreground='White',
                                  border=0
                                  )
        self.menu.add_cascade(menu=self.files_menu,
                              label='File',
                              underline=0)

        self.files_menu.add_command(label='   New File'.ljust(33)+'Ctrl+N',
                                    underline=3,
                                    command=self.createNewFile)

        self.files_menu.add_command(label='   Open File'.ljust(33)+'Ctrl+O',
                                    underline=3,
                                    command=self.openFile)

        self.open_recent_files = tk.Menu(self, tearoff=0,
                                         background=self.bg_menu_color,
                                         activebackground=self.color_light_blue,
                                         activeforeground='White',
                                         foreground='White',
                                         border=0,
                                         selectcolor='White',)
        self.files_menu.add_cascade(menu=self.open_recent_files,
                                    label='   Open Recent',
                                    underline=5,
                                    command=self.showRecentFiles,
                                    )
        self.files_menu.add_separator()
        self.files_menu.add_command(label='   Save'+'Ctrl+S'.rjust(36),
                                    underline=3,
                                    command=self.saveFile)
        self.files_menu.add_command(label='   Save As'.ljust(24)+'Ctrl+Shift+S',
                                    underline=8,
                                    command=self.saveFileAs)
        self.files_menu.add_separator()

        self.files_menu.add_command(label='   Exit'.ljust(38)+'Ctrl+Q',
                                    underline=4,
                                    command=self.exitApplication)
        # Preferences Cascade
        self.preferences = tk.Menu(self, tearoff=0,
                                   background=self.bg_menu_color,
                                   activebackground=self.color_light_blue,
                                   activeforeground="White",
                                   foreground='White',
                                   border=0,
                                   selectcolor='White'
                                   )
        self.menu.add_cascade(menu=self.preferences,
                              label='Preferences',
                              underline=0)

        self.font_settings_menu = tk.Menu(self, tearoff=0,
                                          background=self.bg_menu_color,
                                          activebackground=self.color_light_blue,
                                          activeforeground="White",
                                          foreground='White',
                                          border=0,
                                          selectcolor='White',
                                          font=('Verdana', 10)
                                          )
        self.preferences.add_cascade(menu=self.font_settings_menu,
                                     underline=0,
                                     label='Font Settings'.ljust(30))

        self.font_settings_menu.add_command(label='   Font Size'.ljust(30),
                                            underline=8,
                                            command=self.changeFontSize)
        self.font_radio_menu = tk.Menu(self, tearoff=0,
                                       background=self.bg_menu_color,
                                       activebackground=self.color_light_blue,
                                       activeforeground="White",
                                       foreground='White',
                                       border=0,
                                       selectcolor='White',
                                       )

        for font in self.fonts:
            self.font_radio_menu.add_radiobutton(label=font,
                                                 variable=self.font_type_var,
                                                 command=self.changeFontType,
                                                 font=(font, 10))
        self.font_settings_menu.add_cascade(label='   Font Type',
                                            underline=8,
                                            menu=self.font_radio_menu)

        # Font Color Menu
        # Xam Mushki
        self.font_color_radio_menu = tk.Menu(self, tearoff=0,
                                             background=self.bg_menu_color,
                                             activebackground=self.color_light_blue,
                                             activeforeground="White",
                                             foreground='White',
                                             border=0,
                                             selectcolor='White',
                                             )
        i = 0
        for color in self.font_colors:
            if i == 2:
                self.font_color_radio_menu.add_separator()
            self.font_color_radio_menu.add_radiobutton(label=color,
                                                       variable=self.font_color_var,
                                                       command=self.changeFontColor,
                                                       foreground=color)
            i += 1
        self.font_settings_menu.add_cascade(label='   Font Color'.ljust(20),
                                            underline=8,
                                            menu=self.font_color_radio_menu)

        self.preferences.add_separator()

        self.preferences.add_checkbutton(label='Dark Theme',
                                         underline=0,
                                         variable=self.dark_theme_var,
                                         command=self.darkTheme,
                                         )

        self.preferences.add_checkbutton(label='Fit Text Horizontally',
                                         command=self.fitTextHorizontally,
                                         underline=9,
                                         variable=self.fit_text_horizontally_var)
        self.preferences.add_separator()

        self.preferences.add_command(label='Reset To Default',
                                     underline=0,
                                     command=self.resetSettings)

        # HELP Cascade
        self.help_menu = tk.Menu(self, tearoff=0,
                                 background=self.bg_menu_color,
                                 activebackground=self.color_light_blue,
                                 activeforeground="White",
                                 foreground='White',
                                 border=0,
                                 selectcolor='White')
        self.menu.add_cascade(menu=self.help_menu,
                              label='Help',
                              underline=0)
        self.help_menu.add_command(label='   Keyboard Shortcuts'.ljust(30),
                                   underline=3,
                                   state='disabled')
        self.help_menu.add_separator()
        self.help_menu.add_command(label='   About'.ljust(40),
                                   underline=3,
                                   command=self.showAbout)
        # Function calls at start
        self.doAtStart(self.configurations['fontColor'])

        # KEY BINDINGS SHORTCUTS
        #
        self.bind('<Control-n>', lambda event: self.createNewFile())
        self.bind('<Control-o>', lambda event: self.openFile())
        self.bind('<Control-s>', lambda event: self.saveFile())
        # uppercase S means Ctrl+Shift+s
        self.bind('<Control-S>', lambda event: self.saveFileAs())
        self.bind('<Control-q>', lambda event: self.exitApplication())

    # variables and functions
    # Xam Mushki
    def doAtStart(self, font_color):
        self.setTheme()
        self.showRecentFiles()
        self.textField.config(foreground=font_color)
        self.configurations['fontColor'] = font_color
        self.font_color_var.set(font_color)

    callReset = False

    def changeFontColor(self):
        font_color = self.font_color_var.get()
        self.configurations['fontColor'] = font_color
        self.saveConfigurations()
        self.textField.config(fg=self.configurations['fontColor'])

    def showAbout(self):
        photo = tk.PhotoImage(file='icon.png')
        messagebox.showinfo('About Alfaaz', 'Alfaaz is a simple but functional text editor, \
            that is developed using Python and Tkinter.\n\nDeveloper: Xam Mushki')

    # def openRecentFile(self,file):
    #     def fun():
    #         print(file)
    #     return fun
    def openRecentFile(self, file):
        def openOurFile():
            can_open_file = False
            # work around , bug , when 'Ctrl+o' is used instead of 'Open File' button in menu
            # hence used .strip() method to check
            # clearing the empty newlines
            temp_text = self.textField.get('1.0', 'end-1c').strip()
            self.textField.delete('1.0', 'end-1c')
            self.textField.insert('1.0', temp_text)
            #
            # First check the conditions same as checked when creating a new file.
            filename = os.path.join(self.configurations['path'],
                                    self.configurations['filename'])

            if self.configurations['saved'] == 0 and not self.textField.get('1.0', 'end-1c').strip() == '' or \
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
                        can_open_file = True
                elif result == None:
                    pass
                elif not result:
                    can_open_file = True
            else:
                can_open_file = True

            if can_open_file:
                if file:
                    self.resetEverything()
                    path_for_future_use, filename = os.path.split(file)
                    self.configurations['path'] = path_for_future_use
                    self.saveConfigurations()

                    with open(file, 'r') as f:
                        text = f.read()
                    self.textField.insert('1.0', text)
                    self.title('Alfaaz - '+filename)
                    self.configurations['filename'] = filename
                    self.configurations['saved'] = 1
        return openOurFile

    def showRecentFiles(self):
        recent_files = self.configurations['recentFiles']
        self.open_recent_files.delete(0, 'end')
        for rf in recent_files:
            path, filename = os.path.split(rf)
            self.open_recent_files.add_command(label='   ~'+rf.ljust(30),
                                               font=('Verdana', 10),
                                               command=self.openRecentFile(rf))
        self.open_recent_files.add_separator()
        self.open_recent_files.add_command(label='   Clear Recently Opened',
                                           command=self.clearRecentlyOpened)

    def clearRecentlyOpened(self):
        result = messagebox.askyesno(
            'Clear Recently Opened Files', 'Are you sure, you want to clear the recently opened file history?')
        if result:
            self.configurations['recentFiles'] = []
            self.saveConfigurations()
            self.showRecentFiles()
        else:
            pass

    def resetSettings(self):
        # self.configurations['path'] = '/'
        # self.configurations['filename'] = ''
        self.configurations['saved'] = 0
        self.configurations['fontSize'] = 15
        self.configurations['fontType'] = 'Arial'
        self.configurations['darktheme'] = 0
        self.configurations['fontColor'] = 'Black'
        self.saveConfigurations()

        self.textField.config(font=(
            self.configurations['fontType'],
            self.configurations['fontSize']),
            foreground='Black')
        self.setTheme()

    def changeFontType(self):
        font_type = self.font_type_var.get()
        self.configurations['fontType'] = font_type
        self.saveConfigurations()
        self.textField.config(
            font=(self.configurations['fontType'], self.configurations['fontSize']))

    def changeFontSize(self):
        result = simpledialog.askinteger('Font Size',
                                         'Enter Font Size (px)',
                                         minvalue=1,
                                         initialvalue=self.configurations['fontSize'])
        if result:
            self.configurations['fontSize'] = result
            self.saveConfigurations()
            self.textField.config(
                font=(self.configurations['fontType'], self.configurations['fontSize']))

    def createNewFile(self):
        filename = os.path.join(self.configurations['path'],
                                self.configurations['filename'])
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
            elif result == None:
                pass
            elif not result:
                self.resetEverything()
        else:
            self.resetEverything()

    def openFile(self):
        can_open_file = False
        # work around , bug , when 'Ctrl+o' is used instead of 'Open File' button in menu
        # hence used .strip() method to check
        # clearing the empty newlines
        temp_text = self.textField.get('1.0', 'end-1c').strip()
        self.textField.delete('1.0', 'end-1c')
        self.textField.insert('1.0', temp_text)
        #
        # First check the conditions same as checked when creating a new file.
        filename = os.path.join(self.configurations['path'],
                                self.configurations['filename'])

        if self.configurations['saved'] == 0 and not self.textField.get('1.0', 'end-1c').strip() == '' or \
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
                    can_open_file = True
            elif result == None:
                pass
            elif not result:
                can_open_file = True
        else:
            can_open_file = True

        if can_open_file:
            file_to_open = filedialog.askopenfilename(initialdir=self.configurations['path'],
                                                      title='Choose file',
                                                      filetypes=self.filetypes_to_use)
            if file_to_open:
                self.resetEverything()
                path_for_future_use, filename = os.path.split(file_to_open)
                self.configurations['path'] = path_for_future_use
                self.saveConfigurations()

                with open(file_to_open, 'r') as f:
                    text = f.read()
                self.textField.insert('1.0', text)
                self.title('Alfaaz - '+filename)
                self.configurations['filename'] = filename
                self.configurations['saved'] = 1

                # storing and will be used for opening recent files
                path = file_to_open
                if len(self.configurations['recentFiles']) <= 20:
                    if path in self.configurations['recentFiles']:
                        # that is, path already exist,
                        # now removing it ...
                        self.configurations['recentFiles'].remove(path)
                    # ... and placing it at index zero, since the list doesn't contain the path,
                    # because it is either removed in the above step or it wasn't stored in the first place.
                    self.configurations['recentFiles'].insert(0, path)
                else:
                    # len >20, remove last element/path
                    # and insert new path at index 0
                    del self.configurations['recentFiles'][-1]
                    self.configurations['recentFiles'].insert(0, path)

                self.saveConfigurations()
                # update the list in UI
                self.showRecentFiles()

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

            # storing and will be used for opening recent files
            if len(self.configurations['recentFiles']) <= 20:
                if path in self.configurations['recentFiles']:
                    # that is, path already exist,
                    # now removing it ...
                    self.configurations['recentFiles'].remove(path)
                # ... and placing it at index zero, since the list doesn't contain the path,
                # because it is either removed in the above step or it wasn't stored in the first place.
                self.configurations['recentFiles'].insert(0, path)
            else:
                # len >20, remove last element/path
                # and insert new path at index 0
                del self.configurations['recentFiles'][-1]
                self.configurations['recentFiles'].insert(0, path)

            self.saveConfigurations()
            # update the list in UI
            self.showRecentFiles()

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
            self.title('Alfaaz - '+filename)

            self.callReset = True

            # storing and will be used for opening recent files
            path = os.path.join(path_for_next_time, filename)
            if len(self.configurations['recentFiles']) <= 20:
                if path in self.configurations['recentFiles']:
                    # that is, path already exist,
                    # now removing it ...
                    self.configurations['recentFiles'].remove(path)
                # ... and placing it at index zero, since the list doesn't contain the path,
                # because it is either removed in the above step or it wasn't stored in the first place.
                self.configurations['recentFiles'].insert(0, path)
            else:
                # len >20, remove last element/path
                # and insert new path at index 0
                del self.configurations['recentFiles'][-1]
                self.configurations['recentFiles'].insert(0, path)

            self.saveConfigurations()
            # update the list in UI
            self.showRecentFiles()

    def writeTextFile(self, filename, text):
        with open(filename, 'w') as f:
            f.write(text)

    def readTextFile(self, filename):
        with open(filename, 'r') as f:
            return f.read()

    def exitApplication(self):
        filename = os.path.join(
            self.configurations['path'], self.configurations['filename'])
        if self.configurations['saved'] == 0 and not self.textField.get('1.0', 'end-1c') == '' or \
                self.configurations['saved'] == 1 and not self.readTextFile(filename) == self.textField.get('1.0', 'end-1c'):
            # that is,
            # file was not saved and the text field is not empty
            # or
            # file was saved but some new changes were made to the text
            result = messagebox.askyesno(
                'Exit without Saving', 'Are you sure, you want to exit without saving?')
            if result:
                self.destroy()
        else:
            # also used and called when window X/exit button is clicked from on_closing()
            result = messagebox.askyesno(
                'Exit Alfaaz', 'Are you sure, you want to exit?')
            if result:
                app.destroy()

    def fitTextHorizontally(self):
        val = self.fit_text_horizontally_var.get()
        if val:
            # that is, no horizontal scroll is disabled and
            # text in the textField is made to fit the width of the window
            self.scroll_x.grid_forget()
            self.textField.config(wrap=tk.WORD)
        else:
            self.scroll_x.grid(row=1, column=0, columnspan=2, sticky='swe')
            self.textField.config(wrap=tk.NONE)

        # storing value for next time use
        self.configurations['hScroll'] = val
        self.saveConfigurations()

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
                                  foreground='White',
                                  insertbackground='White')
            self.configurations['fontColor'] = 'White'
            self.font_color_var.set('White')
        else:
            self.dark_theme_var.set(0)
            self.textField.config(background='White',
                                  foreground='Black',
                                  insertbackground='Black',
                                  )
            self.configurations['fontColor'] = 'Black'
            self.font_color_var.set('Black')

        self.saveConfigurations()

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
                    'filename': '',
                    'saved': 0,
                    'fontSize': 15,
                    'fontType': 'Arial',
                    'fontColor': 'Black',
                    'hScroll': 1,
                    'recentFiles': []}
            return data

    def resetEverything(self):
        self.textField.delete('1.0', 'end')
        self.title('Alfaaz - *untitled')
        self.configurations['filename'] = ''
        self.configurations['saved'] = 0
        self.callReset = False
        # self.textField.insert('end','')


if __name__ == "__main__":
    app = App()

    def on_closing():
        app.exitApplication()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
