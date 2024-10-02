## Get elevation difference between artifact and paleosol
## blpotter 2024-02-23
## Step 1:    Find distance to all paleosol elevation data points
## Step 2:    Select minimum distance
## Step 3:    Calculate difference in Z values
## Step 4:    Append that value to artifact data
### 
#### Get files and make sure they work
import pandas as pd
import numpy as np
import csv
import math
import time
#### Starting values:
r = 0
distb = None
distm = None
rminb = None
rminm = None
#### Prep, get, verify input:
resp = input("This program requires three csv files:\n one with artifact N/E/Z data and first column labeled \"Art_ID\",\n one with Bk N/E/Z shot data,\n and one with modern surface N/E/Z shot data.\n Do you have all these files in your current working directory?\n Y/N\n")
if resp == "N":
    print("Fix this and come back later.")
    exit
else:
        art = input("Input name of artifact location data file: ")
        Bk = input("Input name of Bk elevation data file: ")
        surf = input("Input name of modern surface elevation data file: ")
try:
        fBk = open(Bk)
except:
    print("Bk file does not work.")
    exit
try:
    fart = open(art)
except:
    print("Artifact file does not work.")
    exit
try:
    fsurf = open(surf)
except:
    print("Modern surface shot file does not work.")
    exit
#### Set up data nicely in array formats
dfart = np.genfromtxt(art, delimiter=',')
dfBk = np.genfromtxt(fBk, delimiter=',') 
dfsurf = np.genfromtxt(surf, delimiter=',')
dfart2 = pd.read_csv(art)
IDlist = list(dfart2['Art_ID'])
newdf = pd.DataFrame({
    'ID':[],
    'N':[],
    'E':[],
    'Z':[],
    'Bk_diff':[],
    'Mod_diff':[]
})
#### Pull closest points in paleosols and surfs
for row in dfart:
    r=r+1
    try:
        xa = dfart[r,2]
        ya = dfart[r,1]
        r1 = 1
        while r1 < np.shape(dfBk)[0]:
            xb = dfBk[r1,1]
            yb = dfBk[r1,0]
            bdistc = math.sqrt(((xa-xb)**2)+((ya-yb)**2))
            if distb is None or abs(bdistc) < abs(distb):
                distb = bdistc
                rminb = r1
            r1 = r1+1
            continue
        r2 = 1
        while r2 <  np.shape(dfsurf)[0]:
            xs = dfsurf[r2,1]
            ys = dfsurf[r2,0]
            sdistc = math.sqrt(((xa-xs)**2)+((ya-ys)**2))
            if distm is None or abs(sdistc) < abs(distm):
                distm = sdistc
                rminm = r2
            r2 = r2+1
            continue
        za = dfart[r,3]
        zb = dfBk[rminb,2]
        zs = dfsurf[rminm,2]
        diffb = za-zb ## Calculate distance to Bk horizon (pos = above, neg = below)
        diffm = za-zs ## Calculate distance to modern surface (pos = above, neg = below)
        newrow = {'ID':IDlist[r],'N':ya,'E':xa,'Z':za,'Bk_diff':diffb,'Mod_diff':diffm} ## build new row
        newdf.loc[len(newdf)] = newrow 
    except:
        print('nope')
        exit
print(newdf)
timestr = time.strftime("%Y%m%d-%H%M%S")
fn = 'relative_z_'+timestr+'.csv'
newdf.to_csv(fn,index=False)
print('saved as csv to current directory')
print("postivie vals indicate artifact above ref surf;\nnegative vals indicate artifact below ref surf")
