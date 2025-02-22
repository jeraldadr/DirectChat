import tkinter as tk
from tkinter import ttk, filedialog
from typing import Text
import ds_messenger
import Profile
import time


class Body(tk.Frame):


    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root, bg="#36393e")
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()
        

    def node_select(self, event):
        global entry
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        MainApp.recipient_selected(self, entry)
        if self._select_callback is not None:
            self._select_callback(entry)


    def del_contacts(self):
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)
        self._contacts = []


    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)


    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact, )


    def delete_messages(self):
        self.entry_editor.delete("1.0", "end")    


    def insert_user_message(self, message:str):
        self.entry_editor.tag_configure('start', foreground='blue')
        self.entry_editor.tag_configure('mid', foreground='white')
        self.entry_editor.insert(tk.END, account.username, ('start'))
        self.entry_editor.insert(tk.END, ': ' + message + '\n', ('entry-left', 'mid'))
        self.entry_editor.yview(tk.END)


    def insert_contact_message(self, message:str):
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        self.entry_editor.tag_configure('end', foreground='red')
        self.entry_editor.tag_configure('middle', foreground='white')
        self.entry_editor.insert(tk.END, entry, ('end'))
        self.entry_editor.insert(tk.END, message + '\n', ('entry-left', 'middle'))
        self.entry_editor.yview(tk.END)
        #self.entry_editor.tag_add("start", len(entry))
        #self.entry_editor.tag_config("start", foreground="red")


    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end',).rstrip()


    def set_text_entry(self, text:str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)


    def insert_friends(self):
        self.posts_tree.insert("", "0", values= account.friends)


    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250, bg='#1e2124')
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        #self.posts_tree.bind("<<TreeviewSelect>>", ))
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)
        self.posts_tree.heading("#0", text='Contacts')
        style = ttk.Style(master=self)
        style.theme_use("classic")
        style.configure("Treeview.Heading", background="#1e2124", foreground="#FFFFFF")
        style.map("Treeview.Heading", background=[('selected','#424549')], foreground=[('selected', '#FFFFFF')])
        style.configure('Treeview', background="#36393e", fieldbackground='#36393e', foreground='#000000')
        style.map('Treeview', background=[('selected', '#575c5c')], foreground=[('selected','#FFFFFF')])

        entry_frame = tk.Frame(master=self, bg="#36393e")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="#36393e")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="#36393e", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="#36393e")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5, bg='#424549', fg='#FFFFFF', insertbackground='#FFFFFF')
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)
        self.entry_editor = tk.Text(editor_frame, width=0, height=5, bg='#36393e')
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)
        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview, bg="#1e2124", activebackground='#282b30', background='#1065BF')
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    def __init__(self, root, send_callback=None,):
        tk.Frame.__init__(self, root, bg='#36393e')
        self.root = root
        self._send_callback = send_callback
        self._draw()


    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()


    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20, command=self.send_click, bg='#7289da', activebackground='#7289da') 
        # You must implement this. DONE
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.", bg='#36393e')
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)


    def body(self, frame):
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry['show'] = '*'
        self.password_entry.pack()
    
    
        # You need to implement also the region for the user to enter DONE
        # the Password. The code is similar to the Username you see above
        # but you will want to add self.password_entry['show'] = '*'
        # such that when the user types, the only thing that appears are
        # * symbols.
        #self.password...


    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        self.direct_messenger = ds_messenger.DirectMessenger()
        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.
        #self.direct_messenger = ... continue!

        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        self.body.posts_tree.bind("<<TreeviewSelect>>", self.previous_messages)


    def previous_messages(self, discard=None):
        try:
            try:
                message_lst = acc.retrieve_new()
                if message_lst != []:
                    for i in message_lst:
                        account.messages.append(i)
            except:
                pass
            if account.messages == []:
                message_list = acc.retrieve_all()
                account.messages = message_list
                account.save_profile(namefile)
            self.body.delete_messages()
            bubble_sort()
            account.save_profile(namefile)
            try:
                index = int(self.body.posts_tree.selection()[0])
                entry = self.body._contacts[index]
                for dct in account.messages:
                    if dct['from'] == entry:
                        message = ': ' + dct['message']
                        self.body.insert_contact_message(message)
                    elif dct['from'] == 'myself' and dct['to'] == entry :
                        message = dct['message']
                        self.body.insert_user_message(message)
                main.after(2000, self.previous_messages)
            except:
                main.after(2000, self.previous_messages)
        except:
            main.after(2000, self.previous_messages)


    def insert(self):
        self.body.insert_friends()


    def send_message(self):
        message = self.body.get_text_entry()
        if message == '':
            return
        else:
            self.body.insert_user_message(message)
            self.body.set_text_entry('')
            index = int(self.body.posts_tree.selection()[0])
            entry = self.body._contacts[index]
            try:
                acc.send(message, str(entry))
            except NameError:
                return
            directmsg = {"message": message, "from": 'myself', "to": str(entry),  "timestamp": str(time.time())}
            account.messages.append(directmsg)
            account.save_profile(namefile)
            
          
    def add_contact(self):
        contact = tk.simpledialog.askstring('Add contact', 'Enter contact name: ')
        self.body.insert_contact(contact)
        if contact not in account.friends:
            account.friends.append(contact)
            account.save_profile(namefile)


    def recipient_selected(self, recipient):
        self.recipient = recipient


    def configure_server(self):
        ud = NewContactDialog(self.root, "Configure Account",
        self.username==None, self.password==None, self.server==None)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        account.username = ud.user
        account.password = ud.pwd
        account.dsuserver = ud.server
        account.save_profile(namefile)
        acc.username = ud.user
        acc.password = ud.pwd
        acc.dsuserver = ud.server


    def check_new(self):
        try:
            message_lst = acc.retrieve_new()
            if message_lst != []:
                for i in message_lst:
                        account.messages.append(i)
            self.previous_messages
            main.after(2000, self.previous_messages)
        except:
            return
        

    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root, tearoff=False)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar, tearoff=False)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command = self.new)
        menu_file.add_command(label='Open...', command= self.open)
        menu_file.add_command(label='Close', command=self.log_out)

        settings_file = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


    def new(self):
        global namefile
        newusr = tk.filedialog.asksaveasfilename()
        x = new_create_profile(newusr)
        if x == False:
            return
        else:
            app.body.del_contacts()
            account.load_profile(newusr)
            account.username = None
            account.password = None
            account.dsuserver = None
            namefile = newusr
        
            
    def open(self):
        global acc
        global namefile
        openusr = tk.filedialog.askopenfile()
        try:
            account.load_profile(openusr.name)
        except Profile.DsuFileError:
            tk.messagebox.showinfo(title='Error', message='Please open a file ending in .DSU')
        app.body.del_contacts()
        for i in account.friends:
            app.body.insert_contact(i)
        namefile = openusr.name
        acc.dsuserver = account.dsuserver
        acc.username = account.username
        acc.password = account.password
       

    def log_out(self):
        if tk.messagebox.askokcancel(title='Close', message='This will close the application. Proceed?'):
            main.destroy()
   

def acc_file(login):
    global namefile
    global file
    file = tk.filedialog.askopenfile()
    try:
        namefile = file.name
    except AttributeError:
        return
    if len(namefile) > 50:
        path = namefile[:49] + "..."
    else:
        path = namefile
    try:
        file_name.destroy()
    except:
        pass
    file_name = tk.Label(login, text=path, width=50,justify='center', font="Helvetica 14", bg="#36393e", fg="#FFFFFF")
    file_name.place(relx=0.25,rely=0.15)
    return file


def acc_directory(create):
    global directory
    directory = tk.filedialog.askdirectory()
    if len(directory) > 50:
        direct = directory[:49] + "..."
    else:
        direct = directory
    file_name = tk.Label(create, text=direct, justify='center', font="Helvetica 14", bg="#36393e", fg='#FFFFFF')
    file_name.place(relx=0.25,rely=0.15)
    return directory


def new_create_profile(newpath):
    try:
        with open(newpath, 'x') as f:
            prof = Profile.Profile()
            prof.dsuserver = None
            prof.username = None
            prof.password = None
            try:
                prof.save_profile(newpath)
                return prof
            except Profile.DsuFileError:
                tk.messagebox.showinfo(title='Error', message='Please create a file ending in .DSU')
                return False
    except FileExistsError:
        pass


def create_profile(name=None, direct=None, dsuserver=None, user=None, pwd=None):
    global prof
    file_to_open = direct + "/" + name + '.dsu'
    try:
        with open(file_to_open, 'x') as f:
            prof = Profile.Profile()
            prof.dsuserver = dsuserver
            prof.username = user
            prof.password = pwd
            prof.save_profile(file_to_open)
            return prof
    except FileExistsError:
        yes = tk.Label(login, text="File already exists.", bg='#36393e', fg="#fa777c")
        yes.place(relx=0.5,rely=0.01)
        return False
    except PermissionError:
        yes = tk.Label(login, text="Error, please try again.", bg='#36393e', fg="#fa777c")
        yes.place(relx=0.5,rely=0.01)
        return False


def acc_login(user, pwd):
    global account
    global acc
    fail = False
    account = Profile.Profile()
    try:
        a = account.load_profile(namefile)
    except NameError:
        yes = tk.Label(login, text="Please enter a file.", bg='#36393e', fg="#fa777c")
        yes.place(relx=0.5,rely=0.01)
        fail = True
    except Profile.DsuFileError:
        fail = True
        yes = tk.Label(login, text="Invalid file. Please try again", bg='#36393e', fg="#fa777c")
        yes.place(relx=0.5,rely=0.01)
        fail = True
    acc = ds_messenger.DirectMessenger(account.dsuserver, account.username, account.password)
    app.body.del_contacts()
    for i in account.friends:
        app.body.insert_contact(i)
    if account.username == user and account.password == pwd:
        login.destroy()
        ds_messenger.join(account.username, account.password, account.dsuserver)
        try:
            account.token = ds_messenger.token_retrieval()
        except NameError:
            pass
        try:
            if account.messages == []:
                message_list = acc.retrieve_all()
                account.messages = message_list
                account.save_profile(namefile)
            else:
                pass
        except:
            pass
        main.deiconify()
    else:
        if fail == False:
            failure = tk.Label(login, text="Incorrect username and/or password.", bg='#36393e', fg="#fa777c")
            failure.place(relx=0.5,rely=0.01)
        

def creater(window=None):
    if window != None:
        window.destroy()
    else:
        pass
    create = tk.Toplevel(login, bg='#36393e')
    create.title('Registration Page')
    login.withdraw()
    create.deiconify()
    create.geometry('720x480')
    pls = tk.Label(create, text="Create an account", justify='center', 
                    font="Helvetica 14 bold", bg='#36393e', fg='#FFFFFF')

    pls.place(relheight=0.05, relx=0.05, rely=0.01)
    
    
    Dsuserver_name = tk.Entry(create, font="Helvetica 14",bg='#1e2124', fg='#FFFFFF', insertbackground='#FFFFFF')
    label_Dsuserver = tk.Label(create, text="Dsuserver IP: ", font='Helvetica 12', justify="left", bg='#36393e', fg='#FFFFFF')
    label_Dsuserver.place(relheight=0.2, relx=0.1, rely=0.45)
    Dsuserver_name.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.47)
    register_file_label = tk.Label(create, text="Name the file: ", font='Helvetica 12', bg='#36393e', justify="left", fg='#FFFFFF')
    register_file_label.place(relwidth=0.4,relheight=0.12, relx=-0.025, rely=0.30)
    register_file_name = tk.Entry(create, font="Helvetica 14", bg='#1e2124', fg='#FFFFFF', insertbackground='#FFFFFF')
    register_file_name.place(relwidth=0.4,relheight=0.12, relx=0.35, rely=0.30)
    next = tk.Button(create,
                        text="Next",
                        font="Helvetica 14", bg='#7289da', activebackground='#7289da',
                        command=lambda: checker(create, Dsuserver_name.get(), register_file_name.get()))

    next.place(relx=0.8,
                rely=0.82)
    
    back = tk.Button(create,
                        text="Back",
                        font="Helvetica 14", bg='#7289da', activebackground='#7289da',
                        command=lambda: goback(create))

    back.place(relx=0.1,
                rely=0.82)
    

    file_button = tk.Button(master=create, text="Directory", bg='#7289da', width=10, height=2, activebackground='#7289da', command=lambda: acc_directory(create))
    file_button.place(relx=0.10,rely=0.14) 


def checker(create, dsuserver, name):
    fail = False
    try:
        if directory == '':
            yes = tk.Label(create, text="Please enter a  file directory.", bg='#36393e', fg="#fa777c")
            yes.place(relx=0.5,rely=0.01)
    except NameError:
        try:
            yes.destroy()
        except UnboundLocalError:
            pass
        yes = tk.Label(create, text="Please enter a directory.", bg='#36393e', fg="#fa777c")
        yes.place(relx=0.5,rely=0.01)
        fail = True
    if dsuserver == '':
        try:
            yes.destroy()
        except UnboundLocalError:
            pass
        yes = tk.Label(create, text="Please enter a Dsuserver.", bg='#36393e', fg="#fa777c")
        yes.place(relx=0.5,rely=0.01)
        fail = True
    elif name == '':
        try:
            yes.destroy()
        except UnboundLocalError:
            pass
        yes = tk.Label(create, text="Please give the file a name.", bg='#36393e', fg="#fa777c")
        yes.place(relx=0.5,rely=0.01)
        fail = True
    if fail == False:
        creater2(create, name, dsuserver)
    

def creater2(create, name, dsuserver, fail=False):
    create.destroy()
    create = tk.Toplevel(login, bg='#36393e')
    create.title('Registration Page')
    if fail == True:
        yes = tk.Label(create, text="Input error. Please check information.", bg='#36393e', fg="#fa777c")
        yes.place(relx=0.5,rely=0.01)
    login.withdraw()
    create.deiconify()
    create.geometry('720x480')
    pls = tk.Label(create,
                        text="Create an account",
                        justify='center',
                        font="Helvetica 14 bold", bg='#36393e', fg='#FFFFFF')

    pls.place(relheight=0.05,
                    relx=0.05,
                    rely=0.01)
    
    labelName = tk.Label(create,
                            text="Username: ",
                            font="Helvetica 12", fg='#FFFFFF', bg='#36393e')

    labelName.place(relheight=0.2,
                            relx=0.1,
                            rely=0.16)

    # create a entry box for
    # tyoing the message
    register_name = tk.Entry(create, font="Helvetica 14", bg='#1e2124', fg='#FFFFFF')
    register_name.place(relwidth=0.4,relheight=0.12, relx=0.35, rely=0.18)
    register_pwd = tk.Entry(create, font="Helvetica 14", show='*', bg='#1e2124', fg='#FFFFFF', insertbackground='#FFFFFF')
    labelpwd = tk.Label(create, text="Password: ", font='Helvetica 12', justify="left", fg='#FFFFFF', bg='#36393e')
    labelpwd.place(relheight=0.2, relx=0.1, rely=0.35)
    register_pwd.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.37)
    Register = tk.Button(create, text="Register", font="Helvetica 14", bg='#7289da', activebackground='#7289da',
                        command=lambda: [create_check(create, name, dsuserver)])
    Register.place(relx=0.8,
                rely=0.82)
    def create_check(create, name, dsuserver):
        x = create_profile(name, directory, dsuserver, register_name.get(), register_pwd.get())
        if x == False:
            creater2(create, name, dsuserver, fail= True)
        else:
            login_page(create, register=True)
    back = tk.Button(create, text="Back", font="Helvetica 14", bg='#7289da', activebackground='#7289da',
                    command=lambda: creater(create))
    back.place(relx=0.1,
                rely=0.82)


def login_page(window=None, register=None):
    global login
    if window != None:
        window.destroy()
    else:
        pass
    login = tk.Toplevel(main, bg='#36393e')
    login.title("Login Page")
    if register == True:
        success = tk.Label(login, text="Account created!", bg="#36393e", fg='#FFFFFF')
        success.place(relx=0.5,rely=0.01)
    else:
        pass
    file_button = tk.Button(master=login, text="Select File", width=10, height=2, activebackground='#7289da', command=lambda: acc_file(login),bg='#7289da')
    file_button.place(relx=0.10,rely=0.14)
    login.geometry("720x480")
    login.resizable(width=False, height=False)
    login.configure(width=400,height=300)
    pls = tk.Label(login,text="Login Page", justify='center',
                    font="Helvetica 14 bold", bg='#36393e', fg='#FFFFFF')
    pls.place(relheight=0.05, relx=0.05, rely=0.01)
    labelName = tk.Label(login, text="Username: ",
                        font="Helvetica 12", bg='#36393e',fg='#FFFFFF')
    labelName.place(relheight=0.2, relx=0.1, rely=0.28)
    entryName = tk.Entry(login,
                            font="Helvetica 14", bg='#1e2124', fg='#FFFFFF',insertbackground='#FFFFFF')
    

    entryName.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.30)
    
    entrypwd = tk.Entry(login, font="Helvetica 14", show='*', bg='#1e2124', fg='#FFFFFF', insertbackground='#FFFFFF')
    labelpwd = tk.Label(login, text="Password: ", font='Helvetica 12',bg='#36393e', fg='#FFFFFF')
    labelpwd.place(relheight=0.2,
                            relx=0.1,
                            rely=0.48)
    entrypwd.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.50)
    new_user = tk.Label(login, text="New user? Create an account: ", font='Helvetica 12', bg='#36393e', fg='#FFFFFF')
    new_user.place(relwidth=0.4, relheight=0.12, relx = 0.05, rely=0.65)
    new_user_button = tk.Button(login, text="Register", bg='#7289da', activebackground='#7289da', command=lambda: creater())
    new_user_button.place(relx=0.43,rely=0.68)
    entryName.focus()
    go = tk.Button(login,text="Login",font="Helvetica 14", bg='#7289da', activebackground='#7289da',
                    command=lambda: acc_login(entryName.get(), entrypwd.get()))
    go.place(relx=0.4,rely=0.80)
    

def goback(create):
    create.destroy()
    login_page()


def bubble_sort():
    n = len(account.messages)
    swapped = False
    for i in range(n-1):
        for j in range(n-1):
            if account.messages[j]['timestamp'] > account.messages[j+1]['timestamp']:
                swapped = True
                account.messages[j]['timestamp'], account.messages[j+1]['timestamp'] = account.messages[j+1]['timestamp'], account.messages[j]['timestamp']
        if not swapped:
            return
                    

if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()
    app = MainApp(main)
    main.withdraw()
    login_page()
    # 'title' assigns a text value to the Title Bar area of a window.
    main.title()
    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")
    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)
    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id = main.after(2000, app.previous_messages)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()


