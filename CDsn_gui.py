#!/usr/bin/python3

'''
See:
https://likegeeks.com/python-gui-examples-tkinter-tutorial/
https://riptutorial.com/tkinter/example/29714/place--
Removed X cols as not needed.
JM Wed 28 Aug 10:45:32 BST 2019
Added import of actual working suff / nec code.
JM Tue  1 Oct 16:47:27 BST 2019
'''

from tkinter import *
from tkinter.ttk import *
import os

import CDsuffp3_multi
import CDnecp3_multi

csvlist = [ ]

flist = os.listdir( './' )
for f in ( flist ):
    if ( f.endswith( '.csv' ) ):
        csvlist.append( f )
	# Only append csv files for combo box file choice.

rownum = 0
 
def clicked():
	# Need to stop proc from exiting after running proc.
	fname = combofn.get()  
	Yval  = yvar1.get() 
	snb   = snvar1.get()
	if( snb == 1 ):
		# Suff
		msg = 'Running ' + fname + ' Y: ' + str( Yval ) + ' Suff'
		lblfille.configure(text = msg )
		finmsg = 'Finished ' + fname + ' Y: ' + str( Yval ) + ' Suff'
		CDsuffp3_multi.suff_main( fname, Yval )
		lblfille.configure(text = finmsg )
	elif( snb == 2 ):
		# Nec
		msg = 'Running ' + fname + ' Y: ' + str( Yval ) + ' Nec'
		lblfille.configure(text = msg )
		finmsg = 'Finished ' + fname + ' Y: ' + str( Yval ) + ' Nec'
		CDnecp3_multi.nec_main( fname, Yval )
		lblfille.configure(text = finmsg )
	elif( snb == 3 ):
		# Suff & Nec
		msg = 'Running ' + fname + ' Y: ' + str( Yval ) + ' Suff & Nec'
		lblfille.configure(text = msg )
		finmsg = 'Finished ' + fname + ' Y: ' + str( Yval ) + ' Suff & Nec'
		CDsuffp3_multi.suff_main( fname, Yval )
		CDnecp3_multi.nec_main( fname, Yval )
		lblfille.configure(text = finmsg )

	lblfillf.configure(text = 'xxxxxxxxxxxx' )

window = Tk()

#window.font(20)
 
window.title("FSGOF")
window.geometry('550x550')
 
lbl = Label(window, text="Fuzzy Set Goodness of Fit", font=("Arial Bold", 20) )
 
lbl.grid(column=0, row=rownum)
#print('R:', rownum)
rownum += 1
 
lblfillbfrqca = Label(window, text="")
 
lblfillbfrqca.grid(column=0, row=rownum)
#print('R:', rownum)
rownum += 1
 
lblqca = Label(window, text="Qualitative Comparitive Analysis", font=("Arial Bold", 20) )
 
lblqca.grid(column=0, row=rownum)
#print('R:', rownum)
rownum += 1
 
lblfilla = Label(window, text="")
 
lblfilla.grid(column=0, row=rownum)
#print('R:', rownum)
rownum += 1
 
lbl2 = Label(window, text="Choose a File Name", font=("Arial Bold", 20))
 
lbl2.grid(column=0, row = rownum )
#print('R:', rownum)
rownum += 1

lblfillc = Label(window, text="")
 
lblfillc.grid(column=0, row=rownum)
#print('R:', rownum)
rownum += 1
 
combofn = Combobox(window)
combofn['values'] = csvlist 
combofn.current(0) #set the selected item
combofn.grid(column=0, row = rownum )
#print('R:', rownum)
rownum += 1

lblfillb = Label(window, text="")
 
lblfillb.grid(column=0, row = rownum)
#print('R:', rownum)
rownum += 1

lbl3 = Label(window, text="Choose Y-Column", font=("Arial Bold", 20))
 
lbl3.grid(column=0, row = rownum )
#print('R:', rownum)
rownum += 1
 
# Only need one variable so that only one can be picked.
# yvar1 returns value variable setting, ie 1-4.
yvar1 = IntVar() 
yvar1.set(1)
rad1 = Radiobutton(window,text='Y1', value=1, variable = yvar1 )
rad2 = Radiobutton(window,text='Y2', value=2, variable = yvar1 )
rad3 = Radiobutton(window,text='Y3', value=3, variable = yvar1 )
rad4 = Radiobutton(window,text='Y4', value=4, variable = yvar1 )

rad1.grid(column=0, row = rownum )
rownum += 1
rad2.grid(column=0, row = rownum )
rownum += 1
rad3.grid(column=0, row = rownum )
rownum += 1
rad4.grid(column=0, row = rownum )
rownum += 1
#print('R:', rownum)

lblfillfda = Label(window, text="")
 
lblfillfda.grid(column=0, row = rownum)
#print('R:', rownum)
rownum += 1

lblfilld = Label(window, text="  Choose: Sufficient, Necessary or Both", font=("Arial Bold", 20))
 
lblfilld.grid(column=0, row = rownum)
#print('R:', rownum)
rownum += 1

snvar1 = IntVar() 
snvar1.set(1)
rad5 = Radiobutton(window,text='Sufficient', value=1, variable = snvar1 )
rad6 = Radiobutton(window,text='Necessary ', value=2, variable = snvar1 )
rad7 = Radiobutton(window,text='Both      ', value=3, variable = snvar1 )

rad5.grid(column=0, row = rownum )
rownum += 1
rad6.grid(column=0, row = rownum )
rownum += 1
rad7.grid(column=0, row = rownum )
rownum += 1

lblfillfa = Label(window, text="")
 
lblfillfa.grid(column=0, row = rownum)
#print('R:', rownum)
rownum += 1

lblfillc = Label(window, text="")
 
lblfillc.grid(column=0, row = rownum)
#print('R:', rownum)
rownum += 1

btn = Button(window, text="Run", command=clicked )
 
btn.grid(column=0, row = rownum)
#print('R:', rownum)
rownum += 1

lblfillf = Label(window, text="")
 
lblfillf.grid(column=0, row = rownum)
#print('R:', rownum)
rownum += 1

lblfille = Label(window, text="")
 
lblfille.grid(column=0, row = rownum)
#print('R:', rownum)
rownum += 1

window.mainloop()
