import tkinter as tk
import tkinter.filedialog as fd
import tkinter.scrolledtext as st
import datetime
from operator import itemgetter

def btn1Click():
    
    global file
    txtbox4.delete('1.0', 'end')
    fTyp = [('CSVファイル','.csv')]
    iDir = './'
    file = fd.askopenfilename(filetypes = fTyp, initialdir = iDir)
    
def btn2Click():
    
    t1 = txtbox1.get()
    t1 = datetime.datetime.strptime(t1,'%Y/%m/%d')
    t2 = txtbox2.get()
    t2 = datetime.datetime.strptime(t2,'%Y/%m/%d')
    txtbox4.delete('1.0', 'end')

    stu = [['' for i in range(3)] for j in range(10000)]
    i = 0
        
    while i <=9999:
        stu[i][2] = datetime.timedelta()
        i = i + 1

    i = 0
        
    fp = open(file, 'rt')
    csvrow = -1
        
    for deta in fp:
        
        if csvrow != -1:
            csvdeta = deta.split(',')
            name = csvdeta[0]
            event = csvdeta[1]
            time = datetime.datetime.strptime(csvdeta[2],'%Y/%m/%d %H:%M\n')
                
            if time >= t1 and time <= t2 + datetime.timedelta(hours = 24): #期間t1 0:00～t2 24:00
                stu[i][0] = name
                stu[i][1] = event
                stu[i][2] = time
                i = i + 1
                       
        csvrow = csvrow + 1
            
    fp.close()

    i_last = i - 1
    stu = sorted(stu, reverse=True, key=lambda x: x[0])
    stu_list = [['' for k in range(3)] for l in range(10000)]
    k = 0
        
    while k <=9999:
        stu_list[k][1] = datetime.timedelta()
        k = k + 1

    k = 0
    i = 0
    stu_list[0][0] = stu[0][0]

    while i <= i_last:
            
        if stu_list[k][0] != stu[i][0]:
            stu_list[k+1][0] = stu[i][0]
            k = k + 1

        elif stu_list[k][0] == stu[i][0]:

            if stu[i][1] == 'out':
                if sample != 0:
                    stu_list[k][1] = stu_list[k][1] + stu[i][2] - sample
                    sample = 0
                        
                i = i + 1

            elif stu[i][1] == 'in':
                sample = stu[i][2]
                i = i + 1

    stu_list = sorted(stu_list, reverse=True, key=lambda x: x[1])
    k_last = k

    if bln1.get(): #時間数ランキング

        k = 0
        
        while k <= k_last:
            txtbox4.insert('end',' ')
            txtbox4.insert('end', stu_list[k][0])
            txtbox4.insert('end',' ')
            txtbox4.insert('end', stu_list[k][1])
            txtbox4.insert('end','\n')
            k = k + 1

    elif bln2.get(): #全生徒記録
    
        i = 0
    
        while i <= i_last:
            txtbox4.insert('end',' ')
            txtbox4.insert('end', stu[i][0])
            txtbox4.insert('end',' ')
            txtbox4.insert('end', stu[i][1])
            txtbox4.insert('end',' ')
            txtbox4.insert('end', stu[i][2])
            txtbox4.insert('end','\n')
            i = i + 1

    elif bln3.get(): #個人記録選択

        t3 = txtbox3.get()
        i = 0
        k = 0
        txtbox4.insert('end','【登下校記録】\n')

        while i <= i_last:

            if t3 == stu[i][0]:
                txtbox4.insert('end',' ')
                txtbox4.insert('end', stu[i][0])
                txtbox4.insert('end',' ')
                txtbox4.insert('end', stu[i][1])
                txtbox4.insert('end',' ')
                txtbox4.insert('end', stu[i][2])
                txtbox4.insert('end','\n')

            i = i + 1

        txtbox4.insert('end','\n【時間数記録】\n')

        while k <= k_last:

            if t3 == stu_list[k][0]:
                txtbox4.insert('end',' ')
                txtbox4.insert('end', stu_list[k][0])
                txtbox4.insert('end',' ')
                txtbox4.insert('end', stu_list[k][1])
                txtbox4.insert('end','\n')

            k = k + 1
            
    if (bln1.get() and bln2.get() and bln3.get())or\
       (bln1.get() and bln2.get())or\
       (bln1.get() and bln3.get())or\
       (bln2.get() and bln3.get()): #複数選択
        txtbox4.delete('1.0', 'end')
        txtbox4.insert('end', ' Error' + '\n')
        txtbox4.insert('end', ' チェックボックスを複数選択しないでください' + '\n')
    
file = ''
window = tk.Tk()
window.geometry('340x600')
window.title('自習室管理')

input_label = tk.Label(text="登下守データ")
input_label.place(x=40,y=20)
btn1 = tk.Button(text = 'ファイル選択', command = btn1Click)
btn1.place(x=130, y=20, width=70, height=20)

input_label = tk.Label(text="期間設定")
input_label.place(x=40,y=60)
txtbox1 = tk.Entry()
txtbox1.insert(tk.END,'2021/07/15')
txtbox1.place(x=130, y=63, width=70, height=15)
input_label = tk.Label(text="～")
input_label.place(x=205,y=60)
txtbox2 = tk.Entry()
txtbox2.insert(tk.END,'2021/07/21')
txtbox2.place(x=230, y=63, width=70, height=15)

input_label = tk.Label(text="表示設定")
input_label.place(x=40,y=100)

bln1 = tk.BooleanVar()
bln1.set(True)
bln2 = tk.BooleanVar()
bln2.set(False)
bln3 = tk.BooleanVar()
bln3.set(False)
chk1 = tk.Checkbutton(window,variable=bln1,text='時間数ランキング')
chk1.place(x=125,y=100)
chk2 = tk.Checkbutton(window,variable=bln2,text='全生徒記録')
chk2.place(x=125,y=120)
chk3 = tk.Checkbutton(window,variable=bln3,text='個人記録   氏名')
chk3.place(x=125,y=140)

txtbox3 = tk.Entry()
txtbox3.insert(tk.END,'渡辺　琳')
txtbox3.place(x=230, y=145, width=70, height=15)

btn2 = tk.Button(text = '表示', command = btn2Click)
btn2.place(x=30, y=180, width=70, height=20)

txtbox4 = st.ScrolledText()
txtbox4.place(x=0, y=240, width=340, height=360)

txtbox1.focus_set()
window.mainloop()
