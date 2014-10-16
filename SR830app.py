# -*- coding: utf-8 -*-
"""
Created on Tue Oct 07 10:39:34 2014

@author: afeldman
"""
import sys,os,thread,time
import numpy as np
from PyQt4 import QtCore, QtGui
from parse import *

import SR830gui
import SR830

add="GPIB0::14"
lockin=SR830.device(add)

app = QtGui.QApplication(sys.argv)

def update():
    myapp.data.x.append(lockin.get_X())
    myapp.data.y.append(lockin.get_Y())
    
    myapp.Channel1.display('{:.2E}'.format(myapp.data.x[-1]))
    myapp.Channel2.display('{:.2E}'.format(myapp.data.y[-1]))

    refsel=myapp.reference.currentIndex()
    if refsel==0:
        myapp.data.phase.append(lockin.get_phase())
        myapp.Ref.display('{:.2f}'.format(myapp.data.phase[-1]))
    elif refsel==1:
        myapp.data.freq.append(lockin.get_freq())
        myapp.Ref.display('{:.2f}'.format(myapp.data.freq[-1]))
    elif refsel==2:
        myapp.data.ampl.append(lockin.get_ampl())
        myapp.Ref.display('{:.2f}'.format(myapp.data.ampl[-1]))
    elif refsel==3:
        myapp.data.harm.append(lockin.get_harm())
        myapp.Ref.display('{:.2f}'.format(myapp.data.harm[-1]))

    
class SR830dialog(QtGui.QDialog, SR830gui.Ui_Dialog):
    def __init__(self, parent=None):
        super(SR830dialog,self).__init__(parent)
        self.setupUi(self)
        self.running=False
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(update)
        
        self.data=SRdata()
        self.settings=SRsettings()
        
        self.getsettings()

        self.startmeas()
    
    def startmeas(self):
		if not self.running :
			self.timer.start(200)
			self.running  = True
		else:
			self.timer.stop()
			self.running  = False

		print 'Measuring....'    

    def getsettings(self):
        self.settings.sens=lockin.get_sens()
        self.settings.tau=lockin.get_tau()
        self.settings.slope=lockin.get_slope()
        self.settings.sync=lockin.get_sync()
        self.settings.input=lockin.get_input()
        self.settings.couple=lockin.get_couple()
        self.settings.ground=lockin.get_ground()
        self.settings.filter=lockin.get_filter()
        self.settings.reserve=lockin.get_reserve()
        tempdisprat=lockin.get_disp_rat(1)
        self.settings.ch1disp=tempdisprat.split(',')[0]
        self.settings.ch1ratio=tempdisprat.split(',')[1]
        tempexpoff=lockin.get_exp_off(1)
        self.settings.ch1expand=tempexpoff.split(',')[0]
        self.settings.ch1offset=tempexpoff.split(',')[1]
        tempdisprat=lockin.get_disp_rat(2)
        self.settings.ch2disp=tempdisprat.split(',')[0]
        self.settings.ch2ratio=tempdisprat.split(',')[1]
        tempexpoff=lockin.get_exp_off(2)
        self.settings.ch2expand=tempexpoff.split(',')[0]
        self.settings.ch2offset=tempexpoff.split(',')[1]        
        self.settings.trigsource=lockin.get_trigsource()
        self.settings.trigshape=lockin.get_trigshape()    
  
        #set GUI to match settings  
        senstext=self.settings.sensset.get(int(self.settings.sens))
        sensval,sensunit=parse('{:d}{}',senstext)
        self.sensunit.setCurrentIndex(self.sensunit.findText(sensunit))
        self.sensval.setCurrentIndex(self.sensval.findText(str(sensval)))
        tautext=self.settings.tauset.get(int(self.settings.tau))
        tauval,tauunit=parse('{:d}{}',tautext)
        self.tauunit.setCurrentIndex(self.tauunit.findText(tauunit))
        self.tauval.setCurrentIndex(self.tauval.findText(str(tauval)))
        self.slopeval.setCurrentIndex(int(self.settings.slope))
        self.synccheck.setCheckState(int(self.settings.sync)*2)
        self.input.setCurrentIndex(int(self.settings.input))
        self.coupling.setCurrentIndex(int(self.settings.couple))
        self.ground.setCurrentIndex(int(self.settings.ground))
        self.filterset.setCurrentIndex(int(self.settings.filter))
        self.reserveset.setCurrentIndex(int(self.settings.reserve))
        self.ch1_disp.setCurrentIndex(int(self.settings.ch1disp))
        self.ch1_ratio.setCurrentIndex(int(self.settings.ch1ratio))
        self.ch1_offset.setCurrentIndex(int(self.settings.ch1offset))
        self.ch1_expand.setCurrentIndex(int(self.settings.ch1expand))
        self.ch2_disp.setCurrentIndex(int(self.settings.ch2disp))
        self.ch2_ratio.setCurrentIndex(int(self.settings.ch2ratio))
        self.ch2_offset.setCurrentIndex(int(self.settings.ch2offset))
        self.ch2_expand.setCurrentIndex(int(self.settings.ch2expand))
        self.trigshape.setCurrentIndex(int(self.settings.trigshape))
        self.trigsource.setCurrentIndex(int(self.settings.trigsource))
        
        
    def autophase(self):
        if self.running : self.timer.stop()
        lockin.auto_phase()
        if self.running : self.timer.start(200)
    def autogain(self):
        if self.running : self.timer.stop()
        lockin.auto_gain()
        if self.running : self.timer.start(200)
    def autoreserve(self):
        if self.running : self.timer.stop()
        lockin.auto_reserve()
        if self.running : self.timer.start(200)
    def setRef(self):
        curval=float(self.newrefval.text())
        refsel=myapp.reference.currentIndex()
        if refsel==0:
            lockin.set_phase(curval)
        elif refsel==1:
            pass
        elif refsel==2:
            lockin.set_ampl(curval)
        elif refsel==3:
            lockin.set_harm(curval)    
    def phaseplus(self):
        curphase=lockin.get_phase()
        newphase=curphase+90
        lockin.set_phase(newphase)
    def phasemin(self):
        curphase=lockin.get_phase()
        newphase=curphase-90
        lockin.set_phase(newphase)
    def chgtau(self):
        temptau=str(self.tauval.currentText())+str(self.tauunit.currentText())
        if temptau in self.settings.tauset.values():
            for i in self.settings.tauset:
                if temptau==self.settings.tauset[i]:
                    newtau=i
                    lockin.set_tau(newtau)
        else:
            print "not in set"
    def chgsens(self):
        tempsens=str(self.sensval.currentText())+str(self.sensunit.currentText())
        if tempsens in self.settings.sensset.values():
            for i in self.settings.sensset:
                if tempsens==self.settings.sensset[i]:
                    newsens=i
                    lockin.set_sens(newsens)
        else:
            print "not in set"
    def chgres(self):
        lockin.set_reserve(self.reserveset.currentIndex())
    def chgslope(self):
        lockin.set_slope(self.slopeval.currentIndex())
    def chgsync(self):
        if self.synccheck.checkState()==2:
            state=1
        else:
            state=0
        lockin.set_sync(state)
    def selinput(self):
        lockin.set_input(self.input.currentIndex())
    def selcoup(self):
        lockin.set_couple(self.coupling.currentIndex())
    def selgnd(self):
        lockin.set_ground(self.ground.currentIndex())
    def chgfilt(self):
        lockin.set_filter(self.filterset.currentIndex())
    def chgch1disp(self):
        lockin.set_disp_rat(1,self.ch1_disp.currentIndex(),self.ch1_ratio.currentIndex())
    def chgch1ratio(self):
        lockin.set_disp_rat(1,self.ch1_disp.currentIndex(),self.ch1_ratio.currentIndex())
    def chgch1expand(self):
        lockin.set_exp_off(1,self.ch1_offset.currentIndex(),self.ch1_expand.currentIndex())
    def chgch1offset(self):
        lockin.set_exp_off(1,self.ch1_offset.currentIndex(),self.ch1_expand.currentIndex())
    def chgch2disp(self):
        lockin.set_disp_rat(2,self.ch2_disp.currentIndex(),self.ch2_ratio.currentIndex())
    def chgch2ratio(self):
        lockin.set_disp_rat(2,self.ch2_disp.currentIndex(),self.ch2_ratio.currentIndex())
    def chgch2expand(self):
        lockin.set_exp_off(2,self.ch2_offset.currentIndex(),self.ch2_expand.currentIndex())
    def chgch2offset(self):
        lockin.set_exp_off(2,self.ch2_offset.currentIndex(),self.ch2_expand.currentIndex())
    def chgtrigshape(self):
        lockin.set_trigshape(self.trigshape.currentIndex())
    def chgtrigsource(self):
        lockin.set_trigsource(self.trigsource.currentIndex())

class SRdata:
    def __init__(self):
        self.x=[]
        self.y=[]
        self.r=[]
        self.theta=[]
        self.phase=[]
        self.freq=[]
        self.ampl=[]
        self.harm=[]
        
        
class SRsettings:
    def __init__(self):
        self.sens=0
        self.tau=0
        self.slope=0
        self.sync=0
        self.input=0
        self.couple=0
        self.ground=0
        self.filter=0
        self.reserve=0
        self.ch1disp=0
        self.ch1ratio=0
        self.ch1expand=0
        self.ch1offset=0
        self.ch2disp=0
        self.ch2ratio=0
        self.ch2expand=0
        self.ch2offset=0        
        self.trigshape=0
        self.samplerate=0
        self.trigsource=0
        
        self.tauset={
                0 : "10mus",
                1 : "30mus",
                2 : "100mus",
                3 : "300mus",
                4 : "1ms",
                5 : "3ms",
                6 : "10ms",
                7 : "30ms",
                8 : "100ms",
                9 : "300ms",
                10 : "1s",
                11 : "3s",
                12 : "10s",
                13 : "30s",
                14 : "100s",
                15 : "300s",
                16 : "1ks",
                17 : "3ks",
                18 : "10ks",
                19 : "30ks"}
        self.sensset={
                0 : "2nV",
                1 : "5nV",
                2 : "10nV",
                3 : "20nV",
                4 : "50nV",
                5 : "100nV",
                6 : "200nV",
                7 : "500nV",
                8 : "1muV",
                9 : "2muV",
                10 : "5muV",
                11 : "10muV",
                12 : "20muV",
                13 : "50muV",
                14 : "100muV",
                15 : "200muV",
                16 : "500muV",
                17 : "1mV",
                18 : "2mV",
                19 : "5mV",
                20 : "10mV",
                21 : "20mV",
                22 : "50mV",
                23 : "100mV",
                24 : "200mV",
                25 : "500mV",
                26 : "1V"}
        

myapp=SR830dialog()

myapp.show()
app.exec_()
