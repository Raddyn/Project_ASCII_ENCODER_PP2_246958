import os
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox



class ASCIIapp:
    def __init__(self, window):
        # app init
        self.win = window
        window.title('ASCII shifter')
        window.iconbitmap('ascii.ico')
        window.geometry('400x500')
        window.resizable(False, False)
        window.eval('tk::PlaceWindow . center')

        # Button states and variables
        self.mode = tk.IntVar()
        self.key = tk.StringVar()
        self.keyval_scale = tk.IntVar()
        self.muew = []
        self.curr_key = 0

        # buttons
        self.butt_frame = tk.LabelFrame(window, text='modes')
        self.key_frame = tk.LabelFrame(window, text='key')
        self.enc_butt = tk.Radiobutton(self.butt_frame, text='encrypt', variable=self.mode, value=1)
        self.dec_butt = tk.Radiobutton(self.butt_frame, text='decrypt', variable=self.mode, value=2)
        self.brute_butt = tk.Radiobutton(self.butt_frame, text='bruteforce', variable=self.mode, value=3)
        self.key_scale = tk.Scale(self.key_frame, variable=self.keyval_scale, orient='horizontal', from_=0, to=94, 
                                  showvalue=0, command=self.Key_scale_update)
        self.key_entry = tk.Entry(self.key_frame, textvariable=self.key, width=30)
        self.Convert_button = tk.Button(window, text='CONVERT', width=10, command=self.modetest)
        self.Clear_butt = tk.Button(window, text='CLEAR', width=10, command=self.Clear)
        self.textbox = scrolledtext.ScrolledText(window, width=45, height=21)
        # grids
        self.butt_frame.grid(column=0, row=0, sticky='WN', pady=10, padx=20, rowspan=3)
        self.key_frame.grid(column=1, row=0, sticky='N', pady=10, padx=(0, 45), columnspan=2)
        self.enc_butt.grid(column=0, row=1, sticky='W', pady=(10, 0))
        self.dec_butt.grid(column=0, row=2, sticky='W')
        self.brute_butt.grid(column=0, row=3, sticky='WE', pady=(0, 10))
        self.key_entry.grid(column=0, row=0, sticky='WE', pady=2, padx=2)
        self.key_scale.grid(column=0, row=1, sticky='WE', pady=2, padx=2)
        self.Convert_button.grid(column=1, row=2, sticky='N', padx=(0, 45))
        self.Clear_butt.grid(column=2, row=2, sticky='N', padx=(0, 50))
        self.textbox.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky='W')
        # Menu
        self.Menu_bar = tk.Menu(window)
        window.config(menu=self.Menu_bar)
        self.file_menu = tk.Menu(self.Menu_bar, tearoff=0)
        self.about_menu = tk.Menu(self.Menu_bar, tearoff=0)
        self.Menu_bar.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Open', command=self.open_file)
        self.file_menu.add_command(label='Save As', command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Quit', command=self.Close_app)
        #
        self.Menu_bar.add_cascade(label='About', menu=self.about_menu)
        self.about_menu.add_command(label='About', command=self.popup_message)
        self.key_entry.insert('0', '0')

    def Key_scale_update(self, value) -> None:
        self.keyval_scale = value
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, value)

    def modetest(self):
        match self.mode.get():
            case 1:
                self.Shift()
            case 2:
                self.Shift()
            case 3:
                self.Brute_force()
            case _:
                self.popup_message('You must choose one of the modes!')

    def Shift(self, show=1, key=-1, clear=1) -> list[str]:
        '''
        Shifts the value of each char. Uses mode to determine how to use the key val
        '''
        inp_str = self.textbox.get("1.0", tk.END)
        temp = []
        if key == -1:
            temp_key = self.key_entry.get()
        else:
            temp_key = key
        if self.mode.get() == 1:
            mode = 1
        else:
            mode = -1
        if clear == 1:
            self.Clear()
        for i in inp_str:
            if i == '\n':
                temp.append(i)
            else:
                var = (ord(i) + int(temp_key) * mode)
                while var < 32:
                    var += 126 - 31  # Length of the interval
                while var > 126:
                    var -= 126 - 31
                temp.append(chr(var))
        if show == 1:
            self.Show(temp)
        else:
            return temp
        '''
         TODO: Zjisti proč to hází ten random poslední charakter :D = Hotovo,  je tam chyba u větších hodnot KURVA 
          -> VYŘEŠENO
        '''

    def Show(self, input) -> None:
        '''
        Shows inputed string in the scrolledtext textbox wiidget
        '''
        while input[-1] == '\n':  # Removes the last entry character,
            input.pop()  # without it the textbox always adds it for some reason
        content = ''.join(input)
        self.textbox.insert("1.0", content)

    def Clear(self) -> None:
        '''
        Deletes content of textbox widget
        '''
        self.textbox.delete(1.0, tk.END)

    def Close_app(self) -> None:
        self.Clear()
        self.win.quit()
        self.win.destroy()
        exit()

    def Brute_force(self) -> None:
        '''
        Tries to brute force the correct key value by trying every combination and comparing it to words from a file
        :return: None
        '''
        key_guess = []
        if not self.muew:
            cur_dir = os.getcwd()
            file_path = os.path.join(cur_dir, 'muew.txt')
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as file:
                        self.muew = file.read()
                        self.muew = ''.join(self.muew)
                        self.muew = self.muew.split('\n')
                except Exception as error:
                    self.popup_message(error)
                file.close()
                
        for key in range(94):
            key_guess.append(0)
            cipher = self.Shift(show=0, key=key, clear=0)
            cipher = ''.join(cipher)
            cipher = cipher.split()
            self.key = key
            for i in cipher:
                for o in self.muew:
                    if i == o:
                        key_guess[key] += 1

        print(max(key_guess))
        self.Shift(show=1, key=key_guess.index(max(key_guess)))
        self.Key_scale_update(key_guess.index(max(key_guess)))

    def save_file(self) -> None:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Text File")
        
        if not file_path:
            return

        try:
            with open(file_path, 'w') as file:
                file.write(self.textbox.get("1.0", tk.END))
                file.close()
        except Exception as error:
            self.popup_message(error)    

    def  popup_message(self, error = '') -> None:
        if error == '':
            about_text = 'Simple ASCII character based cipher app with built-in bruteforce method.\nMade by Radoslav Tomčala (246958) for PP2 class.\nIn Brno VUT FEKT 2023'
            messagebox.showinfo(title="About", message=about_text)
        else:
            messagebox.showinfo(title="About", message=error)
            
            


    def open_file(self) -> None:
        filepath = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                              filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as file:
                    content = file.read()
            except Exception as error:
                self.popup_message(error)
                return
            file.close()
            self.textbox.insert("1.0", content)
