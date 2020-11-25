# W251 HW13 Deep Learning SDK
<br><br>
Epoch=100, batch-size=8 <br>
Train time: 10 hrs<br>
Final accuracy top1: 56.211<br>
Final accuracy top5: 86.344<br>
<br><br>
Epoch=100, batch-size=16<br>
Train time: 8.5 hrs<br>
Final accuracy top1: 56.388<br>
Final accuracy top5: 87.753<br>
<br><br>
Batch size was able to be increased, as TX2 memory is sufficient to compute large matrices. There is a modes increase in accuracy, suggesting that higher batch size is helping keep the model from overfitting.
