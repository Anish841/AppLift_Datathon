__author__ = 'pratap'





import  pandas as pd
import numpy as np
df = pd.read_csv('pandasoutput.csv')

rowcount= len(df)

ctype = 0.0004
wtype = 0.034

clen = int(ctype*rowcount)
wlen = int(wtype*rowcount)

print clen,wlen


cdata = df[1:clen]
wdata = df[clen:wlen]
zdata = df[wlen:]


cdata['Fracexbid'] = 2.0

cbid = cdata[['Creative_ID','Excbid']]
cbidagg = cbid.groupby('Creative_ID', as_index=False).sum()

zdata['Fracexbid'] = 0.0

wbid = wdata[['Creative_ID','Excbid']]
wbidagg = wbid.groupby('Creative_ID', as_index=False).sum()

wbidagg.rename(columns={'Excbid':'WExcbid'},inplace =True)

meragg = cbidagg.merge(wbidagg, how = "outer", on = 'Creative_ID')

meragg['Fracexbid']= (meragg['WExcbid']-meragg['Excbid'])/meragg['WExcbid']


# meragg['Fracexbid'] = meragg['Fracexbid']

meragg.loc[meragg['Fracexbid']<0,'Fracexbid'] = 0

meraggafter=meragg.fillna(1)

wbidwfr = wdata.merge(meraggafter[['Creative_ID','Fracexbid']], how = "left", on = 'Creative_ID')

totalfr = pd.concat([cdata,wbidwfr,zdata])

totalfr['NExcbid']= totalfr['Excbid']*totalfr['Fracexbid']

totalfr.to_csv('experiment.csv',index=False)








