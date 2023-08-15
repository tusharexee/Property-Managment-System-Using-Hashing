from tkinter import *
from customtkinter import *
from functools import partial
import tkinter.font
import datetime
import tkinter.messagebox
from datetime import timedelta
import os
import hashlib
import binascii

ox,oy=0,0

loc_table={
	"JP Nagar, Bangaluru":0,
	"Rajajinagar, Bangaluru":1,
	"Sadashivnagar, Mysore":2,
	"HSR Layout, Bangaluru":3,
	"MG Road, Bangaluru":4,
	"Nandani Layout, Bangaluru":5,
	"Basaveshwaranagar, Bangaluru":6,
	"Kormangala, Bangaluru":7,
	"Ng Road, Chennai":8,
	"TR Puram, Chennai":9,
	"MG Road, Delhi":10,
	"Tr Puram, Chennai":11
}

def login_in():
	global id_input_login
	global password_input_login
	global login_menu

	login_menu=CTk()
	login_menu.title("Login")
	login_menu.resizable(False,False)
	login_menu.geometry("720x541")
	bg=PhotoImage(file="back.png",height=541,width=720,master=login_menu)
	bgl=Label(login_menu,image=bg)
	bgl.place(x=0,y=0)

	frame=CTkFrame(login_menu)

	orionLabel=CTkLabel(frame,text="PROPERTY MANAGMENT SYSTEM WITH HASHING",font=("Times New Roman Bold",15))
	subLabel=CTkLabel(frame, text="Anish Kumar, Piyush Singh and Tushar Prakash",font=("Times New Roman Bold",15))
	id_label=CTkLabel(frame,text="Enter ID")
	password_label=CTkLabel(frame,text="Enter Password")
	id_input_login=CTkEntry(frame)
	password_input_login=CTkEntry(frame,show="*")
	loginbutton1=CTkButton(frame,command=login_check,text="Login")
	registerbutton=CTkButton(frame,command=register_in,text="Register")
	adminbutton=CTkButton(frame,command=admin_in,text="Admin Login")

	orionLabel.grid(row=0, column=0,columnspan=2)
	subLabel.grid(row=1, column=0,columnspan=2)
	id_label.grid(row=2,column=0,pady=15)
	id_input_login.grid(row=2,column=1,pady=15)
	password_label.grid(row=3,column=0,pady=15)
	password_input_login.grid(row=3,column=1,pady=15)
	loginbutton1.grid(row=4,column=0,pady=15)
	registerbutton.grid(row=4,column=1,pady=15)
	adminbutton.grid(row=5,column=0,pady=15)

	frame.place(x=200,y=100)
	login_menu.mainloop()

def login_check():
	global id
	id=id_input_login.get()
	password=password_input_login.get()

	pos = binary_search('index.txt', id)
	if pos == -1:
		tkinter.messagebox.showinfo("Login","Incorrect Username")
		return(login_in)
	else:
		f2 = open ('Userprofile.txt', 'r')
		f2.seek(int(pos))
		l = f2.readline()
		l = l.rstrip()
		word = l.split('|')
		if(verify_password(word[1], password)):
			f2.close()
			tkinter.messagebox.showinfo("Login","Login Successful")
			login_menu.destroy()
			Main_Menu()
		else:
			f2.close()
			tkinter.messagebox.showinfo("Login","Incorrect Password")
			return(login_in)

def register_in():
	global id_input
	global name_input
	global email_input
	global password_input
	global register_menu

	register_menu=CTk()
	register_menu.title("Register")
	register_menu.resizable(False,False)
	register_menu.geometry("720x541")
	bg=PhotoImage(file="back.png",height=541,width=720,master=register_menu)
	bgl=Label(register_menu,image=bg)
	bgl.place(x=0,y=0)

	frame=CTkFrame(register_menu)

	id_label=CTkLabel(frame,text="ID")
	name_label=CTkLabel(frame,text="Full Name")
	email_label=CTkLabel(frame,text="Email")
	password_label=CTkLabel(frame,text="Password")
	login_label=CTkLabel(frame,text="Already have an account?")
	id_input=CTkEntry(frame)
	name_input=CTkEntry(frame)
	email_input=CTkEntry(frame)
	password_input=CTkEntry(frame,show="*")
	loginbutton1=CTkButton(frame,command=login_in,text="Login")
	registerbutton=CTkButton(frame,command=register_check,text="Register")

	id_label.grid(row=3, column = 4, pady = (10,10),padx=(10, 10))
	id_input.grid(row=3,column=5, sticky=E)
	name_label.grid(row=4, column = 4, pady = (10,10),padx=(10, 10))
	name_input.grid(row=4, column = 5, sticky=E)
	email_label.grid(row=5, column = 4, pady = (10,10),padx=(10, 10))
	email_input.grid(row=5,column=5, sticky=E)
	password_label.grid(row=6, column = 4, pady = (10,10),padx=(10, 10))
	password_input.grid(row=6,column=5, sticky=E)
	login_label.grid(row=8, column = 4, pady = (10,10),padx=(10, 10))
	registerbutton.grid(row =7, column = 5, pady = (10,10),padx=(10, 10))
	loginbutton1.grid(row =8, column = 5, pady = (10,10),padx=(10, 10))

	frame.place(x=170,y=100)
	register_menu.mainloop()

def register_check():
	global id

	id=id_input.get()
	name=name_input.get()
	email=email_input.get()
	password=password_input.get()

	if len(id)==0 or len(name) == 0 or len(email) == 0 or len(password) == 0:
		tkinter.messagebox.showinfo("Register","Blank Field not Allowed")
		register_menu.lift()
		return(register_in)

	pos = binary_search('index.txt', id)
	if pos != -1:
		tkinter.messagebox.showinfo("Register","Already registered. Choose a different ID")
		register_menu.destroy()

	f2 = open ('Userprofile.txt', 'a')
	pos = f2.tell()
	f3 = open ('index.txt', 'a')
	buf = id + '|' + hash_password(password) + '|' + name + '|' + email + '|' + '$'
	f2.write(buf)
	f2.write('\n')
	buf = id + '|' + str(pos) + '|' + '$'
	f3.write(buf)
	f3.write('\n')
	f3.close()
	f2.close()
	key_sort('index.txt')
	tkinter.messagebox.showinfo("Register","Registration Successful")
	register_menu.destroy()


def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def admin_in():
	global id_admin
	global password_admin
	global admin_menu

	admin_menu=CTk()
	admin_menu.title("Admin")
	admin_menu.resizable(False,False)
	admin_menu.geometry("720x541")
	bg=PhotoImage(file="back.png",height=541,width=720,master=admin_menu)
	bgl=Label(admin_menu,image=bg)
	bgl.place(x=0,y=0)

	frame=CTkFrame(admin_menu)

	admin_label=CTkLabel(frame,text="Admin ID")
	admin_password_label=CTkLabel(frame,text="Password")
	id_admin=CTkEntry(frame)
	password_admin=CTkEntry(frame,show="*")
	loginbutton2=CTkButton(frame,command=admin_check,text="Login")

	admin_label.grid(row=0,column=0,pady=15)
	id_admin.grid(row=0,column=1,pady=15)
	admin_password_label.grid(row=1,column=0,pady=15)
	password_admin.grid(row=1,column=1,pady=15)
	loginbutton2.grid(row=2,column=0,columnspan=2,pady=15)

	frame.place(x=240,y=150)
	admin_menu.mainloop()

def admin_check():
	global admin_id

	admin_id=id_admin.get()
	admin_password=password_admin.get()

	if admin_id=="admin" and admin_password=="admin":
		tkinter.messagebox.showinfo("Login","Admin Login Successful")
		admin_menu.destroy()
		login_menu.destroy()
		Admin_Opt()
	else:
		tkinter.messagebox.showinfo("Login","Admin id or password INCORRECT. Please reenter")

def Admin_Opt():
	global opt_menu

	opt_menu=CTk()
	opt_menu.title("Admin_menu")
	opt_menu.resizable(False,False)
	opt_menu.geometry("720x541")
	bg=PhotoImage(file="back.png",height=541,width=720,master=opt_menu)
	bgl=Label(opt_menu,image=bg)
	bgl.place(x=0,y=0)

	frame=CTkFrame(opt_menu)

	addbutton=CTkButton(frame,command=add_book,text="Add property")
	delbutton=CTkButton(frame,command=del_book,text="Remove property")
	backbutton=CTkButton(frame,command=reopen_login,text="Log out")

	addbutton.grid(row=0,column=0,padx=10,pady=10)
	delbutton.grid(row=0,column=1,padx=10,pady=10)
	backbutton.grid(row=0,column=2,padx=10,pady=10)

	frame.place(x=120,y=200)
	opt_menu.mainloop()

def reopen_login():
	tkinter.messagebox.showinfo("Login","Admin Logout Successful!")
	opt_menu.destroy()

	f7=open('Bindex.txt','r')
	lines1=f7.readlines()
	f7.close()
	f8=open('Bindex.txt','w')
	for line1 in lines1:
		if line1.startswith('*'):
			continue
		else:
			f8.write(line1)
	f8.close()

	login_in()


def key_sort(fname):
	t=list()
	fin=open(fname,'r')
	for line in fin:
		line=line.rstrip('\n')
		words=line.split('|')
		if(fname=="Bindex.txt"):
			t.append((words[0],words[1],words[2]))
		else:
			t.append((words[0],words[1]))
	fin.close()
	t.sort()
	with open("temp.txt",'w') as fout:
		if(fname=="Bindex.txt"):
			for pkey,addr,addrec in t:
				pack=pkey+"|"+addr+"|"+addrec+"|$"
				fout.write(pack+'\n')
		else:
			for pkey,addr in t:
				pack=pkey+"|"+addr+"|$"
				fout.write(pack+'\n')
	os.remove(fname)
	os.rename("temp.txt",fname)


def binary_search(fname, search_key):
	t = []
	fin = open(fname,'r')
	for lx in fin:
		lx = lx.rstrip()
		wx = lx.split('|')
		if(fname=="Bindex.txt"):
			t.append((wx[0],wx[1],wx[2]))
		else:
			t.append((wx[0],wx[1]))
	fin.close()
	l = 0
	r = len(t) - 1
	while l <= r:
		mid = (l + r)//2
		if t[mid][0] == search_key:
			return (int(t[mid][1]),int(t[mid][2])) if(fname=="Bindex.txt") else int(t[mid][1])
		elif t[mid][0] <= search_key:
			l = mid + 1
		else:
			r = mid - 1
	return (-1,-1) if(fname=="Bindex.txt") else -1


def add_book():
	global book_id
	global book_name
	global author_name
	global add_menu

	add_menu=CTk()
	add_menu.title("Add")
	add_menu.resizable(False,False)
	add_menu.geometry("720x541")
	bg=PhotoImage(file="back.png",height=541,width=720,master=add_menu)
	bgl=Label(add_menu,image=bg)
	bgl.place(x=0,y=0)

	frame=CTkFrame(add_menu)

	book_id_label=CTkLabel(frame,text="Property ID")
	book_label=CTkLabel(frame,text="Property Name")
	author_label=CTkLabel(frame,text="Location")
	book_id=CTkEntry(frame)
	book_name=CTkEntry(frame)
	author_name=CTkOptionMenu(frame,values=list(loc_table.keys()))
	addbutton1=CTkButton(frame,command=add_check,text="Add property")

	book_id_label.grid(row=0,column=0,padx=10,pady=10)
	book_id.grid(row=0,column=1,padx=10,pady=10)
	book_label.grid(row=1,column=0,padx=10,pady=10)
	book_name.grid(row=1,column=1,padx=10,pady=10)
	author_label.grid(row=2,column=0,padx=10,pady=10)
	author_name.grid(row=2,column=1,padx=10,pady=10)
	addbutton1.grid(row=3,column=0,columnspan=2,padx=10,pady=10)

	frame.place(x=200,y=150)
	add_menu.mainloop()

def add_check():
	global b_id
	b_id=book_id.get()
	b_name=book_name.get().upper()
	a_id=author_name.get()

	if len(b_name)==0:
		tkinter.messagebox.showinfo("Add Property","You did not type a property name O_O")
		add_menu.lift()
		return(add_book)

	if len(b_id)!=5 or b_id.isdigit()==False:
		tkinter.messagebox.showinfo("Add property","Please renter the details(ID should be 5 positive integers)")
		add_menu.lift()
		return(add_book)

	if len(a_id) == 0:
		a_id = "Unknown"

	pos = binary_search('Bindex.txt', b_id)
	if pos[0] != -1:
		tkinter.messagebox.showinfo("Add","Property already present.")
		add_menu.lift()
		return(add_book)

	f22 = open('BData.txt','r')
	property_data=f22.readlines()
	f22.close()
	pos=loc_table[a_id]
	records=property_data[pos].strip('\n').strip("$").split("||")
	
	for i in range(len(records)):
		rec=records[i]
		pid,pname,pavailability=rec.split('|')
		if(pid.strip()=='/' or pid.strip()=='#'):
			if(len(b_name)>=20):
				records[i]=b_id+'|'+b_name[:20]+"|Y"
			else:
				records[i]=b_id+'|'+b_name+(' '*(20-len(b_name)))+"|Y"
			pos_in_record=i
			break
	else:
		tkinter.messagebox.showinfo("Add","Location already has 3 Property")
		add_menu.lift()
		return(add_book)

	property_data[pos]="||".join(records)+"$$\n"
	

	f22 = open('BData.txt','w')
	f22.writelines(property_data)
	f22.close()

	f33 = open ('Bindex.txt', 'a')
	buf = b_id + '|' + str(pos) + '|' + str(pos_in_record)+'|$'
	f33.write(buf)
	f33.write('\n')
	f33.close()

	key_sort('Bindex.txt')
	tkinter.messagebox.showinfo("Add","Property added Successfully")
	add_menu.destroy()


def del_book():
	global rb_id
	global del_menu

	del_menu=CTk()
	del_menu.title("Delete")
	del_menu.resizable(False,False)

	Id=[]
	Title = []
	Author = []
	Availability = []

	f1 = open('Bindex.txt', 'r')
	f = open ("BData.txt", 'r')
	norecord = 0

	loc_records=f.readlines()
	f.close()
	for line in f1:
		if not line.startswith('*'):
			norecord += 1
			line = line.rstrip('\n')
			word = line.split('|')

			loc_record=loc_records[int(word[1])].strip('\n').strip("$").split("||")
			record=loc_record[int(word[2])].split('|')

			Id.append(record[0])
			Title.append(record[1])
			Author.append(list(loc_table.keys())[int(word[1])])
			Availability.append(record[2])
	f1.close()

	borrow_list=Listbox(del_menu)
	borrow_list2=Listbox(del_menu)
	borrow_list3=Listbox(del_menu)
	borrow_list4=Listbox(del_menu)

	for num in range(0,norecord):
		borrow_list.insert(0,Id[num])
		borrow_list2.insert(0,Title[num])
		borrow_list3.insert(0,Author[num])
		borrow_list4.insert(0,Availability[num])


	b_label=CTkLabel(del_menu,text="Property ID")
	rb_id=CTkEntry(del_menu)
	delbutton1=CTkButton(del_menu,command=del_check,text="Remove property")
	borrow_label=CTkLabel(del_menu,text="Id")
	borrow_label2=CTkLabel(del_menu,text="Name")
	borrow_label3=CTkLabel(del_menu,text="Location")
	borrow_label4=CTkLabel(del_menu,text="Availability")

	borrow_label.grid(row=1,column=0)
	borrow_label2.grid(row=1,column=1)
	borrow_label3.grid(row=1,column=2)
	borrow_label4.grid(row=1,column=3)

	borrow_list.grid(row=2,column=0)
	borrow_list2.grid(row=2,column=1)
	borrow_list3.grid(row=2,column=2)
	borrow_list4.grid(row=2,column=3)
	b_label.grid(row=0,column=0)
	rb_id.grid(row=0,column=1)
	delbutton1.grid(row=0,column=2)

	del_menu.mainloop()

def del_check():

	global del_id
	del_id=rb_id.get()

	if len(del_id)==0:
		tkinter.messagebox.showinfo("Delete Property","You did not type anything O_O")
		del_menu.lift()
		return(del_book)

	pos = binary_search('Bindex.txt', del_id)
	if(pos[0] == -1):
		tkinter.messagebox.showinfo("Delete","Property not present. Please reenter")
		del_menu.destroy()
		return(del_book)
	else:
		f = open ('BData.txt', 'r')
		l1 = f.readlines()[pos[0]]
		w1 = l1.strip('\n').strip('$').split('||')[pos[1]].split('|')
		f.close()
		if(w1[2] == 'N'):
			tkinter.messagebox.showinfo("Delete","property currently borrowed. Please try another property")
			del_menu.destroy()
			return(del_book)

	bi=open('Bindex.txt','r')
	rl=bi.readlines()
	for i in range(len(rl)):
		if(rl[i].strip('\n').strip('$').split('|')[0]==del_id):
			del(rl[i])
			break
	bi.close()

	bi=open('Bindex.txt','w')
	bi.writelines(rl)
	bi.close()

	bi=open('BData.txt','r')
	rl=bi.readlines()
	records=rl[int(pos[0])].strip('\n').strip('$').split('||')
	records[int(pos[1])]="#    |#                   |#"
	rl[int(pos[0])]="||".join(records)+"$$\n"
	bi.close()

	bi=open('BData.txt','w')
	bi.writelines(rl)
	bi.close()

	tkinter.messagebox.showinfo("Delete","Property Successfully removed")
	del_menu.destroy()


def Main_Menu():
	base = CTk()
	#Window title and size optimization
	base.title("Main Menu")
	base.resizable(False,False)
	base.geometry("720x541")
	bg=PhotoImage(file="back.png",height=541,width=720,master=base)
	bgl=Label(base,image=bg)
	bgl.place(x=0,y=0)
	
	frame=CTkFrame(base)

	current_time1=datetime.datetime.now()
	current_time=str(current_time1.strftime("%c"))

	#Bunch of labels
	status = CTkLabel(frame,text=("Last Login: " + current_time))
	orionLabel=CTkLabel(frame, text="PROPERTY MANAGMENT SYSTEM",font=("Arial",15))
	welcomeLabel=CTkLabel(frame,text=("Welcome "+id))
	orionLabel.grid(row=0, column=0,columnspan=4,pady=15)
	welcomeLabel.grid(row=1,column=0,pady=15)
	status.grid(row=1,column=2,columnspan=2,pady=15)

	#Buttons
	borrow_but=CTkButton(frame,text="Buy Property",command=borrow_in)
	return_but=CTkButton(frame,text="Return Property",command=return_in)
	search_but=CTkButton(frame,text="Search Property",command=search_in)

	borrow_but.grid(row=2,column=0,padx=10,pady=15)
	return_but.grid(row=2,column=2,padx=10,pady=15)
	search_but.grid(row=2,column=3,padx=10,pady=15)

	frame.place(x=120,y=180)
	base.mainloop()


def borrow_in():
	global borrow_entry1
	global borrow_menu

	borrow_menu=CTk()
	borrow_menu.title("Borrow")
	borrow_menu.resizable(False,False)

	Id=[]
	Title = []
	Author = []
	Availability = []

	f1 = open('Bindex.txt', 'r')
	f = open ("BData.txt", 'r')
	norecord = 0

	loc_records=f.readlines()
	f.close()
	for line in f1:
		if not line.startswith('*'):
			norecord += 1
			line = line.rstrip('\n')
			word = line.split('|')

			loc_record=loc_records[int(word[1])].strip('\n').strip("$").split("||")
			record=loc_record[int(word[2])].split('|')

			Id.append(record[0])
			Title.append(record[1])
			Author.append(list(loc_table.keys())[int(word[1])])
			Availability.append(record[2])
	f1.close()

	borrow_list=Listbox(borrow_menu,height=50,width=20)
	borrow_list1=Listbox(borrow_menu,height=50,width=50)
	borrow_list2=Listbox(borrow_menu,height=50,width=50)
	borrow_list3=Listbox(borrow_menu,height=50,width=20)

	for num in range(0,norecord):
		borrow_list.insert(0,Id[num])
		borrow_list1.insert(0,Title[num])
		borrow_list2.insert(0,Author[num])
		borrow_list3.insert(0,Availability[num])

	borrow_label1=CTkLabel(borrow_menu,text="Enter the Property ID that you wish to borrow",font=("Arial",15))
	borrow_label=CTkLabel(borrow_menu,text="Id")
	borrow_label2=CTkLabel(borrow_menu,text="Name")
	borrow_label3=CTkLabel(borrow_menu,text="Location")
	borrow_label4=CTkLabel(borrow_menu,text="Availability")

	borrow_entry1=CTkEntry(borrow_menu)
	borrow_button1=CTkButton(borrow_menu,text="Buy",command=borrow_check)

	borrow_label1.grid(row=0,column=0,columnspan=4)
	borrow_label.grid(row=3,column=0)
	borrow_label2.grid(row=3,column=1)
	borrow_label3.grid(row=3,column=2)
	borrow_label4.grid(row=3,column=3)

	borrow_entry1.grid(row=1,column=1)
	borrow_button1.grid(row=1,column=2)
	borrow_list.grid(row=4,column=0)
	borrow_list1.grid(row=4,column=1)
	borrow_list2.grid(row=4,column=2)
	borrow_list3.grid(row=4,column=3)
	borrow_menu.mainloop()

def borrow_check():
	count = 0
	f = open('Record.txt', 'r')
	for l in f:
		l = l.split('|')
		if l[0] ==  id:
			count += 1
	if count >= 3:
		tkinter.messagebox.showinfo("Borrow", "Cannot have more than 3 property")
		borrow_menu.destroy()
	else:
		date = datetime.date.today()
		enddate = date + timedelta(days = 7)
		bbook=borrow_entry1.get().upper()

		if len(bbook) == 0:
			tkinter.messagebox.showinfo("Borrow","You did not type anything O_O")
			borrow_menu.lift()
			return(borrow_in)

		pos = binary_search('Bindex.txt', bbook)
		if pos[0] == -1:
			tkinter.messagebox.showinfo("Borrow","The property that you entered is not in our database, please enter a different property")
			borrow_menu.lift()
		else:
			f2 = open('BData.txt', 'r')
			rl = f2.readlines()
			l2 = rl[int(pos[0])].strip('\n').strip('$').split('||')
			w2 = l2[int(pos[1])].split('|')
			f2.close()
			if(w2[2] == 'Y'):
				w2[2]='N'
				l2[int(pos[1])]="|".join(w2)
				rl[int(pos[0])] = "||".join(l2)+"$$\n"
				f2=open("BData.txt",'w')
				f2.writelines(rl)
				f2.close()
				tkinter.messagebox.showinfo("Borrow","The property you have selected has been successfully borrowed. Please return it by:" +'\n'+ str(enddate) )

				buf = id + '|' + bbook + '|' + w2[1] + '|$\n'
				f3 = open('Record.txt', 'a')
				f3.write(buf)
				f3.close()
				key_sort('Record.txt')
				Done2=tkinter.messagebox.askyesno("Borrow","Do you want to borrow another property?")
				if Done2==True:
					borrow_menu.destroy()
					borrow_in()
				else:
					borrow_menu.destroy()
			else:
				tkinter.messagebox.showinfo("Borrow","This property is currently unavailable, please select another property")
				borrow_menu.lift()


def return_in():
	global return_entry1
	global return_menu
	global record_verification

	return_menu=CTk()
	return_menu.wm_title("Return")
	return_menu.resizable(False,False)

	Id=[]
	Name = []
	Location = []
	Availability = []
	record_verification = []

	f1 = open('Bindex.txt', 'r')
	f = open ("BData.txt", 'r')
	norecord = 0

	loc_records=f.readlines()
	f.close()
	for line in f1:
		norecord += 1
		line = line.rstrip('\n')
		word = line.split('|')

		loc_record=loc_records[int(word[1])].strip('\n').strip("$").split("||")
		record=loc_record[int(word[2])].split('|')

		if(record[2]=='N'):
			file=open("Record.txt","r")
			for f in file.readlines():
				r=f.strip('\n').strip('$').split("|")
				if(r[0]==id and r[1]==record[0]):
					Id.append(record[0])
					Name.append(record[1])
					Location.append(list(loc_table.keys())[int(word[1])])
					Availability.append(record[2])
					record_verification.append(record[0])
			file.close()
	f1.close()

	return_list=Listbox(return_menu)
	return_list1=Listbox(return_menu)
	return_list2=Listbox(return_menu)
	return_list3=Listbox(return_menu)

	for num in range(0,len(Id)):
		return_list.insert(0,Id[num])
		return_list1.insert(0,Name[num])
		return_list2.insert(0,Location[num])
		return_list3.insert(0,Availability[num])

	return_label=CTkLabel(return_menu,text="Id")
	return_label2=CTkLabel(return_menu,text="Name")
	return_label3=CTkLabel(return_menu,text="Location")
	return_label4=CTkLabel(return_menu,text="Availability")

	return_button1=CTkButton(return_menu,text="Return",command=return_check)
	return_entry1=CTkEntry(return_menu)
	return_label1=CTkLabel(return_menu,text="Please enter the property ID that you wish to return",font=("Arial",15))

	return_label1.grid(row=0,column=0,columnspan=4)
	return_entry1.grid(row=1,column=1)
	return_button1.grid(row=1,column=2)

	return_label.grid(row=3,column=0)
	return_label2.grid(row=3,column=1)
	return_label3.grid(row=3,column=2)
	return_label4.grid(row=3,column=3)

	return_list.grid(row=4,column=0)
	return_list1.grid(row=4,column=1)
	return_list2.grid(row=4,column=2)
	return_list3.grid(row=4,column=3)

	return_menu.mainloop()


def return_check():
	import datetime as dt
	from datetime import timedelta
	date = dt.date.today()
	bbook = return_entry1.get().upper()

	if len(bbook) == 0:
		tkinter.messagebox.showinfo("Return","You did not enter anything O_O")
		return_menu.lift()
		return(return_in)

	if(bbook in record_verification):
		pos = binary_search('Bindex.txt', bbook)
		if pos[0] != -1:
			f2 = open('BData.txt', 'r')
			rl = f2.readlines()
			l2 = rl[int(pos[0])].strip('\n').strip('$').split('||')
			w2 = l2[int(pos[1])].split('|')
			f2.close()
			if(w2[2] == 'N'):
				tkinter.messagebox.showinfo("Return","The property you have selected has been successfully returned on"+'\n'+str(date))
				
				w2[2]='Y'
				l2[int(pos[1])]="|".join(w2)
				rl[int(pos[0])] = "||".join(l2)+"$$\n"
				f2=open("BData.txt",'w')
				f2.writelines(rl)
				f2.close()

				f2=open('Record.txt','r')
				lines=f2.readlines()
				f2.close()
				f3=open('Record.txt','w')
				for l2 in lines:
					l3=l2.split('|')
					if l3[1] == bbook and l3[0] == id:
						continue
					else:
						f3.write(l2)
				f3.close()
				Done3=tkinter.messagebox.askyesno("Return","Do you want to return another property?")
				if Done3==True:
					return_menu.destroy()
					return_in()
				else:
					return_menu.destroy()
			else:
				tkinter.messagebox.showinfo("This property has been returned, please select another property")
	else:
		tkinter.messagebox.showinfo("Return","The property that you had entered is invalid. Please reenter a different property")
		return_menu.lift()


def search_in():
	global search_entry
	global search_menu
	search_menu=CTk()

	search_menu.title("Search")
	search_menu.resizable(False,False)

	search_label1=CTkLabel(search_menu,text="Search through our database to check if your desired property is available",font=("Arial",15))

	search_entry = CTkEntry(search_menu)

	search_button=CTkButton(search_menu,text="Search",command=search_check)
	
	search_label1.grid(row=0,column=0,columnspan=4,pady=15)
	search_entry.grid(row=1,column=1,pady=15)
	search_button.grid(row=1,column=2,pady=15)

	search_menu.mainloop()


def search_check():
	search_word=search_entry.get().upper()
	search_menu.destroy()

	if len(search_word) == 0:
		tkinter.messagebox.showinfo("Search","You did not type anything O_O")
		return(search_in)

	pos = binary_search('Bindex.txt', search_word)

	if (pos[0] == -1):
		tkinter.messagebox.showinfo("Search","This property does not exist in our database")
	else:
		search_menu2=CTk()
		search_menu2.resizable(False,False)
		search_menu2.title("Search")
		search_menu2.attributes("-topmost",True)
		tkinter.messagebox.showinfo("Search","Property Found")

		search_result=Listbox(search_menu2)
		f2 = open('BData.txt', 'r')
		
		l1 = f2.readlines()[int(pos[0])].strip('\n').strip('$')
		w1 = l1.split('||')[int(pos[1])]
		b_id = w1.split('|')[0]
		name = w1.split('|')[1]
		location = list(loc_table.keys())[int(pos[0])]
		if(w1.split('|')[2] == "Y"):
			availability = 'Available'
		else:
			availability = 'Unavailable'
		f2.close()

		search_result.insert(1,"ID:" + b_id)
		search_result.insert(2,"Name:" + name)
		search_result.insert(3,"Location:" + location)
		search_result.insert(4,"Availability:" + availability)

		search_result.pack()
		search_menu2.mainloop()

login_in()
