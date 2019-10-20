from pylab import plot, show, xlabel, ylabel, subplot
from scipy import fft, arange, sin, arctan, pi

sampleCount = 8192          # Sampling Frequency
R = 1000                    # R Ohm
C = 100e-9                  # C Farad
Ts = 1.0 / sampleCount      # sampling interval
freq1 = 1000                # freq Hz input signal
freq2 = 2000                # freq Hz input signal
freq3 = 3000                # freq Hz input signal

inputSignal = [0] * sampleCount
outputSignal = [0] * sampleCount

t = arange(0, 1, Ts)

class LowPassFilter(object):
    def __init__(self, x, R, C, period):
        self.__R = R
        self.__C = C
        self.__T = period
        self.__x = x
        self.__y = [0] * len(x)
        
        self.__K1 = (self.__T / (self.__T + 2 * self.__R * self.__C))
        self.__K2 = (self.__T / (self.__T + 2 * self.__R * self.__C))
        self.__K3 = ((self.__T - 2 * self.__R * self.__C) / (self.__T + 2 * self.__R * self.__C))

    def FilterApply(self):
        for i in range(len(self.__x)):
            self.__y[i] = (self.__x[i] * self.__K1) + (self.__x[i - 1] * self.__K2) - (self.__y[i - 1] * self.__K3)
        return (self.__y)

    def GetFrequency(self):
        return (1 / (2 * pi * self.__R * self.__C))

    def GetWarping(self):
        return (2 / self.__T) * arctan(2 * pi * self.GetFrequency() * self.__T / 2) / (2 * pi)

def plotSpectrum(y, Fs):
    """
    Plots a Single-Sided Amplitude Spectrum of y(t)
    """
    n = len(y)  # length of the signal
    k = arange(n)
    T = n / Fs
    frq = k / T  # two sides frequency range
    frq = frq[range(int(n / 2))]  # one side frequency range

    Y = fft(y) / n  # fft computing and normalization
    Y = Y[range(int(n / 2))]

    plot(frq, abs(Y), 'r')  # plotting the spectrum
    xlabel('Freq (Hz)')
    ylabel('|Y(freq)|')

inputSignal = sin(2 * pi * freq1 * t) + sin(2 * pi * freq2 * t) + sin(2 * pi * freq3 * t)

myFilter = LowPassFilter(inputSignal, R, C, Ts)

outputSignal = myFilter.FilterApply()

print("CutOff Frequency : " + str(myFilter.GetFrequency()))
print("Frequency Warping : " + str(myFilter.GetWarping()))

subplot(2, 1, 1)
plot(t, outputSignal)
xlabel('Time')
ylabel('Amplitude')
subplot(2, 1, 2)
plotSpectrum(outputSignal, sampleCount)
show()
