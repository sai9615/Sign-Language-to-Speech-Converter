import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")

print "Hello!!\nHow may i help you?\n"
print "Enter 1 if You want to train me :D\nEnter 2 if you want to test me :>\n"
ch = input();
print ch
compre =[0,0,0,0,0,0,0,0]
word=""

ind = [-1]
arr = ["","","","","","","",""]
ar_val = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
counter=0
no_of_frames=1
final_output="sf"
prev_out=""
new_out=""

def com_fun(ch,fil):
    
    fo=open(fil,"r+")
    flag=0
    if ch==1:
        word=fo.readline();
        #print word
    pos=-1
    num=fo.readline();
    while int(num)!=999:
        #print num
        if pos==6:
            flag =1
        pos=pos+1
        compre[pos]=int(num)/8
        if flag==1:
            if ch==1:
                data_fun(word)
            else:
                out_fun()
            #print compre
            pos=-1
            flag=0
       # position=fo.seek(1,1);
        num=fo.readline();
 
    fo.close()

def data_fun(word):
    for i in range(0,8):
        c=0
        if compre[i]<10:
            buf = "%d0%d.txt" % (i, compre[i])

        else:
            buf = "%d%d.txt" % (i, compre[i])
        #print buf
        fo=open(buf,"a+")
        strg=fo.readline();
        #print strg
        while(strg!=""):
            if(strg == word):
                #print "yes"
                c=1
            
            strg=fo.readline();
        if c==0 :
            fo.seek(0,2)
            #print "datafun", word
            fo.write("%s0.02\n" % word)
        
        fo.close();

def out_fun() :
    #print "beg",ar_val
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
                
def trig():
    global prev_out, counter, no_of_frames, final_output
    #print arr, ar_val
    pos=ar_val.index( max(ar_val) )
    new_out=arr[pos].rstrip()
    if(new_out!=prev_out):
        #if(final_output!=prev_out):
            #    disp(final_output)
        if(counter>=no_of_frames):
            #if(final_output!=new_out):        #i change
                disp(final_output)
                #print "yo"#i change
            #final_output=new_out#prev_out
            #print final_output, "final"
        counter=1
        prev_out=new_out
    else:
        counter=counter+1
        if(counter>=no_of_frames):
            final_output=prev_out
           
        
    for i in range(0,ind[0]+1):
            ar_val[i]=0.0
    print counter   
def disp(buff):
    print buff
    speak.Speak(buff)

if ch==1:
    print "Enter the file name"
    fil=raw_input()
    com_fun(ch,fil)
elif ch==2:
    print "Enter the file name"
    fil=raw_input()
    com_fun(ch,fil)
else:
    print "Your choice is unintelligent\n"


       
