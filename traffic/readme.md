The first model I kept basic and followed closely to what was done in the lecture. then I made small changes to see what effect that would have.

Experiment 1: basic model: accuracy .0577%
Experiment 2: changed to average pooling : accuraccy .0563% small - change. Reverting
Experiment 3: changed to 64 filters : accuracy .0550% - change. Reverting
Experiment 4: Normalized input data : accuracy .9479% huge + change. Keeping
Experiment 5: added additional convolutional layer and pooling layer : accuracy .9834% huge + change. Keeping
Experiment 6: reduced dropout to .3 : accuracy .9828%  small - change. reverting
Experiment 7: added additional neurons, now 256 : accuracy .9870%  + change. Keeping
Experiment 8: added additional convolutional layer and pooling layer : accuracy .975%  small - change. reverting
Experiment 9: increased to 20 epochs : accuracy .9913%  small + change. keeping