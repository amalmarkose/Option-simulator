from sqlite3 import Time
from time import time
from django.shortcuts import render
from .models import dashboard, displaydata, optionchain, positions, builder, inview
import datetime
from django.http import JsonResponse
from django.db.models import F
from django.db.models import Sum



DB_format = '%Y-%m-%d %H:%M:%S'
JSON_format = '%d-%m-%Y %H:%M:%S'
POSITION_UPDATED=True
CHAIN_UPDATED=True


def timeFormat(time):
  return datetime.datetime.strptime(time, JSON_format).strftime(DB_format)


def index(request):
  inviewdata=inview.objects.all()
  strategy=inviewdata[0].strategy
  createdon=inviewdata[0].createdon
  expiry=inviewdata[0].expiry
  return render(request, 'nifty.html',{"data": [{"expiry": expiry}, {"strategy": strategy}]})

def trade(request, id, strategy, expiry):
  datee=positions.objects.filter(id=id, strategy=strategy, expiry=expiry).all()[0].createdon
  inview.objects.filter(id=1).update(strategy=strategy, createdon=datee, expiry=expiry)
  inviewdata=inview.objects.all()
  strategy=inviewdata[0].strategy
  expiry=inviewdata[0].expiry
  return render(request, 'nifty.html',{"data": [{"expiry": expiry}, {"strategy": strategy}]})
   
def alltrades(request):
  inviewdata=inview.objects.all()
  expiry=inviewdata[0].expiry
  data=positions.objects.filter(archived=False)
  createdon=[]
  for each in data: 
    if each.createdon not in createdon:
      createdon.append(each.createdon)
  context=[]
  for i in createdon:
    data=positions.objects.filter(createdon=i).first()
    context.append(data)
  return render(request, 'trades.html',{"data": [{"expiry": expiry}, {"context": context}]})

def archived(request):
  inviewdata=inview.objects.all()
  expiry=inviewdata[0].expiry
  data=positions.objects.filter(archived=True)
  createdon=[]
  for each in data: 
    if each.createdon not in createdon:
      createdon.append(each.createdon)
  context=[]
  for i in createdon:
    data=positions.objects.filter(createdon=i).first()
    context.append(data)
  return render(request, 'archive.html',{"data": [{"expiry": expiry}, {"context": context}]})

def inviewpush(request):
  data= inview.objects.all()
  return JsonResponse({"messages":list(data.values())})

def inviewupdate(request, strategy, expiry):
  inview.objects.filter(id=1).update(strategy=strategy, expiry=expiry, createdon=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
  return JsonResponse({"messages":"true",})

def dashboardpush(request, name, date):
  data= dashboard.objects.filter(id=1)
  return JsonResponse({"messages":list(data.values())})

def displaydatapush(request):
  data= displaydata.objects.all()
  return JsonResponse({"messages":list(data.values())})

def positionspush(request, name, date):
  global POSITION_UPDATED
  data= positions.objects.filter(strategy=name, createdon=date, active=True)
  notactive=positions.objects.filter(strategy=name, createdon=date, active=False)
  totalpnl=positions.objects.filter(strategy=name, createdon=date).aggregate(Sum('pnl'))
  totallots=positions.objects.filter(strategy=name, createdon=date, active=True).aggregate(Sum('lots'))
  if POSITION_UPDATED==True:
      pos=True
      POSITION_UPDATED=False
  else:
    pos=False
  return JsonResponse({"messages":list(data.values()),"notactive":list(notactive.values()),"totalpnl":totalpnl, "totallots":totallots,"POSITION_UPDATED":pos})

def optionchainpush(request, expiry, active):
  global CHAIN_UPDATED
  
  if active=="false":
    CHAIN_UPDATED=False
    return JsonResponse({"messages":"false"})
  elif active=="true":
    CHAIN_UPDATED=True
    niftydata=displaydata.objects.filter(name="Nifty").all()
    spot=float(niftydata[0].value)
    spotstrike=50 * round(spot/50)
    data= optionchain.objects.filter(expiry=expiry).order_by('strike')
    return JsonResponse({"messages":list(data.values()),"spotstrike":spotstrike})

  




def builderpush(request, name, date):
  data= builder.objects.filter(strategy=name, createdon=date)
  return JsonResponse({"messages":list(data.values())})

def chartpush(request):
  inviewdata=inview.objects.all()
  strategy=inviewdata[0].strategy
  createdon=inviewdata[0].createdon
  spot= displaydata.objects.filter(name="Nifty")[0].value
  positiondata=positions.objects.filter(strategy=strategy, createdon=createdon, active=True).all()
  builderdata=builder.objects.filter(strategy=strategy, createdon=createdon).all()
  data=[]
  for each in positiondata:
    items={"strike":each.strike, "premium":each.entry, "lots":each.lots, "cepe":each.cepe, "bs":each.bs}
    data.append(items)
  for each in builderdata:
    items={"strike":each.strike, "premium":each.price, "lots":each.lots, "cepe":each.cepe, "bs":each.bs}
    data.append(items)
  return JsonResponse({"spot":spot,"data":data})

def buildermodify(request, token, bs, action):
  token=int(token)
  inviewdata=inview.objects.all()
  strategy=inviewdata[0].strategy
  createdon=inviewdata[0].createdon
  scripdb=builder.objects.filter(token=token, bs=bs, strategy=strategy, createdon=createdon)
  if action=="clear":
    builder.objects.filter(strategy=strategy, createdon=createdon).delete()
  else:
    if action=="add":
      if scripdb.exists():
          scripdb.update(lots=F('lots')+1)
      elif builder.objects.filter(token=token, strategy=strategy, createdon=createdon).exists():
          if builder.objects.filter(token=token, strategy=strategy, createdon=createdon).all()[0].lots>1:
            builder.objects.filter(token=token, strategy=strategy, createdon=createdon).update(lots=F('lots')-1)
          else:
            builder.objects.filter(token=token, strategy=strategy, createdon=createdon).delete()
      else:
          builder.objects.create(token=token, bs=bs, strategy=strategy, createdon=createdon)

    elif action=="substract":
          if scripdb.all()[0].lots>1:
            scripdb.update(lots=F('lots')-1)
          else:
            scripdb.delete()

    elif action=="remove":
          scripdb.delete()

    elif action=="plus":
      strike=builder.objects.filter(token=token, strategy=strategy, createdon=createdon).all()[0].strike
      cepe=builder.objects.filter(token=token, strategy=strategy, createdon=createdon).all()[0].cepe
      strike = int(strike)+50
      if cepe=="CE":
        newtoken=optionchain.objects.filter(strike=strike).all()[0].ctoken
      elif cepe=="PE":
        newtoken=optionchain.objects.filter(strike=strike).all()[0].ptoken
      builder.objects.filter(token=token, strategy=strategy, createdon=createdon).update(token=newtoken)
      
    elif action=="minus":
      strike=builder.objects.filter(token=token, strategy=strategy, createdon=createdon).all()[0].strike
      cepe=builder.objects.filter(token=token, strategy=strategy, createdon=createdon).all()[0].cepe
      strike = int(strike)-50
      if cepe=="CE":
        newtoken=optionchain.objects.filter(strike=strike).all()[0].ctoken
      elif cepe=="PE":
        newtoken=optionchain.objects.filter(strike=strike).all()[0].ptoken
      builder.objects.filter(token=token, strategy=strategy, createdon=createdon).update(token=newtoken)

  return JsonResponse({"messages":"true",})
def addtoposition(request):
  inviewdata=inview.objects.all()
  strategy=inviewdata[0].strategy
  createdon=inviewdata[0].createdon
  builds= builder.objects.filter(strategy=strategy, createdon=createdon).all()
  for each in builds:
    active=positions.objects.filter(token=each.token, strategy=strategy, createdon=createdon, active=True)
    if active.exists():
      if active.all()[0].bs != each.bs:
        activelots=int(active.all()[0].lots)
        eachlots=int(each.lots)
        if activelots>eachlots:
          active.update(lots= activelots-eachlots)
          if active.all()[0].bs=="B":
            pnl=(float(active.all()[0].entry)-float(active.all()[0].price))*eachlots
          elif active.all()[0].bs=="S":
            pnl=(float(active.all()[0].price)-float(active.all()[0].entry))*eachlots
          positions.objects.create(active=False, token=each.token, strategy=strategy, createdon=createdon, bs=each.bs, expiry=each.expiry, strike=each.strike, cepe=each.cepe,lots=each.lots, entry=active.all()[0].entry, price=active.all()[0].price, pnl=pnl)
        elif activelots==eachlots:
          active.update(active=False)
        elif activelots<eachlots:
          active.update(active=False)
          positions.objects.create(token=each.token, strategy=strategy, createdon=createdon, bs=each.bs, expiry=each.expiry, strike=each.strike, cepe=each.cepe,lots=eachlots-activelots, entry=each.price)
    else:
      positions.objects.create(token=each.token, strategy=strategy, createdon=createdon, bs=each.bs, expiry=each.expiry, strike=each.strike, cepe=each.cepe,lots=each.lots, entry=each.price)
  builder.objects.filter(strategy=strategy, createdon=createdon).delete()
  return JsonResponse({"messages":"true",})

def positionmodify(request, token, action, value):
  inviewdata=inview.objects.all()
  strategy=inviewdata[0].strategy
  createdon=inviewdata[0].createdon
  active=positions.objects.filter(token=token, strategy=strategy, createdon=createdon, active=True)

  if action=="stoploss":
    active.update(stoploss=float(value))

  elif action=="squareoff":
    if int(active.all()[0].lots)==int(value):
      active.update(active=False)
    elif int(active.all()[0].lots>int(value)):
      active.update(lots= int(active.all()[0].lots)-int(value))
      if active.all()[0].bs=="B":
        pnl=(float(active.all()[0].entry)-float(active.all()[0].price))*int(value)
      elif active.all()[0].bs=="S":
        pnl=(float(active.all()[0].price)-float(active.all()[0].entry))*int(value)
      positions.objects.create(active=False, token=token, strategy=strategy, createdon=createdon, bs=active.all()[0].bs, expiry=active.all()[0].expiry, strike=active.all()[0].strike, cepe=active.all()[0].cepe,lots=active.all()[0].lots, entry=active.all()[0].entry, price=active.all()[0].price, pnl=pnl)
  elif action=="squareoffall":
    positions.objects.filter(strategy=strategy, createdon=createdon, active=True).update(active=False)
  return JsonResponse({"messages":"true",})

def trademodify(request, id, strategy, expiry, action):
  createdon=positions.objects.filter(id=int(id)).all()[0].createdon
  if action=="delete":
    positions.objects.filter(createdon=createdon, strategy=strategy, expiry=expiry).delete()
  elif action=="archive":
    positions.objects.filter(createdon=createdon, strategy=strategy, expiry=expiry).update(archived=True)
  return JsonResponse({"messages":"true",})

def dashboardmodify(request, maxprofit, maxloss, breakeven1, breakeven2):
  rrr=round(float(maxprofit)/abs(float(maxloss)), 2)
  dashboard.objects.filter(id=1).update(maxprofit=round(float(maxprofit), 2), maxloss=round(float(maxloss), 2), breakeven1=round(float(breakeven1)), breakeven2=round(float(breakeven2)), rrr=rrr)
  
