import csv
import numpy as np
import matplotlib.pyplot as plt
import cv2
import biosppy


name = '1.csv'
name2 = 'sample1.csv'
directory ='samples'

#read first record CSV
csv_data = np.loadtxt(name, delimiter=',')
data = np.array(csv_data)
signals = []
count = 1
count2=1
#find QRS peaks
peaks =  biosppy.signals.ecg.christov_segmenter(signal=data, sampling_rate = 125)[0]
#second file will have the signal cut by beats, window size - half the measure of the QRS peaks
with open(name2,'w') as writer:
    wtr = csv.writer(writer)
    for i in (peaks[1:-1]):
        diff1 = abs(peaks[count - 1] - i)
        diff2 = abs(peaks[count + 1]- i)
        x = peaks[count - 1] + diff1//2
        y = peaks[count + 1] - diff2//2
        signal = data[x:y]
        signals.append(signal)
        wtr.writerow(signal)
        count += 1

        fig = plt.figure(frameon=False)
        plt.plot(signal)
        plt.xticks([]), plt.yticks([])
        for spine in plt.gca().spines.values():
          spine.set_visible(False)
        
        #save all images into the samples folder
        filename = directory + '/' + str(count)+'.png'
        fig.savefig(filename)
        im_gray = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(filename, im_gray)
        count2 += 1
print(signals)
