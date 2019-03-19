for i in range(0,8):
    for j in range(0,32):
        if j<10:
            buf = "%d0%d.txt" % (i, j)

        else:
            buf = "%d%d.txt" % (i, j)
        fo=open(buf,"w")
        fo.close()

