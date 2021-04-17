from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Sum, Subquery, OuterRef, Avg
from django.db import connection
from ..models import lck_2021, lck_2021_spring_player
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np



def scout_report(request, player_nick):
    """
    주력
    """
    player=lck_2021.objects.filter(nickname=player_nick).values().first()
    play_count=lck_2021.objects.filter(nickname=player_nick).values().count()
    KDA=lck_2021.objects.filter(nickname=player_nick).aggregate(total_kill=Sum('kill'),total_death=Sum('death'),total_assist=Sum('assist'),KDA=((Sum('kill')+Sum('assist'))/Sum('death')),KDA_2=(((Sum('kill')+Sum('assist'))%Sum('death')))*100/Sum('death'), win_rate=Avg('win')*100)
    grow=lck_2021.objects.filter(nickname=player_nick).aggregate(CS=Avg('CS'),gold=Avg('Golds'))
    vision=lck_2021.objects.filter(nickname=player_nick).aggregate(vision_scord=Avg('Vision_Scord'), wards_place=Avg('Wards_place'), Wards_destroyed=Avg('Wards_destroyed'), control_ward_purchased=Avg('control_ward_purchased'))
    fight=lck_2021.objects.filter(nickname=player_nick).aggregate(damage=Avg('Total_damage_to_champion'), DPM=Avg('DPM'))
    line=lck_2021.objects.filter(nickname=player_nick).aggregate(GD15=Avg('GD15'), CSD15=Avg('CSD15'), XPD15=Avg('XPD15'), LVLD15=Avg('LVLD15'))
    others=lck_2021.objects.filter(nickname=player_nick).aggregate(CC=Avg('Time_ccing_others'), taken_damage=Avg('Total_damage_taken'))
    most=lck_2021.objects.values_list('champion').filter(nickname=player_nick).annotate(most_champion=Count('champion')).order_by('-most_champion')[:5]
    """TEST"""

    CS=list(lck_2021.objects.filter(nickname=player_nick).values_list('CS'))
    CSM=list(lck_2021.objects.filter(nickname=player_nick).values_list('CSM'))
    CS_sum=lck_2021.objects.filter(nickname=player_nick).values_list().aggregate(CS_sum=Sum('CS'))
    a=[]
    for i in range(0,len(CS)):
        a.append(CS[i][0]/CSM[i][0])
        time=sum(a)
    CS_M=CS_sum['CS_sum']/time
    Gold_sum=lck_2021.objects.filter(nickname=player_nick).values_list().aggregate(Golds_sum=Sum('Golds'))
    Gold_M=Gold_sum['Golds_sum']/time
    Damage_sum=lck_2021.objects.filter(nickname=player_nick).values_list().aggregate(damage_sum=Sum('Total_damage_to_champion'))
    Damage_M=Damage_sum['damage_sum']/time

    personid=list(lck_2021.objects.filter(nickname=player_nick).values_list('id'))
    teamid=[]
    for i in range(0,len(personid)):
        for j in range(0,5):
            teamid.append(int(personid[i][0]/5)*5+1+j)
    teamgold=[]
    for i in teamid:
        teamgold.append(lck_2021.objects.values_list('Golds').filter(id=i))
    teamgolds=0
    for i in range(0,len(teamgold)):
        teamgolds+=teamgold[i][0][0]
    persongold=lck_2021.objects.filter(nickname=player_nick).aggregate(persongold=Sum('Golds'))
    GOLDp=list(persongold.values())[0]/teamgolds*100
    teamdamage=[]
    for i in teamid:
        teamdamage.append(lck_2021.objects.values_list('Total_damage_to_champion').filter(id=i))
    teamdamages=0
    for i in range(0,len(teamdamage)):
        teamdamages+=teamdamage[i][0][0]
    persondamage=lck_2021.objects.filter(nickname=player_nick).aggregate(persondamage=Sum('Total_damage_to_champion'))
    DMGp=list(persondamage.values())[0]/teamdamages*100
    teamKA=[]
    for i in teamid:
        teamKA.append(lck_2021.objects.values_list('kill').filter(id=i))
    teamKA_2=0
    for i in range(0,len(teamKA)):
        teamKA_2+=teamKA[i][0][0]
    KAp=(list(KDA.values())[0]+list(KDA.values())[2])/teamKA_2*100
    KAm=(list(KDA.values())[0]+list(KDA.values())[2])/time
    mo_win=[]
    m5=lck_2021.objects.filter(nickname=player_nick).values('champion').annotate(count=Count('champion'))[:5]

    for i in range(0,len(m5)):
        mo_win.append(lck_2021.objects.filter(nickname=player_nick,champion=list(most)[i][0]).aggregate(win_rate=Avg('win')*100))

    DWG=[]
    NS=[]
    FreditBrion=[]
    DragonX=[]
    Afreeca=[]
    HLE=[]
    GenG=[]
    T1=[]
    KT=[]
    LSB=[]
    db=lck_2021.objects.values()
    db_2=lck_2021_spring_player.objects.values()
    c=[]
    for i in range(0,len(db)):
        if db[i]['nickname']==player_nick:
            if i%10 < 5:
                c=db[i+5]['nickname']
                for j in range(0,len(db_2)):
                    if c==db_2[j]['nickname']:
                        d=db_2[j]['team']
                        if d=='DWG':
                            DWG.append(db[i])
                        elif d=='NS':
                            NS.append(db[i])
                        elif d=='FreditBrion':
                            FreditBrion.append(db[i])
                        elif d=='DragonX':
                            DragonX.append(db[i])
                        elif d=='Afreeca':
                            Afreeca.append(db[i])
                        elif d=='HLE':
                            HLE.append(db[i])
                        elif d=='GenG':
                            GenG.append(db[i])
                        elif d=='T1':
                            T1.append(db[i])
                        elif d=='KT':
                            KT.append(db[i])
                        elif d=='LSB':
                            LSB.append(db[i])


            elif i%10 >=5:
                c=db[i-5]['nickname']
                for j in range(0,len(db_2)):
                    if c==db_2[j]['nickname']:
                        d=db_2[j]['team']
                        if d=='DWG':
                            DWG.append(db[i])
                        elif d=='NS':
                            NS.append(db[i])
                        elif d=='FreditBrion':
                            FreditBrion.append(db[i])
                        elif d=='DragonX':
                            DragonX.append(db[i])
                        elif d=='Afreeca':
                            Afreeca.append(db[i])
                        elif d=='HLE':
                            HLE.append(db[i])
                        elif d=='GenG':
                            GenG.append(db[i])
                        elif d=='T1':
                            T1.append(db[i])
                        elif d=='KT':
                            KT.append(db[i])
                        elif d=='LSB':
                            LSB.append(db[i])
    all=[]
    all.append(DWG)
    all.append(NS)
    all.append(FreditBrion)
    all.append(DragonX)
    all.append(Afreeca)
    all.append(HLE)
    all.append(GenG)
    all.append(T1)
    all.append(KT)
    all.append(LSB)
    DWG2=[]
    NS2=[]
    FreditBrion2=[]
    DragonX2=[]
    Afreeca2=[]
    HLE2=[]
    GenG2=[]
    T12=[]
    KT2=[]
    LSB2=[]
    for j in range(0,len(all)):
        w_r=[]
        k=[]
        d=[]
        a=[]
        if j==0:
            for i in range(0,len(all[j])):
                w_r.append(all[j][i]['win'])
                k.append(all[j][i]['kill'])
                d.append(all[j][i]['death'])
                a.append(all[j][i]['assist'])
            DWG_play=len(DWG)
            DWG_win_rate=sum(w_r)
            DWG_K=sum(k)
            DWG_D=sum(d)
            DWG_A=sum(a)
        elif j==1:
            w_r=[]
            k=[]
            d=[]
            a=[]
            for i in range(0,len(all[j])):
                w_r.append(all[j][i]['win'])
                k.append(all[j][i]['kill'])
                d.append(all[j][i]['death'])
                a.append(all[j][i]['assist'])
            NS_play=len(NS)
            NS_win_rate=sum(w_r)
            NS_K=sum(k)
            NS_D=sum(d)
            NS_A=sum(a)
        elif j==2:
            w_r=[]
            k=[]
            d=[]
            a=[]
            for i in range(0,len(all[j])):
                w_r.append(all[j][i]['win'])
                k.append(all[j][i]['kill'])
                d.append(all[j][i]['death'])
                a.append(all[j][i]['assist'])

            FreditBrion_play=len(FreditBrion)
            FreditBrion_win_rate=sum(w_r)
            FreditBrion_K=sum(k)
            FreditBrion_D=sum(d)
            FreditBrion_A=sum(a)
        elif j==3:
            w_r=[]
            k=[]
            d=[]
            a=[]
            for i in range(0,len(all[j])):
                w_r.append(all[j][i]['win'])
                k.append(all[j][i]['kill'])
                d.append(all[j][i]['death'])
                a.append(all[j][i]['assist'])

            DragonX_play=len(DragonX)
            DragonX_win_rate=sum(w_r)
            DragonX_K=sum(k)
            DragonX_D=sum(d)
            DragonX_A=sum(a)
        elif j==4:
            w_r=[]
            k=[]
            d=[]
            a=[]
            for i in range(0,len(all[j])):
                w_r.append(all[j][i]['win'])
                k.append(all[j][i]['kill'])
                d.append(all[j][i]['death'])
                a.append(all[j][i]['assist'])

            Afreeca_play=len(Afreeca)
            Afreeca_win_rate=sum(w_r)
            Afreeca_K=sum(k)
            Afreeca_D=sum(d)
            Afreeca_A=sum(a)
        elif j==5:
            w_r=[]
            k=[]
            d=[]
            a=[]
            for i in range(0,len(all[j])):
                w_r.append(all[j][i]['win'])
                k.append(all[j][i]['kill'])
                d.append(all[j][i]['death'])
                a.append(all[j][i]['assist'])

            HLE_play=len(HLE)
            HLE_win_rate=sum(w_r)
            HLE_K=sum(k)
            HLE_D=sum(d)
            HLE_A=sum(a)
        elif j==6:
            w_r=[]
            k=[]
            d=[]
            a=[]
            for i in range(0,len(all[j])):
                w_r.append(all[j][i]['win'])
                k.append(all[j][i]['kill'])
                d.append(all[j][i]['death'])
                a.append(all[j][i]['assist'])

            GenG_play=len(GenG)
            GenG_win_rate=sum(w_r)
            GenG_K=sum(k)
            GenG_D=sum(d)
            GenG_A=sum(a)
        elif j==7:
            w_r=[]
            k=[]
            d=[]
            a=[]
            for i in range(0,len(all[j])):
                w_r.append(all[j][i]['win'])
                k.append(all[j][i]['kill'])
                d.append(all[j][i]['death'])
                a.append(all[j][i]['assist'])

            T1_play=len(T1)
            T1_win_rate=sum(w_r)
            T1_K=sum(k)
            T1_D=sum(d)
            T1_A=sum(a)
        elif j==8:
            w_r=[]
            k=[]
            d=[]
            a=[]
            for i in range(0,len(all[j])):
                w_r.append(all[j][i]['win'])
                k.append(all[j][i]['kill'])
                d.append(all[j][i]['death'])
                a.append(all[j][i]['assist'])

            KT_play=len(KT)
            KT_win_rate=sum(w_r)
            KT_K=sum(k)
            KT_D=sum(d)
            KT_A=sum(a)
        elif j==9:
            w_r=[]
            k=[]
            d=[]
            a=[]
            for i in range(0,len(all[j])):
                w_r.append(all[j][i]['win'])
                k.append(all[j][i]['kill'])
                d.append(all[j][i]['death'])
                a.append(all[j][i]['assist'])
                print(w_r)
            LSB_play=len(LSB)
            LSB_win_rate=sum(w_r)
            LSB_K=sum(k)
            LSB_D=sum(d)
            LSB_A=sum(a)

    DWG2.append(DWG_play)
    DWG2.append(DWG_win_rate)
    DWG2.append(DWG_K)
    DWG2.append(DWG_D)
    DWG2.append(DWG_A)
    NS2.append(NS_play)
    NS2.append(NS_win_rate)
    NS2.append(NS_K)
    NS2.append(NS_D)
    NS2.append(NS_A)
    FreditBrion2.append(FreditBrion_play)
    FreditBrion2.append(FreditBrion_win_rate)
    FreditBrion2.append(FreditBrion_K)
    FreditBrion2.append(FreditBrion_D)
    FreditBrion2.append(FreditBrion_A)
    DragonX2.append(DragonX_play)
    DragonX2.append(DragonX_win_rate)
    DragonX2.append(DragonX_K)
    DragonX2.append(DragonX_D)
    DragonX2.append(DragonX_A)
    Afreeca2.append(Afreeca_play)
    Afreeca2.append(Afreeca_win_rate)
    Afreeca2.append(Afreeca_K)
    Afreeca2.append(Afreeca_D)
    Afreeca2.append(Afreeca_A)
    HLE2.append(HLE_play)
    HLE2.append(HLE_win_rate)
    HLE2.append(HLE_K)
    HLE2.append(HLE_D)
    HLE2.append(HLE_A)
    GenG2.append(GenG_play)
    GenG2.append(GenG_win_rate)
    GenG2.append(GenG_K)
    GenG2.append(GenG_D)
    GenG2.append(GenG_A)
    T12.append(T1_play)
    T12.append(T1_win_rate)
    T12.append(T1_K)
    T12.append(T1_D)
    T12.append(T1_A)
    KT2.append(KT_play)
    KT2.append(KT_win_rate)
    KT2.append(KT_K)
    KT2.append(KT_D)
    KT2.append(KT_A)
    LSB2.append(LSB_play)
    LSB2.append(LSB_win_rate)
    LSB2.append(LSB_K)
    LSB2.append(LSB_D)
    LSB2.append(LSB_A)

    team=lck_2021_spring_player.objects.filter(nickname=player_nick).values_list()
    test=0



    content={'player':player, 'play_count':play_count, 'KDA':KDA, 'grow':grow, 'vision':vision, 'fight':fight, 'line':line, 'others':others, 'most':most, 'CS_M':CS_M, 'CS':CS,'CSM':CSM, 'CS_sum':CS_sum, 'Gold_M':Gold_M, 'Damage_M':Damage_M, 'time':time,
    'personid':personid, 'teamid':teamid, 'teamgold':teamgold, 'test':test, 'GOLDp':GOLDp, 'DMGp':DMGp,
    'teamKA_2':teamKA_2,'KAp':KAp, 'KAm':KAm, 'mo_win':mo_win, 'LSB2':LSB2 ,'DWG2':DWG2, 'NS2':NS2,
    'FreditBrion2':FreditBrion2, 'DragonX2':DragonX2, 'Afreeca2':Afreeca2, 'HLE2':HLE2, 'GenG2':GenG2,
    'T12':T12, 'KT2':KT2 ,'team':team}


    return render(request,'scout/scout_report.html',content)
