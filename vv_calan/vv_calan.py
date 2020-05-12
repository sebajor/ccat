import corr
import time,os
import telnetlib
from plot_snapshot import snapshot
from powerpc import PPC_upload_code, PPC_start_measure,PPC_download_data, PPC_kill_process
from parse_raw import parse_raw


class vv_calan(object):
    def __init__(self, roachIP, bof_path, valon_freq):
        """ Class constructor
            valon freq is the actual frequency of the valon,
            not the sampling frequency.
            ##Remember the sampling frequency is the double
            of the valon frequency
        """
        self.IP = roachIP
        self.bof = bof_path
        self.valon_freq = valon_freq
        self.fpga_clk = valon_freq/8.
        self.bw = self.fpga_clk/2       #this is the bw after the decimation
        self.fpga = corr.katcp_wrapper.FpgaClient(self.IP)
        self.fft_size = 2**14
        self.channels = 2**13
        self.n_acc = 10

    def upload_bof(self):
        """Upload the bof file to the ROACH
        """
        self.fpga.upload_program_bof(self.bof, 3000)
        time.sleep(1)


    def set_integ_time(self, integ_time=1.2*10**-3):
        """Set integration time 
           integ_time = imtegration time in seconds
        """    
        chann_period = 2.**14/(self.fpga_clk*10**6) #
        self.n_acc = int(integ_time/chann_period)+1
        if(self.n_acc>2**14-2):
            print("The accumulation could overflow, carefull look at the spectrum..") 
        self.fpga.write_int('acc_len',self.n_acc)
        self.fpga.write_int('cnt_rst',1)
        self.fpga.write_int('cnt_rst',0)
        print("integration time set to: %.4f [ms]"%(self.n_acc*chann_period*10**3))


    def init_vv(self, integ_time=1.2*10**-3):
        """initialize the vector voltmeter registers
        """
        self.fpga.write_int('cnt_rst',1)
        self.set_integ_time(integ_time)
        self.fpga.write_int('cnt_rst',0)
        
    def init_timestamp(self, unlock_error=10**-4):
        """initialize the timestamp model
            unlock_error = the varition in seconds to rise an
            unlock flag
        """
        T = 10**-2 #bit time of IRIGB00
        sec_factor = 0.75                               #security factor (could be higher, but this value works..)
        irig_pos_id = 0.8*T*self.fpga_clk*10**6*sec_factor
        irig_1 = 0.5*T*self.fpga_clk*10**6*sec_factor
        irig_0 = 0.2*T*self.fpga_clk*10**6*sec_factor
        
        print('writing timestamp variables.....')
        
        #those are the durations of every symbol in IRIG
        self.fpga.write_int('IRIG_irig_pos_id', irig_pos_id)
        self.fpga.write_int('IRIG_irig_1', irig_1)
        self.fpga.write_int('IRIG_irig_0', irig_0)
    
        
        
        self.fpga.write_int('IRIG_sel_ind',0)           #1 only to debbugg the irig_read fsm
        
        #settings for the debouncer fsm
        self.fpga.write_int('IRIG_waiting_in_vain', 20) #cycles that the gpio values may vary until sets to one
        self.fpga.write_int('IRIG_threshold', 20)       #cycles that the gpio values may vary until sets to zero
        self.fpga.write_int('IRIG_top_count', 100)      #the number of symbols of the first data frame, for debbuging only
        self.fpga.write_int('IRIG_bott_count', 100)     #the number of symbols of the dataframe, for debbuging only
        
        
        #set upper and lower limit of seconds that the timestamp
        #could vary to rise the flag of unlocking
        self.fpga.write_int('IRIG_frec_uplim', int(self.fpga_clk*10**6*(1+unlock_error)))   
        self.fpga.write_int('IRIG_frec_downlim', int(self.fpga_clk*10**6*(1-unlock_error))) 
        
        ##with the previous registers set up, we obtain the time from the master clock
        self.calibrate_timestamp()
    
    
    
    def calibrate_timestamp(self):
        """Get the time from the master clock
         This function enable obtain the time from the master clock
        """
        #reset the fsm to a known state
        self.fpga.write_int('IRIG_hrd_rst', 1)
        time.sleep(1)
        self.fpga.write_int('IRIG_hrd_rst', 0)
            
        #start the calibration
        self.fpga.write_int('IRIG_cal',1)
        time.sleep(1)
        self.fpga.write_int('IRIG_cal',0)
            
        #wait until the first frame is detected and received
        print('waiting for the master clock data...')
        time.sleep(3)
        for i in range(5):
            time.sleep(1)
            aux = self.fpga.read_int('IRIG_terminate')
            if(aux == 1):
                break
            
        if(i==4):
            print('There might be a problem..its everything connected?')
            ans = raw_input('Do you want to try the calibration again?(y/n)')
            if(ans=='y' or ans=='yes'):
                self.calibrate_timestamp()
            else:
                return
        else:
            #The first second is always over the upper lim, and the second its always below the lower lim because
                # the fraction counter initialize only when the calibration is over. 
                #From the third second the system is stable, so we rest the unlock flag.
            time.sleep(3)
            self.fpga.write_int('IRIG_try_again',1)
            self.fpga.write_int('IRIG_try_again',0)
                 
            print('Timestamp calibration finished :D')
    
    
    def get_hour(self):
        """Translate the time from seconds of a year
        to day/hour/minutes/seconds
        """
        toy = self.fpga.read_int('secs')
        days = int(toy/(24.*3600))
        hours =int((toy%(24.*3600))/3600)
        minutes = int((toy%(24.*3600)%3600)/60)
        secs = toy%(24.*3600)%3600%60
        out = str(days)+'day'+str(hours)+':'+str(minutes)+':'+str(secs)
        print(out)
        return out


    def get_unlock(self):
        """ return 1 if the timestamp is unlocked
            return 0 if the timestamp is locked
        """
        out = self.fpga.read_int('unlock')
        return out


    def adc_snapshot(self):
        """Plot animation of the ADC snapshot
        """
        snapshot(self.fpga)
    

    def ppc_upload_code(self, file_path='ppc_save'):
        """Upload the required files to the ppc in the ROACH
        We connect through telnet to the 
        """
        PPC_upload_code(self.IP, file_path)
     

    
    def ppc_meas(self, chann=6068 ,duration=30):
        """Measure and save the data in the PowerPC in the roach
           duration=time of the complete measure, in minutes 
        """
        ###TODO: check if some registers must be cleaned before...
        self.fpga.write_int('addr2catch', chann)                       #select the channel to save in the ppc
        bram_addr = 8192.
        bram_period = self.fft_size*bram_addr*self.n_acc/(self.fpga_clk*10**6)*2 #we have two banks
        self.__read_cycles__ = int(duration*60./bram_period)
        self.__pid__ = PPC_start_measure(self.IP,self.__read_cycles__)
        print("PID of the process: "+str(self.__pid__))
        
                

    def ppc_download_data(self, pc_IP):
        """Download the saved data to a computer
        """
        PPC_download_data(self.IP, pc_IP)
        

    def ppc_finish_meas(self):
        """Finish the measurement before measure duration has 
           elapsed
        """
        PPC_kill_process(self.IP, self.__pid__)



    def parse_raw_data(self, filename='raw_data', n_reading=None):
        """
        Parse the raw data after downloading the data from the 
        PowerPC and save it in hdf5 format.
        """
        if(n_reading==None):
            parse_raw(filename, self.read_cycles*2)
        else:
            parse_raw(filename, n_reading)

        

    def calibration(self, load=0, man_gen=0, ip_gen='192.168.1.33', filename='cal'):
        """This function makes the calibration of the ROACH more 
        understandable; you have to had installed the package 
        calandigital (https://github.com/FrancoCalan/calandigital)
        if you only want to make mcmm set load at 1
        if you want to manually set the generator set man_gen=1
        ip_gen = generator IP, to use in this mode the generator must
                 support visa commands
        filename = if load=1 the load dir, if load=0 the saving dir


            -Sidenote: a common failure is to set bad the bw and it throws
            an error of representation
        """
        parameter = "calibrate_adc5g.py"
        parameter += " -i "+str(self.IP)
        if(man_gen==0):
            parameter += " -g "+str(ip_gen)
            parameter += " -gf "+str(10)
            parameter += " -gp "+str(-3)
        parameter += " -psn -psp"
        parameter += " -bw "+str(self.valon_freq)
        parameter += " -s0 adcsnap0"
        parameter += " -s1 adcsnap1"
        parameter += " -ns 1000"
        if(load==0):
            parameter += " -dm -di -do"
            parameter += " -cd "+str(filename)
        if(load==1):
            parameter += " -dm -li -lo"
            parameter += " -ld "+str(filename)
        print(parameter)    
        os.system(parameter)



    def set_valon_freq(self, new_freq, port=1):
        """
        To use this function is necessary to be connected 
        to the USB port of the valon
        new freq: Its the sampling frequency of the ADC's
        port: which port we are programming, 0 means A and 1 means B
        ##The actual sampling frequency is the double of new_freq
        beacause the ADC take a sample at the rising and falling edge
    
        After changing the clock you should reset the vector voltmeter
        register and re-calibrate the timestamp.

        #If you have some problem change the tty in the adc_clock script
        """
        parameter = "python adc_clock.py -f" + str(int(new_freq/2))
        if(port):
            parameter += ' -s B'
            os.system(parameter)
            self.valon_freq = new_freq
            self.fpga_clk = self.valon_freq/8
            self.bw = self.fpga_clk/2
        else:
            parameter += ' -s A'
            os.system(parameter)


    def synchronization(self):
        ##TODO...
        return    


    def get_sampling_freq(self):
        """Returns the sampling frequency at the ADC
        """
        return self.valon_freq*2

    
    def get_fpga_clock(self):
        """Return the fpga clock, this is twice of
            the usefull bandwidth.
        """
        return self.fpga_clk






