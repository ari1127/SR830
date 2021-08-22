import pyvisa as visa


class device:
    def __init__(self,add="GPIB0::14"):
        self.__ressourceManager=visa.ResourceManager()
        self.device=self.__ressourceManager.open_resource(add)
        # use the right termination characters, defaults don't work correctly
        self.device.read_termination='\n'
        self.device.write_termination='\n'
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
                4 : "50 nV",
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
    
    def reset(self):
        self.device.write('*RST')
    def clear(self):
        self.device.write('*CLS')
    def disable_front_panel(self):
        self.device.write('OVRM 0')
    def enable_front_panel(self):
        self.device.write('OVRM 1')
    def auto_phase(self):
        self.device.write('APHS')
    def auto_gain(self):
        self.device.write('AGAN')
    def auto_reserve(self):
        self.device.write('ARSV')
    def auto_offset(self,channel):
        self.device.write('AOFF %i' % channel )
        
        
    #get settings
    def get_tau(self):
        return self.device.query('OFLT?')
    def get_sens(self):
        return self.device.query('SENS?')
    def get_trigsource(self):
        return self.device.query('FMOD?')
    def get_trigshape(self):
        return self.device.query('RSLP?')
    def get_harm(self):
        return self.device.query('HARM?')
    def get_input(self):
        return self.device.query('ISRC?')
    def get_ground(self):
        return self.device.query('IGND?')
    def get_couple(self):
        return self.device.query('ICPL?')
    def get_filter(self):
        return self.device.query('ILIN?')
    def get_reserve(self):
        return self.device.query('RMOD?')
    def get_slope(self):
        return self.device.query('OFSL?')
    def get_sync(self):
        return self.device.query('SYNC?')
    def get_disp_rat(self,channel):
        return self.device.query('DDEF? %i' % channel)
    def get_exp_off(self,channel):
        return self.device.query('OEXP? %i' % channel)



    #set settings        
    def set_freq(self,freq):
        self.device.write('FREQ %f' % freq )
    def set_ampl(self,ampl):
        self.device.write('SLVL %f' % ampl)
    def set_mode(self,mode):
        self.device.write('FMOD %i' % mode)
    def set_tau(self,tau):
        self.device.write('OFLT %i' % tau)
    def set_sens(self,sens):
        self.device.write('SENS %i' % sens)    
    def set_phase(self,phase):
        self.device.write('PHAS %f' % phase)       
    def set_aux(self,output,value):
        self.device.write('AUXV %(out)i, %(val).3f' % {'out':output,'val':value})
    def set_trigsource(self,ref):
        self.device.write('FMOD %e' % ref)
    def set_trigshape(self, trigshape):
        self.device.write('RSLP %i' % trigshape)        
    def set_disp_rat(self,channel,disp,ratio):
        self.device.write('DDEF %(channel)i, %(disp)i, %(ratio)i'  % {'channel':channel,'disp':disp, 'ratio':ratio})
    def set_exp_off(self,channel,offset,expand):
        self.device.write('OEXP %(channel)i, %(offset)f, %(expand)i'  % {'channel':channel,'offset':offset, 'expand':expand})
    def set_reserve(self,reserve):
        self.device.write('RMOD %i' % reserve)
    def set_filter(self,filt):
        self.device.write('ILIN %i' % filt)
    def set_input(self, inp):
        self.device.write('ISRC %i' % inp)
    def set_ground(self,gnd):
        self.device.write('IGND %i' % gnd)
    def set_couple(self, coup):
        self.device.write('ICPL %i' % coup)
    def set_slope(self,slope):
        self.device.write('OFSL %i' % slope)
    def set_sync(self,sync):
        self.device.write('SYNC %i' % sync)      
        
        
        
    #get data    
    def get_all(self):
        return self.device.query("SNAP?1,2,3,4")
    def get_X(self):
        return float(self.device.query('OUTP? 1'))
    def get_Y(self):
        return float(self.device.query('OUTP? 2'))
    def get_R(self):
        return float(self.device.query('OUTP? 3'))
    def get_Theta(self):
        return float(self.device.query('OUTP? 4'))
    def get_freq(self):
        return float(self.device.query('FREQ?'))   
    def get_ampl(self):
        return float(self.device.query('SLVL?'))        
    def get_phase(self):
        return float(self.device.query('PHAS?'))
    def get_oaux(self,value):
        return float(self.device.query('OAUX? %i' %value))
    def read_aux(self,output):
        return float(self.device.query('AUXV? %i' %output))

        
        
 
              
if (__name__ == '__main__'):
    add="GPIB0::8"
    lockin=device(add)
    #f = open('test.dat','wb');
    data=lockin.get_all()
    x=float(data.split(',')[0])
    y=float(data.split(',')[1])
    r=float(data.split(',')[2])
    theta=float(data.split(',')[3])