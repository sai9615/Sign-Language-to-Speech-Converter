#importing libraries
import collections
import Tkinter as tk
import threading
import serial
from collections import defaultdict
from playsound import playsound
import os


#path to audio files
base_dir = r'C:/Python27/Lib/site-packages/visual/examples/New folder/60%/New folder'


sen_val = collections.deque()
max_words = collections.deque()
q = collections.deque()
arduinoSerialData = serial.Serial('com3',9600) #communcation port


#initializing variables
count = 0
ch = 2
compre =[0,0,0,0,0,0,0,0]
word=" "
previous="NO WORD"
ind = [-1]
arr = ["","","","","","","",""]
ar_val = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
to_output="  "
prev_out=""
flag=0


def myfunc(): #start function
    left.start()
    right.start()


def capture(direction, nextSource): #sensor value capture function
    global count
    while(1):
            if(arduinoSerialData.inWaiting()>0):
                myData=arduinoSerialData.readline()
                md = myData.rstrip()
                sen_val.append(md)   
                count=count+1
                #print list(sen_val)       
    return


def processing_func(direction, nextSource):  #processing function
    while True:
         global count,flag
         if(count >= 8):
             for i in range(8):
                 compre[i]=int(sen_val[i])/8 #divide by 8
                 if(compre[i]<0 or compre[i]>31):
                     flag=1
             sen_val.popleft()
             sen_val.popleft()
             sen_val.popleft()
             sen_val.popleft()
             sen_val.popleft()
             sen_val.popleft()
             sen_val.popleft()
             sen_val.popleft()
             count-=8
             if(flag==0):
                 out_fun()
             flag=0
    return
   


def out_fun() : #calculate signal value
    c=0
    for i in range(0,8):
        
        if compre[i]<10:
            buf = "%d0%d.txt" % (i, compre[i])
        else:
            buf = "%d%d.txt" % (i, compre[i])
        fo=open(buf,"r+")
        #print buf
        strg=fo.readline();
        
        while(strg!=""):
            c=0
            sig=fo.readline();
            for j in range(0,ind[0]+1):
                if strg == arr[j]:
                    c=1
                    ar_val[j] = ar_val[j] + 0.02
                    break
                
            if c==0 :
                ind[0]=ind[0]+1
                arr[ind[0]]="%s" % strg
                ar_val[ind[0]]=0.02
            strg=fo.readline();
        fo.close();
    trig()

                
def trig(): #find maximum word array and output word
    global to_output
    max_occur_word=""
    max_occur=0
    #print arr, ar_val
    pos=ar_val.index( max(ar_val) )
    new_out=arr[pos].rstrip()
    max_words.append(new_out)
    print max_words
    
    if(len(max_words)>=6):

        d=defaultdict(int)
        for i in max_words:
            d[i]+=1
        result=max(d.iteritems(), key=lambda x: x[1]) #find max occurance ie to_output
        max_occur_word=result[0]
        max_occur=result[1]/(6*1.0)
        
    if(to_output!=max_occur_word and max_occur>=0.5):
        
        disp(to_output)
        for i in range(0,6):
            max_words.popleft()
            max_words.append(max_occur_word)
        to_output=max_occur_word
        
    elif(max_occur<0.5):
        disp(to_output)
                           
    for i in range(0,ind[0]+1):
            ar_val[i]=0.0
            
    if(len(max_words)==6):
        max_words.popleft()
      
       
def disp(buff): #print function
    
    global prev_out
    
    if(prev_out!=buff):
        print (buff)
        q.append(buff)
        
    prev_out=buff
   
    
    
left = threading.Thread(target=capture, args=('Left', sen_val.popleft))
right = threading.Thread(target=processing_func, args=('Right', sen_val.pop))


def UI_label(label): #UI function
    
  end=".mp3"
  global word
  global base_dir
  
  def count():
    global previous
    
    if(q):
        word=q.popleft()
        previous=word
        filename=os.path.join(base_dir, word)
        filename1="%s.mp3" % filename
        abc=filename1.replace("/","\\")
        playsound(r'C:/Python27/Lib/site-packages/visual/examples/New folder/60%/New folder/NAME.mp3')#
    else:
        word=previous  
    label.config(text=word)   
    label.after(2000, count)
  count()


#UI design format
root = tk.Tk()
root['bg']='snow3'
root.title("Sign language Interpreter")
root.geometry("900x600")
label2 = tk.Label(root,text="  ",bg='snow3', font = "Times 100 italic ")
label2.pack()

label1 = tk.Label(root,text="GESTURE GLOVE", fg="dark blue",bg='snow3', font = "Times 60 italic ")
label1.pack()

label_space1 = tk.Label(root,text="  ",bg='snow3', font = "Times 10 italic ")
label_space1.pack()
label = tk.Label(root, fg="dark green",bg='snow3', font = "Times 50 bold")
label.pack()
label_space2 = tk.Label(root,text="  ",bg='snow3', font = "Times 10 italic ")
label_space2.pack()

UI_label(label)

button = tk.Button(root, text='START', width=20,bg="PeachPuff4", fg="white", font = "Times 12 bold " , command=myfunc)
button.pack()
button1 = tk.Button(root, text='STOP', width=20, bg="salmon3",  fg="white", font = "Times 12 bold " , command=root.destroy)
button1.pack()
root.mainloop()

#closing port
arduinoSerialData.close()
