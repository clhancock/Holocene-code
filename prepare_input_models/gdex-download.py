#!/usr/bin/env python
""" 
Python script to download selected files from gdex.ucar.edu.
After you save the file, don't forget to make it executable
i.e. - "chmod 755 <name_of_script>"
"""
import sys, os
from urllib.request import build_opener

os.chdir('/Users/christopherhancock/Library/CloudStorage/OneDrive-NorthernArizonaUniversity/ECS_DA/data/models/original_model_data/TraCE_21ka/')

opener = build_opener()
var='PRECC' # convective precipitation (PRECT=PRECC+PRECL)
var='PRECC' # convective precipitation (PRECT=PRECC+PRECL)
var='QFLX' # large-scale precipitation (PRECT=PRECC+PRECL)
var='RELHUM' #relative humidity
var='PS' #Pressure
var='FSNS' #net sortwave radiation
var='FLNS'#net longwave radiation
#var='PRECT' # PRECT=PRECC+PRECL
for var in ['TS']: #['TREFHT','PRECL','PRECC','QFLX','PS','PSL','RELHUM','FSNS','FLNS','LANDFRAC','QOVER','SNOWICE']:#,PS'RELHUM','FSNS','FLNS','QOVER']:
    if var in ['QOVER','SNOWICE']:
        filelist = [
            f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/lnd/proc/tavg/decadal/trace.01-36.22000BP.clm2.{var}.22000BP_decavg_400BCE.ncc',    
        ]
    elif var in ['PS','PSL','RELHUM','FSNS','FLNS','FSDS','LANDFRAC']:
        filelist = [
            f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tavg/decadal/trace.01-36.22000BP.cam2.{var}.22000BP_decavg_400BCE.nc',
        ]
    else: 
        filelist = [
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tavg/decadal/trace.01-36.22000BP.cam2.{var}.22000BP_decavg_400BCE.nc',
          #  
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.01.22000-20001BP.clm2.h0.{var}.0000101-0200012.nc',    
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.01.22000-20001BP.cam2.h0.{var}.0000101-0200012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.02.20000-19001BP.cam2.h0.{var}.0200101-0300012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.03.19000-18501BP.cam2.h0.{var}.0300101-0350012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.04.18500-18401BP.cam2.h0.{var}.0350101-0360012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.05.18400-17501BP.cam2.h0.{var}.0360101-0450012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.06.17500-17001BP.cam2.h0.{var}.0450101-0500012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.07.17000-16001BP.cam2.h0.{var}.0500101-0600012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.08.16000-15001BP.cam2.h0.{var}.0600101-0700012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.09.15000-14901BP.cam2.h0.{var}.0700101-0710012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.10.14900-14351BP.cam2.h0.{var}.0710101-0765012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.11.14350-13871BP.cam2.h0.{var}.0765101-0813012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.12.13870-13101BP.cam2.h0.{var}.0813101-0890012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.13.13100-12901BP.cam2.h0.{var}.0890101-0910012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.14.12900-12501BP.cam2.h0.{var}.0910101-0950012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.15.12500-12001BP.cam2.h0.{var}.0950101-1000012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.16.12000-11701BP.cam2.h0.{var}.1000101-1030012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.17.11700-11301BP.cam2.h0.{var}.1030101-1070012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.18.11300-10801BP.cam2.h0.{var}.1070101-1120012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.19.10800-10201BP.cam2.h0.{var}.1120101-1180012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.20.10200-09701BP.cam2.h0.{var}.1180101-1230012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.21.09700-09201BP.cam2.h0.{var}.1230101-1280012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.22.09200-08701BP.cam2.h0.{var}.1280101-1330012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.23.08700-08501BP.cam2.h0.{var}.1330101-1350012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.24.08500-08001BP.cam2.h0.{var}.1350101-1400012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.25.08000-07601BP.cam2.h0.{var}.1400101-1440012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.26.07600-07201BP.cam2.h0.{var}.1440101-1480012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.27.07200-06701BP.cam2.h0.{var}.1480101-1530012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.28.06700-06201BP.cam2.h0.{var}.1530101-1580012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.29.06200-05701BP.cam2.h0.{var}.1580101-1630012.nc',   
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.30.05700-05001BP.cam2.h0.{var}.1630101-1700012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.31.05000-04001BP.cam2.h0.{var}.1700101-1800012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.32.04000-03201BP.cam2.h0.{var}.1800101-1880012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.33.03200-02401BP.cam2.h0.{var}.1880101-1960012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.34.02400-01401BP.cam2.h0.{var}.1960101-2060012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.35.01400-00401BP.cam2.h0.{var}.2060101-2160012.nc',
          f'https://osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/TraCE-Main/atm/proc/tseries/monthly/{var}/trace.36.400BP-1990CE.cam2.h0.{var}.2160101-2204012.nc',
        ]


    for i,file in enumerate(filelist[:]):
        #print(i)
        if file.split('/')[-1] in os.listdir(): continue
        try:
            ofile = os.path.basename(file)
            sys.stdout.write("downloading " + ofile + " ... ")
            sys.stdout.flush()
            infile = opener.open(file)
            outfile = open(ofile, "wb")
            outfile.write(infile.read())
            outfile.close()
            sys.stdout.write("done\n")
        except:
            print('!!!!!!!!!!!!!!!!!'+str(i)+' FAIL!!!!!!!!!!!!!!!!!!!!!!')
            continue
#%%
os.chdir('/Users/christopherhancock/Library/CloudStorage/OneDrive-NorthernArizonaUniversity/ECS_DA/data/models/original_model_data/HadCM3B_transient21k/')


for var in ['temp_mm_1_5m']: 
    filelist = [f'https://www.paleo.bristol.ac.uk/HadCM3B_transient21k/deglh/vn1_0/{var}/010/deglh.vn1_0.{var}.monthly.ANN.010.nc'
                ]
    for i,file in enumerate(filelist[:]):
        #print(i)
        if file.split('/')[-1] in os.listdir(): continue
        try:
            ofile = os.path.basename(file)
            sys.stdout.write("downloading " + ofile + " ... ")
            sys.stdout.flush()
            infile = opener.open(file)
            outfile = open(ofile, "wb")
            outfile.write(infile.read())
            outfile.close()
            sys.stdout.write("done\n")
        except:
            print('!!!!!!!!!!!!!!!!!'+str(i)+' FAIL!!!!!!!!!!!!!!!!!!!!!!')
            continue
        #%%
        
        
#TS (Surface Temperature) represents the temperature of the surface itself, which includes land, ocean, or ice.
path='/Users/christopherhancock/Library/CloudStorage/OneDrive-NorthernArizonaUniversity/ECS_DA/data/models/original_model_data/TraCE_21ka/'
fn='trace.01.22000-20001BP.cam2.h0.TS.0000101-0200012.nc'
handle = xr.open_dataset(path+fn)

fn2= 'trace.01-36.22000BP.pop.TEMP.22000BP_decavg_400BCE.nc'
handle2 = xr.open_dataset(path+fn2)
