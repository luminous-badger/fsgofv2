#!/usr/bin/python3

# Read in file and add to dictionary. Python 3 version.
# No longer uses indvidual add to list. Adds direct to dictionary. Improvement !
# JM Mon 26 Aug 12:37:40 BST 2019
# Splits up combination list into indivdual lists and then processes the in one proc.
# No need for multiple procs.
# JM Fri 30 Aug 16:17:13 BST 2019
# Calculates Csuff in one procedure. Add graph plot.
# Version 1 to calculate C&D Suff with 2-11 X columns & 4 Y columns
# JM Thu  5 Sep 12:09:34 BST 2019
# Added test for call from Cmd Line or from GUI.
# All output to directory based on input filename and date/time.
# JM Tue 24 Sep 18:13:38 BST 2019

import datetime
from scipy.stats import norm, f
import matplotlib.pyplot as plt
import itertools
import csv
import sys
import os

damping_factor   = 0.01
error_value      = 0.1
reqfontsize      = 8
#print( 'F:', fname )

X0list = []
X1list = []
X2list = []
X3list = []
X4list = []
X5list = []
X6list = []
X7list = []
X8list = []
X9list = []
X10list = []
X11list = []
YNlist  = []

column_dict = {
1 : X1list ,
2 : X2list ,
3 : X3list ,
4 : X4list ,
5 : X5list ,
6 : X6list ,
7 : X7list ,
8 : X8list ,
9 : X9list ,
10 : X10list ,
11 : X11list ,
12 : YNlist
}

def read_file( fname, Yval ):
#	print( 'Reading:', fname )    
	with open( fname, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			linelist = list( row )			
			linel = len( linelist )
			CDYval = linel - 5 + Yval 
			# NumXcols = line len minus 4 Y cols and 1 header col.
			NumXcols = linel - 5 
			# Use for loop and append. Don't need to add to each list by name.
			# Last four cols in input file are the Y vals.
			# Added proc of any blank values.
			for Xlocal in range ( 1, linel - 4 ):
				if( not linelist[ Xlocal ] ):
					column_dict[ Xlocal ].append( 0.0 )
				else:
					try:
						column_dict[ Xlocal ].append( float ( linelist[ Xlocal ] ) )
					except:
						#print( 'CD Err:', linelist[ Xlocal ], 'Len:', len( linelist[ Xlocal ] ) )
						pass
			try:
				column_dict[ 12 ].append( float ( linelist[ CDYval ] ) )
			except:
				pass
	return NumXcols

#************** End Read   ************** 

def plot_zt_graph( xlist = [], ylist = [], pltitle = 'DXY', fname = 'DXY.png', Yval = 1, opdirname = './' ):
	Xmin = -3.0
	Ymin = -3.0
	Xmax =  3.0
	Ymax =  3.0
#	print( 'ZT OP Dirname:', opdirname )
	fname = opdirname + '/' + fname

	plt.figure( figsize=( 3, 3 ) ) 
	# Sets size of axis ticks and numbers.
	plt.tick_params(labelsize=6)
	plt.title( pltitle,fontsize=reqfontsize )
	plt.xlabel( 'ZX',fontsize=reqfontsize )
	plt.ylabel( 'ZY' + str( Yval ),fontsize=reqfontsize )

	plt.plot( [ Xmin, Xmax ], [ Ymin, Ymax ], '--', lw=2 )
	plt.plot( [ xlist ], [ ylist ], 'rD', markersize=5 )
	
	plt.savefig( fname )
	plt.close()
	# Need to close to free up memory. Stops next slide being overwritten with previous slide data.

#************** End plot_zt_graph ******* 

def Ztransform( zlist =[] ):
	for ZL in range(0, len( zlist ), 1 ):
		if   ( zlist[ ZL ] < damping_factor ):
			zlist[ ZL ] = damping_factor
		elif ( zlist[ ZL ] > 1 - damping_factor ):
			zlist[ ZL ] = 1 - damping_factor
		
	qzxlist = norm.ppf( zlist )
	return qzxlist

#************** End Ztransform ********** 

def calc_df1(  xlist, ylist ):
	df1 = 0.0
	for XL in range(0, len( xlist ), 1 ):
		
		if ( ylist[ XL ] < xlist[ XL ] ):
			df1 += 1
		
	return df1 		
		
#************** End calc_df1 ************ 

def calc_ssd(  xlist, ylist, pltitle = 'DXY', fname = 'DXY.png', Yval = 1, opdirname = './' ):
	ssd = 0.0
	zxlist = Ztransform( xlist )
	zylist = Ztransform( ylist )
	#print( 'SSD OP Dirname:', opdirname )
	#print( 'SSD OP Fname:', fname )
	#print( 'SSD OP Y:', Yval )
	plot_zt_graph( zxlist, zylist, pltitle, fname, Yval, opdirname )
	
	for XL in range(0, len( xlist ), 1 ):
		
		if ( ylist[ XL ] > xlist[ XL ] ):
			d = 1
		else:
			d = 0
		
		ssd += ( 1 - d ) *  ( zylist[ XL ] - zxlist[ XL ] )**2 
		
	return ssd 

#************** End calc_ssd ************ 

def calc_nullsd2( xlist, ylist, error_value ):	
# Use different calculation method for nullsd
	nullsd = 0.0
	df2 = len( ylist )
	nullsd = df2 * error_value**2
	return nullsd
	
#************** End calc_nullsd2 ******** 

def calc_nullsd1( xlist, ylist, error_value ):
	nullsd = 0.0
	for XL in range(0, len( xlist ), 1 ):
		if ( ylist[ XL ] > xlist[ XL ] ):
			S = 1
		else:
			S = 0
		nullsd += ( S *( 2 * error_value - 2 * error_value * xlist[ XL ] ) + ( 1 - S ) * ( 2 * error_value * xlist[ XL ] ) )**2
	return nullsd
	
#************** End calc_nullsd1 ******** 

def proc_Dsuff(  xlist, ylist, pltitle = 'DXY', Csuff = 0.0, fname = 'DXY.png', Yval = 1, opdirname = './', opcsv = 'OP', optxt = 'OT' ):
	ssd = 0.0
	msd = 0.0
	df1 = 0.0
	F   = 0.0
	PVAL = 0.0
	nullsd = 0.0
	#print( 'PDsuff OP Dirname:', opdirname )
	ssd = calc_ssd(  xlist, ylist, pltitle, fname, Yval, opdirname )
	df1 = calc_df1(  xlist, ylist )
	
	df2 = len( ylist )

	nullsd = calc_nullsd2( xlist, ylist, error_value )
	emsd = nullsd 
	if ( df1 > 0 ):
		msd = ssd/df1
		F = msd/emsd 
		PVAL = f.sf ( F, df1, df2, loc=0, scale=1 ) 
	## Only do calcs if DF1 > 0. Error o'wise.
	## Write output to text file instead of on screen for GUI version.	
	## Spaces added for alignment.
	ProcLabel = os.path.splitext( fname )[0] 
	ProcLabel = ProcLabel.replace( 'D', '' ) # Remove D from Label.
	txtmsg = '{:>10s}'.format( ProcLabel ) + \
	' {:>2d}'.format( Yval ) + \
	' {:>4.3f}'.format( Csuff ) + \
	' {:>8.3f}'.format( ssd ) + \
	' {:>11.3f}'.format( F ) + \
	' {:>3.2f}'.format( PVAL ) + \
	' {:>3.2f}'.format( df1 ) + \
	'{:>3d}'.format( df2 ) + '\n'

	optxt.write( txtmsg )
	#print
	opcsv.writerow( [ ProcLabel, Yval, '{:>4.3f}'.format( Csuff ), '{:>8.3f}'.format( ssd ), 
	'{:>11.3f}'.format( F ), '{:>3.2f}'.format( PVAL ), '{:>3.2f}'.format( df1 ), '{:>3d}'.format( df2 ) ] )

#************** End proc_Dsuff ********** 

#************** Csuff Processing ************** 

def plot_graph( xlist = [], ylist = [], pltitle = 'XY', Csuff = 0.0, fname = 'XY.png', Yval = 1, opdirname = './' ):
	MinXaxis =  float( min( xlist ) ) - 1.0
	MaxXaxis =  float( max( xlist ) ) + 1.0

	MinYaxis =  float( min( ylist ) ) - 1.00
	MaxYaxis =  float( max( ylist ) ) + 1.00
	Xmin = 0.0
	Ymin = 0.0
	Xmax = 1.0
	Ymax = 1.0
	fname = opdirname + '/' + fname
	plt.figure( figsize=( 3, 3 ) ) 
	# Sets size of axis ticks and numbers.
	plt.tick_params(labelsize=6)

	plt.title( pltitle,fontsize=reqfontsize )
	plt.xlabel( 'X',fontsize=reqfontsize )
	plt.ylabel( 'Y' + str( Yval ),fontsize=reqfontsize )

	plt.plot( [ xlist ], [ ylist ], 'rD', markersize=15 )
	
	plt.plot( [ Xmin, Xmax ], [ Ymin, Ymax ], 'k-', lw=2 )

	plt.savefig( fname )
	plt.close()
	# Need to close to free up memory. Stops next slide being overwritten with previous slide data.

#************** End plot_graph ********** 

#************** Process Combinations **** 

def proc_cons4b( XvalListn=[], fname='XX', Yval=1, opdirname='./', opcsv = 'OP', optxt = 'OT' ):

    Csuff    = 0.0 # Csuff initialised
    CsuffNum = 0.0 # Csuff Numerator
    CsuffDen = 0.0 # Csuff Denominator
    xlist_plot = [] # Min of each X row for graph plotting.
    # LCD is number of rows in input file.
    for LCD in range( 0, len( column_dict[ 1 ] ), 1 ):
        numrl = [] # Numerator list
        denrl = [] # Denominator list
        fnamecs = 'X' 
        fnameds = 'DX' 
        pltitlecs = 'Plot of Y' + str( Yval ) + ' & Minimum of X'
        pltitleds = 'Plot of Z(Y' + str( Yval ) + ') & Z( Minimum of X'
        for xv in( XvalListn ):
            numrl.append(  column_dict[ xv ][LCD] )    
            denrl.append(  column_dict[ xv ][LCD] )    
            fnamecs = fnamecs + str(xv)
            fnameds = fnameds + str(xv)
            pltitlecs = pltitlecs + str(xv) 
            pltitleds = pltitleds + str(xv) 
        numrl.append(  column_dict[ 12 ][LCD] )    
        # numerator is min of row & Y val
        # denominator is just min of row.
	# xlist plot is list of mins of row denom for graph plotting.
        CsuffNum += min(numrl)
        CsuffDen += min(denrl)
        xlist_plot.append( min( denrl ) )
    if ( CsuffDen != 0 ):
        Csuff = CsuffNum / CsuffDen
    fnamecs = fnamecs + 'Y' + str(Yval) + '.png'
    fnameds = fnameds + 'Y' + str(Yval) + '.png'
    Csuffplot = ( '{:0.3f}' ).format( Csuff )
    # Reduce length of Csuff for plot title.
    pltitlecs = pltitlecs + '; Csuff = ' + Csuffplot
    pltitleds = pltitleds + ' )'
    #Plot output graphs.
    plot_graph( xlist_plot, column_dict[ 12 ], pltitlecs, Csuff, fnamecs, Yval, opdirname )
    proc_Dsuff( xlist_plot, column_dict[ 12 ], pltitleds, Csuff, fnameds, Yval, opdirname, opcsv, optxt )

#************** End proc_cons4 ********** 


####################### SUFF main #######################

def suff_main( fname, Yval ):
	#print( 'Processing File:', fname )
	#print( 'Fname:', os.path.splitext( fname )[0] )
	NumXcols = read_file( fname, Yval )
#	print( 'NumXcols:', NumXcols )

	opdirname = os.path.splitext( fname )[0]

	DandT     = datetime.datetime.now()
	opdirname = opdirname + '_suff_Y' + str( Yval ) + '_' + DandT.strftime( '%Y_%m_%d_%H_%M' )
	#print( 'OP Dirname:', opdirname )

	if ( os.path.exists( opdirname ) ):
	#	print( 'EXISTS OP Dirname:', opdirname )
		direxist = True
	else:
		os.mkdir( opdirname )
	#	print( 'OP Dirname:', opdirname )

	OPCSVfile = opdirname + '/' + 'outputX1to' + str( NumXcols ) + '_Y' + str( Yval ) + '_suff.csv'
	OPTXTfile = opdirname + '/' + 'outputX1to' + str( NumXcols ) + '_Y' + str( Yval ) + '_suff.txt'

	#print( 'Output to:', OPCSVfile )

	opcsv = csv.writer( open( OPCSVfile, 'w' ) )
	optxt = open( OPTXTfile, 'w' ) 

	# Headers for output.
	opcsv.writerow( [ 'Config', 'Y', 'Csuff', 'Dsuff', 'F', 'PVAL', 'Df1', 'Num' ] )

	optxt.write( '    Config  Y Csuff    Dsuff       F     PVAL DF1  DF2\n' )

	varlist = list( range(1, NumXcols + 1 ) )
	# NB range goes from start to end-1. Feature !

	# Need to cater for diff lengths of xval list. Hence 6 procs in orig prog.

	for Xindex in range(1, len(varlist) + 1):
		XvalList = list(itertools.combinations(varlist, Xindex))
		# use for xv in xvallist to process each item in xvallist separately.
		for xvv in( XvalList ):
			proc_cons4b( xvv, fname, Yval, opdirname, opcsv, optxt )

	optxt.close()

#************** End suff_main ********** 

#************** Cmd Line check *********
## Checks if called from command line.
if ( __name__ == '__main__' ):
	if ( len( sys.argv ) == 1 ):
	    fname = 'cs2k.csv'
	    Yval = 1
	elif ( len( sys.argv ) == 2 ):
	    fname = sys.argv[ 1 ]
	    Yval = 1
	elif ( len( sys.argv ) == 3 ):
	    fname = sys.argv[ 1 ]
	    Yval = int( sys.argv[ 2 ] )
	else:
	    fname = 'cs2k.csv'
	    Yval = 1

	if ( Yval > 4 ):
	    # Can't allow Y to be more than four. Only four Y vals allowed.
	    Yval = 1
	suff_main( fname, Yval )

