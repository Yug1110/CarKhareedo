f=open('supplier_file.txt',"r")
x=f.read()
a=int(x)
x=str(a+1)
f.close()
f=open('supplier_file.txt',"w")
f.write(x)
f.close()