import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcol

color_dict = mcol.TABLEAU_COLORS


def lin2db(x):
    return 10*np.log10(x)


def db2lin(x):
    return 10**(x/10)


class ADC:
    fs_step = 2.75625e3
    def __init__(self, n_bit):
        self.n_bit = n_bit

    def snr(self, flag):
        try:
            t = len(self.n_bit)
            snr = []
            for i in range(t):
                x = 6*self.n_bit[i]
                if flag != 1:
                    x = 10**(x/10)
                snr.append(x)
            return snr
        except:
            OSError()
            snr = 6*self.n_bit
            return snr
    
    def sf(self, bandwidth):
        sf = np.ceil(2 * ADC.fs_step * bandwidth / ADC.fs_step)
        return sf
    
class BSC:
    def __init__(self, error_probability):
        self.error_probability = error_probability

    def snr(self, flag):
        try:
            t = len(self.error_probability)
            snr = []
            for i in range(t):
                x = 1/(4 * self.error_probability[i])
                if flag == 1:
                    x = 10 * np.log10(x)
                snr.append(x)
            return snr
        except:
            OSError()
            t = 1
            snr = 1/(4 * self.error_probability[i])
            return snr

class PCM:

    def __init__(self, analog_bandwidth, adc, bsc):
        self.analog_bandwidth = analog_bandwidth
        self.adc = adc
        self.bsc = bsc
    
    def snr(self):
        snrs = []
        for i in range(len(self.adc.n_bit)):
            a = self.adc.snr(2)
            b = self.bsc.snr(2)
            snr = []
            for k in range(len(b)):
                x = 1 / (1/a[i] + 1/b[k])
                x = 10 * np.log10(x)
                snr.append(x)
            snrs.append(snr)
        return snrs

    def critical_pe(self):
        critical_pe = []
        for i in range(len(self.adc.n_bit)):
            critical_pe.append(1 / (4* (4**self.adc.n_bit[i])))
        return critical_pe
    
    def transmission(self):
        p = self.bsc.error_probability
        c = 1 + p*np.log2(p) + (1 - p)*np.log2(1 - p)
        n = self.adc.n_bit
        k = self.adc.sf(self.analog_bandwidth)
        r  = n * k
        if r <= c :
            print("Supported transmission")
        else:
            print("Transmission not supported")

def n_bit_pcm(snr, p_e):
    n_bit = np.sqrt((snr-4*p_e*snr)/(1-4*p_e*snr))
    n_bit = np.ceil(n_bit)
    return n_bit


def plotting(snr, critical_pe, quant, p_e):
    fig, axs = plt.subplots(2, 2, subplot_kw={'xscale': 'log', 'xlabel' : 'log(Error Probability)', 'ylabel' : 'SNR / dB'})
    for i in range(2):
        for j in range(2):
            axs[i][j].plot(p_e, snr[2*i+j], color="blue")
            axs[i][j].axhline(quant[2*i+j], color = "red")
            axs[i][j].axvline(critical_pe[2*i+j], color = "green")


def exercise_1():
    n_bit = [2, 3, 4, 6, 8, 10, 12, 14, 16]
    p_e = []
    i  =1e-12
    while i <= 1:
        p_e.append(i)
        i += 0.001
    p_e.append(1)

    x = ADC(n_bit)
    plt.plot(x.n_bit, x.snr(1))
    plt.xlabel("n_bit")
    plt.ylabel("SNR / dB")
    plt.show()

    y = BSC(p_e)
    plt.plot(y.error_probability, y.snr(1))
    plt.xscale("log")
    plt.xlabel("log(Error probability)")
    plt.ylabel("SNR / dB")
    plt.show()
     

def exercise_2():
    n_bit = [2, 4, 8, 16]
    p_e = []
    badnwidth = 22e3
    p_e = np.logspace(-12, 0, 500)

    x = ADC(n_bit)
    y = BSC(p_e)
    z = PCM(badnwidth, x, y)
    
    snr = z.snr()
    critical_pe = z.critical_pe()
    quant = x.snr(1)

    plotting(snr, critical_pe, quant, p_e)
    plt.show()


def exercise_3():
    badnwidth = 22e3
    p_e = 3.8e-7
    snr = 80
    n_bit = n_bit_pcm(snr, p_e)
    
    x = ADC(n_bit)
    y = BSC(p_e)
    z = PCM(badnwidth, x, y)

    print("Obtained n_bit of the ADC are:", z.adc.n_bit)
    print("SNR corresponding to obtained n_bit: ", z.adc.snr(1), "DB", sep = "")
    z.transmission()

if __name__ == "__main__":
    print("Laboratory 3 - ADC-BSC")
    
    exercise_1()
    exercise_2()
    exercise_3()
