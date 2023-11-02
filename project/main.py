import tkinter as tk
from tkinter import ttk
import sqlite3

class Main(tk.Frame):
    def __init__ (self,root):
        super().__init__(root)
        self.db = db
        self.init_main()
        self.view_records()
    #метод иницилизации виджетов
    def init_main(self):
        #toolbar
        toolbar = tk.Frame(bg = '#d7d7d7', bd = 2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        #button_add
        self.add_img = tk.PhotoImage(file='./img/add.png')
        bth_add = tk.Button(toolbar, image= self.add_img,bg = '#d7d7d7', bd = 0, command = self.open_child)
        bth_add.pack(side = tk.LEFT) 
        #button_change
        #toolbar
        toolbar = tk.Frame(bg = '#d7d7d7', bd = 2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        #button_upd
        self.upd_img = tk.PhotoImage(file='./img/change.png')
        bth_upd = tk.Button(toolbar, image= self.upd_img,bg = '#d7d7d7', bd = 0, command = self.open_update)
        bth_upd.pack(side = tk.LEFT) 
#button_del
        toolbar = tk.Frame(bg = '#d7d7d7', bd = 2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        #button_del
        self.del_img = tk.PhotoImage(file='./img/del.png')
        bth_del = tk.Button(toolbar, image= self.del_img,bg = '#d7d7d7', bd = 0, command = self.del_records)
        bth_del.pack(side = tk.LEFT) 

        #таблица для вывода контактов
        self.tree = ttk.Treeview(self,columns=('ID', 'name','PHONE', 'EMAIL'), show='headings')
        self.tree.column('ID', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('PHONE', width=150, anchor=tk.CENTER)
        self.tree.column('EMAIL', width=150, anchor=tk.CENTER)
        #задать названия
        self.tree.heading('ID',text='ID')
        self.tree.heading('name',text='name')
        self.tree.heading('PHONE',text='phone')
        self.tree.heading('EMAIL',text='email')

        self.tree.pack()



#метод добавления в БД
    def record(self,name,phone,email):
        self.db.insert_data(name,phone,email)
        self.view_records()


#метод редактирования
    def upd_record(self,name,phone,email):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''
            UPDATE user SET name = ?, phone = ?, email = ?
            WHERE id= ?
                    ''',(name,phone,email,id))
        self.db.conn.commit()
        self.view_records()


# метод удаления
    def del_records(self):
        for i in self.tree.selection():
            self.db.cur.execute('DELETE FROM user WHERE id = ?',
                                self.tree.set(i, '#1'))
        self.db.conn.commit()
        self.view_records()

#перезаполнение таблицы
    def view_records(self):
        for i in self.tree.get_children():
              self.tree.delete(i)
        self.db.cur.execute('SELECT * FROM user')
        r = self.db.cur.fetchall()  
        for i  in r:
            self.tree.insert('', 'end', values = i)            


    #метод открытия окна добавления 
    def open_child(self):
        Child()

    #метод открытия окна редоктирования
    def open_update(self):
         Update()

    

#класс дочерних окон
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_child()
#метод для вызывания виджетов дочерних окон
    def init_child(self):
            self.title('add_contact')
            self.geometry('400x200')
            self.resizable(False,False)
            self.grab_set()
            self.focus_set()
            label_name = tk.Label(self, text = 'name')
            label_phone = tk.Label(self, text='number')
            label_email = tk.Label(self, text='email')

            label_name.place(x = 50, y = 50)
            label_phone.place(x = 50, y = 80)
            label_email.place(x = 50, y = 130)

            self.entry_name = tk.Entry(self)
            self.entry_phone = tk.Entry(self)
            self.entry_email = tk.Entry(self)
            self.entry_name.place(x = 250,y = 50)
            self.entry_phone.place(x = 250,y = 80)
            self.entry_email.place(x = 250,y = 130)

            bth_close = tk.Button(self, text='close', command=self.destroy)
            bth_close.place(x = 250, y = 160)
            self.bth_ok = tk.Button(self, text= 'add')
            self.bth_ok.bind('<Button-1>', lambda ev: self.view.record(self.entry_name.get(), 
                                                                  self.entry_phone.get(), 
                                                                  self.entry_email.get()))
            self.bth_ok.place(x = 350 , y = 160)


#редактирование
class Update(Child):
    def __init__(self):
          super().__init__()
          self.init_update()
          self.db = db
          self.default_data()
    def init_update(self):
        self.title('редактирование контакта')
        self.bth_ok.destroy()
        self.bth_upd = tk.Button(self, text= 'change')
        self.bth_upd.bind('<Button-1>', lambda ev: self.view.upd_record(self.entry_name.get(), 
                                                                  self.entry_phone.get(), 
                                                                  self.entry_email.get()))
        self.bth_upd.bind('<Button-1>', lambda ev: self.destroy(),add ='+')
        self.bth_upd.place(x = 320 , y = 160)


    def default_data(self):  
         id = self.view.tree.set(self.view.tree.selection()[0], '#1')
         self.db.cur.execute('SELECT * FROM user WHERE id = ?', id)
         row = self.db.cur.fetchone()
         self.entry_name.insert(0, row[1])
         self.entry_phone.insert(0, row[2])
         self.entry_email.insert(0, row[3])
         
#class db
class Db:
     #СОЗДАНИЕ СОЕДИНЕНИЙ И КУРСОРА И ТАБЛИЦЫ
    def __init__(self):
          self.conn = sqlite3.connect('employee.db')
          self.cur = self.conn.cursor()
          self.cur.execute('''
                CREATE TABLE IF NOT EXISTS user(
                           id INTEGER PRIMARY KEY,
                           name TEXT,
                           phone TEXT,
                           email TEXT
                )''')
    def insert_data(self, name, phone,email):
        self.cur.execute('''
            INSERT INTO user(name, phone, email)
            VALUES (?,?,?)
''', (name, phone, email))
        self.conn.commit()





if __name__ == '__main__':
    root = tk.Tk()
    root.title('employee_note')
    root.geometry('665x450')
    root.resizable(False,False)
    db = Db()
    app = Main(root)
    app.pack()

    root.mainloop()