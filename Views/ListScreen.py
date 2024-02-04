from tkinter import *
import Defaults as d
import CryptRepo.Cryptor as cryptor
import atexit



class MainScreen:

    def __init__(self):
        self.root = Tk()
        self.root.geometry('1280x720')
        self.root.title('Mijn eerste password manager')

        self.list_frame = Frame(self.root)
        self.list_scroll = Scrollbar(self.list_frame, orient=VERTICAL)
        self.listbox = Listbox(self.list_frame, width=40,
                               font=d.my_font, yscrollcommand=self.list_scroll.set)
        self.list_scroll.config(command=self.listbox.yview)
        self.list_scroll.pack(side=RIGHT, fill=Y)
        self.listbox.pack()
        self.list_frame.pack(pady=(10, 0))

        self.label_name = Label(self.root, text='Name',
                                font=(d.my_font, 14, 'bold'))
        self.label_name.pack(pady=(10, 0))

        self.name = Entry(self.root, font=(d.my_font, 12))
        self.name.pack(pady=(0, 0))

        self.label_pw = Label(self.root, text='Password',
                              font=(d.my_font, 14, 'bold'))
        self.label_pw.pack(pady=(10, 0))

        self.password = Entry(self.root, font=(d.my_font, 12))
        self.password.pack(pady=(0, 0))

        self.submit = Button(self.root, text="Add password",
                             font=(d.my_font, 12), width=15,
                             command=self.add_entry)
        self.submit.pack(pady=(10, 0))

        self.show = Button(self.root, text="Get password",
                           font=(d.my_font, 12), width=15,
                           command=self.display_selection)
        self.show.pack(pady=(5, 0))

        self.clear = Button(self.root, text="Delete selected",
                            font=(d.my_font, 12), width=15,
                            command=self.clear_item)
        self.clear.pack(pady=(5, 0))

        self.output_text = StringVar()
        self.output = Entry(self.root, textvariable=self.output_text,
                            font=(d.my_font, 12), state='readonly')
        self.output.pack(pady=(15, 0))

        self.crypto = cryptor.Cryptor()

        self.refresh_listbox()

    def add_entry(self):
        input_name = self.name.get()
        input_password = self.password.get()
        if not input_name or not input_password:
            return

        self.crypto.add_password(input_name, input_password)
        self.listbox.insert("end", input_name)

    def display_selection(self):
        for item in self.listbox.curselection():
            print(self.listbox.get(item))
        name = self.listbox.get(ANCHOR)
        self.output_text.set(self.crypto.get_password(name))

    def clear_item(self):
        name = self.listbox.get(ANCHOR)
        self.crypto.remove_password(name)
        self.refresh_listbox()

    def refresh_listbox(self):
        self.listbox.delete(0, 'end')
        for item in self.crypto.password_dict.keys():
            self.listbox.insert('end', item)

    def before_closure(self):
        self.crypto.save_password_file()

