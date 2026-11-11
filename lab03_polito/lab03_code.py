import numpy as np
import matplotlib.pyplot as plt

from scipy.special import erfc

class Digital_Signal_Information:
    def __init__(self, signal_power, noise_power, n_bit_mod):
        self.signal_power = signal_power
        self.noise_power = noise_power
        self.n_bit_mod = n_bit_mod
        pass


class line:
    def __init__(self, loss_coefficient, length):
        self.loss_coefficient = loss_coefficient
        self.length = length
        self.loss = loss_coefficient * length
        pass

    def noise_generation(self, signal_power):
        noise_gen = 1e-9 * signal_power * self.length
        return noise_gen

    def snr_digital(self, signal_power):
        snr = 10 * np.log10(signal_power / self.noise_generation(signal_power)) - self.loss
        return snr


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


class PCM:


    def __init__(self, line, adc, digital_singal_information):
        self.adc = adc
        self.line = line
        self.digital_singal_information = digital_singal_information
    
    def snr(self):
        snr = 10**(self.line.snr_digital(self.digital_singal_information.signal_power) / 10)
        return snr
    
    def ber_evaluation(self):
        if self.digital_singal_information.n_bit_mod == 1:
            ber = 1/2 * erfc(np.sqrt(self.snr()))
        elif self.digital_singal_information.n_bit_mod == 2:
            ber = 1/2 * erfc(np.sqrt(1/2 * self.snr()))
        elif self.digital_singal_information.n_bit_mod == 3:
            ber = 2/3 * erfc(np.sqrt(3/14 * self.snr()))
        elif self.digital_singal_information.n_bit_mod == 4:
            ber = 3/8 * erfc(np.sqrt(1/10 * self.snr()))
        return ber



def plotting_1(signal_power, lengths, loss_coefficient, n_bit_mod, n_bit_adc, ber_th):
    fig, axs = plt.subplots(2, 2, subplot_kw={'yscale': 'log', 'xlim': (-1, 30), 'ylim': (1e-30, 0), 'ylabel' : 'log(BER)', 'xlabel' : 'SNR / dB'})
    for i in range(2):
        for j in range(2):
            list = {}
            list["ber"] = []
            list["snr"] = []
            for k in range(len(lengths)):
                adc = ADC(n_bit_adc)
                l = line(loss_coefficient, lengths[k])
                dig = Digital_Signal_Information(signal_power, l.noise_generation(signal_power) , n_bit_mod[2*i + j])
                p = PCM(l, adc, dig)
                list["ber"].append(p.ber_evaluation())
                list["snr"].append(10 * np.log10(p.snr()))
            axs[i][j].plot(list["snr"], list["ber"], color="blue")
            axs[i][j].axhline(ber_th, color = "green")

def plotting_2(signal_power, lengths, loss_coefficient, n_bit_mod, n_bit_adc, ber_th):
    fig, axs = plt.subplots(2, 2, subplot_kw={'yscale': 'log', 'xlim': (5, 120), 'ylim': (1e-30, 0), 'ylabel' : 'log(BER)', 'xlabel' : 'Length / km'})
    for i in range(2):
        for j in range(2):
            list = []
            for k in range(len(lengths)):
                adc = ADC(n_bit_adc)
                l = line(loss_coefficient, lengths[k])
                dig = Digital_Signal_Information(signal_power, l.noise_generation(signal_power) , n_bit_mod[2*i + j])
                p = PCM(l, adc, dig)
                list.append(p.ber_evaluation())
            axs[i][j].plot(lengths, list, color="blue")
            axs[i][j].axhline(ber_th, color = "green")

def main():
    signal_power = 1e-3
    lengths = np.linspace(10, 120, 100)
    loss_coefficient = 0.5
    n_bit_mod = [1, 2, 3, 4]
    n_bit_adc = 6
    ber_th = 1e-2
    plotting_1(signal_power, lengths, loss_coefficient, n_bit_mod, n_bit_adc, ber_th)
    plt.show()
    plotting_2(signal_power, lengths, loss_coefficient, n_bit_mod, n_bit_adc, ber_th)
    plt.show()
main()
