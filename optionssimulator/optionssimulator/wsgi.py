"""
WSGI config for optionssimulator project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

from multiprocessing.sharedctypes import Value

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optionssimulator.settings')

application = get_wsgi_application()

import threading
import time
from thefirstock import thefirstock
from tradesim.models import dashboard, displaydata, optionchain, positions, builder, inview
from tradesim import views
inviewdata=inview.objects.all()

def userLogin():
  thefirstock.firstock_login(
    userId='USERID',
    password='PASSWORD',
    DOBnPAN='PAN/DOB',
    vendorCode='VENDORCODE',
    apiKey='APIKEY',   
  ) 
def userLogout():
  thefirstock.firstock_logout()
userLogin()
def displayfetch():
    while True:
        nifty= thefirstock.firstock_GetQuotes(
        exchange='NSE', 
        token='26000',
        )
        banknifty=thefirstock.firstock_GetQuotes(
        exchange='NSE', 
        token='26009',
        )
        indiavix=thefirstock.firstock_GetQuotes(
        exchange='NSE', 
        token='26017',
        )
        if(nifty['stat']=='Ok'):
            niftypercent=round((float(nifty['lp'])-float(nifty['c']))*100/float(nifty['c']), 2)
            displaydata.objects.filter(name="Nifty").update(value=float(nifty['lp']), percentagechange=niftypercent)
        if(banknifty['stat']=='Ok'):
            bankniftypercent=round((float(banknifty['lp'])-float(banknifty['c']))*100/float(banknifty['c']), 2)
            displaydata.objects.filter(name="Bank Nifty").update(value=float(banknifty['lp']), percentagechange=bankniftypercent)
        if(indiavix['stat']=='Ok'):
            indiavixpercent=round((float(indiavix['lp'])-float(indiavix['c']))*100/float(indiavix['c']), 2)
            displaydata.objects.filter(name="India VIX").update(value=float(indiavix['lp']), percentagechange=indiavixpercent)
        time.sleep(1)

def chainscripfetch(strk, i):
    scrip=thefirstock.firstock_GetQuotes(
                    exchange='NFO', 
                    token=strk['token'],
                    )
    scripexpiry=scrip['exd']
    scripexpiry = scripexpiry.replace("-20", "")
    scripexpiry=scripexpiry.replace("-","")
    if(i<40):
        optionchain.objects.filter(id=i+689).update(strike=scrip['strprc'], ctoken=int(scrip['token']), expiry=scripexpiry, cltp=float(scrip['lp']), coi=float(scrip['oi']))
    elif(i>=40):
        optionchain.objects.filter(id=i+649).update(ptoken=int(scrip['token']), pltp=float(scrip['lp']), poi=float(scrip['oi']))
SPOT_STRIKE=1.00
OC={}
EXPIRY=""
def optionchainfetch():
    global SPOT_STRIKE, OC, EXPIRY
    while True:
        while views.CHAIN_UPDATED: 
            niftydata=displaydata.objects.filter(name="Nifty").all()
            spot=float(niftydata[0].value)
            spotstrike=50 * round(spot/50)
            expiry=inviewdata[0].expiry
            if(SPOT_STRIKE!=spotstrike or EXPIRY!=expiry):
                SPOT_STRIKE=spotstrike
                EXPIRY=expiry
                symbol='NIFTY'+expiry+'P'+str(spotstrike)
                OC =thefirstock.firstock_OptionChain(
                    tradingSymbol=symbol,
                    exchange='NFO',
                    strikePrice=spotstrike,
                    count="20",
                    )
            if OC['stat']=="Ok":       
                threadsce=[]
                for i in range(40):
                    t=threading.Thread(target=chainscripfetch, args=[OC['values'][i],i])
                    t.start()
                    threadsce.append(t)
                for thread in threadsce:
                    thread.join()
                
                threadspe=[]
                for i in range(39,80):
                    t=threading.Thread(target=chainscripfetch, args=[OC['values'][i],i])
                    t.start()
                    threadspe.append(t)
                for thread in threadspe:
                    thread.join()
                time.sleep(0.7)

def builderscripfetch(token):
    scrip=thefirstock.firstock_GetQuotes(
                    exchange='NFO', 
                    token=token,
                    )
    if scrip['stat']=="Ok":
        scripexpiry=scrip['exd']
        scripexpiry = scripexpiry.replace("-20", "")
        scripexpiry=scripexpiry.replace("-","")
        builder.objects.filter(strategy=inviewdata[0].strategy, createdon=inviewdata[0].createdon, token=token).update(expiry=scripexpiry, strike=scrip['strprc'], cepe=scrip['optt'], price=scrip['lp'])

def builderfetch():
    while True:
        data=builder.objects.filter(strategy=inviewdata[0].strategy, createdon=inviewdata[0].createdon).all()
        threads=[]
        for each in data:
            t=threading.Thread(target=builderscripfetch, args=[each.token])
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()
        time.sleep(0.33)

def positionscripfetch(token, entry, lots, bs, stoploss):
    scrip=thefirstock.firstock_GetQuotes(
                    exchange='NFO', 
                    token=token,
                    )
    if scrip['stat']=="Ok":
        if bs=="B": 
            pnl=round((float(scrip['lp'])-float(entry))*lots*50,2)
            if stoploss:
                if float(scrip['lp'])<=float(stoploss):
                    positions.objects.filter(strategy=inviewdata[0].strategy, createdon=inviewdata[0].createdon, token=token).update(price=scrip['lp'], pnl=pnl, active=False)
                    views.POSITION_UPDATED=True            
        elif bs=="S":
            pnl=round((float(entry)-float(scrip['lp']))*lots*50,2)
            if stoploss:
                if float(scrip['lp'])>=float(stoploss) and stoploss:
                    positions.objects.filter(strategy=inviewdata[0].strategy, createdon=inviewdata[0].createdon, token=token).update(price=scrip['lp'], pnl=pnl, active=False)
                    views.POSITION_UPDATED=True        
        
        positions.objects.filter(strategy=inviewdata[0].strategy, createdon=inviewdata[0].createdon, token=token, active=True).update(price=scrip['lp'], pnl=pnl)
        

def positionfetch():           
    while True:
        data=positions.objects.filter(strategy=inviewdata[0].strategy, createdon=inviewdata[0].createdon, archived=False, active=True).all()
        threads=[]
        for each in data:
            t=threading.Thread(target=positionscripfetch, args=[each.token, each.entry, each.lots, each.bs, each.stoploss])
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()
        time.sleep(0.3)

thread1 = threading.Thread(target=displayfetch)
thread1.start()      
thread2 = threading.Thread(target=optionchainfetch)
thread2.start()
thread3 = threading.Thread(target=builderfetch)
thread3.start()
thread4 = threading.Thread(target=positionfetch)
thread4.start()