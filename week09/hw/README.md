# W251 HW09 Submission
#### Adam Sohn
____________

#### 1. How long does it take to complete the training run? 
Using a V100 cluster (4 CPU over 2 nodes), training 50k steps took 23 hrs 46 mins
* Start time: 2/27 0650 
* Finish time: 2/28 0636 
#### 2. Do you think your model is fully trained? How can you tell?
The model is not yet fully trained. Neither Eval_BLEU score nor eval_loss  has yet plateaued. If this is debatable based upon the 50k view, the knowledge of the 300k view confirms this.
#### 3. Were you overfitting?
No. Overfit would occur when BLEU score begins to decrease, which did not occur. Also, overfit is characterized by a departure of the train_loss and eval_loss trends over high step count. This departure did not occur. 
#### 4. Were your GPUs fully utilized?
Mostly. Each GPU was utilized at 100% for most of the time. Periodically, alternating VMs GPUs would reduce utilization to ~ 80%, then return to 100%.
#### 5. Did you monitor network traffic (hint: apt install nmon ) ? Was network the bottleneck?
Yes, network traffic was monitored w/ nmon. There was not an apparent difference in network traffic when GPU was @ 80% Utilization vs. 100% Utilization, so it is not deemed that network was a bottleneck. 
#### 6. Take a look at the plot of the learning rate and then check the config file. Can you explain this setting?
Learn rate is decreasing over time according to settings file entry: 

    "lr_policy": transformer_policy,
    "lr_policy_params": {
    "learning_rate": 2.0,
    "warmup_steps": 8000,
    "d_model": d_model,
    },

`transformer_policy` can be fully seen at https://nvidia.github.io/OpenSeq2Seq/html/_modules/optimizers/lr_policies.html
Transformer policy will start learn rate low and gradually increase learn rate until a warmup steps threshold is reached where learn rate will begin decreasing as a function of steps. This warmup behavior is helpful for tuning attention mechanisms.

#### 8. How big was your training set (mb)? How many training lines did it contain?
Below unix file cmds show that the training set was `1032 MB (de)`, `959 MB (en)`, `4,524,868 lines for each of en/de.` 

	root@v100a:/data/wmt16_de_en# wc -l train.clean.en.shuffled.BPE_common.32K.tok
	4524868 train.clean.en.shuffled.BPE_common.32K.tok
	root@v100a:/data/wmt16_de_en# wc -l train.clean.de.shuffled.BPE_common.32K.tok
	4524868 train.clean.de.shuffled.BPE_common.32K.tok
	root@v100a:/data/wmt16_de_en# 
    
    root@v100a:/data/wmt16_de_en# ls -l --block-size=MB
    ...
    -rw-r--r-- 1 root root 1023MB Feb 26 23:48 train.clean.de.shuffled.BPE_common.32K.tok
    -rw-r--r-- 1 root root  959MB Feb 26 23:48 train.clean.en.shuffled.BPE_common.32K.tok	
#### 9. What are the files that a TF checkpoint is comprised of?
A TF checkpoint is comprised of multiple models at configured step intervals. Note below for checkpoints, including best_models checkpoint.

    less /data/en-de-transformer/best_models/checkpoint
    model_checkpoint_path: "val_loss=1.6273-step-50000"
    all_model_checkpoint_paths: "val_loss=1.6649-step-32009"
    all_model_checkpoint_paths: "val_loss=1.6454-step-40011"
    all_model_checkpoint_paths: "val_loss=1.6434-step-44012"
    all_model_checkpoint_paths: "val_loss=1.6338-step-48013"
    all_model_checkpoint_paths: "val_loss=1.6273-step-50000"
    checkpoint (END)

    less /data/en-de-transformer/checkpoint
    model_checkpoint_path: "model.ckpt-50000"
    all_model_checkpoint_paths: "model.ckpt-0"
    all_model_checkpoint_paths: "model.ckpt-49998"
    all_model_checkpoint_paths: "model.ckpt-50000"
    checkpoint (END)
#### 10. How big is your resulting model checkpoint (mb)?
A total of `871 MB`

    root@v100a:/data/en-de-transformer/best_models# ls -l --block-size=MB
    ...
    -rw-r--r-- 1 root root   1MB Feb 28 14:39 checkpoint
    -rw-r--r-- 1 root root 853MB Feb 28 14:39 val_loss=1.6273-step-50000.data-00000-of-00001
    -rw-r--r-- 1 root root   1MB Feb 28 14:39 val_loss=1.6273-step-50000.index
    -rw-r--r-- 1 root root  17MB Feb 28 14:39 val_loss=1.6273-step-50000.meta
#### 11. Remember the definition of a "step". How long did an average step take?
Steps are the auto-regressive treatment of previous step (ie. per-GPU batch of data lines) gradient descent model parameter outputs (cite: https://arxiv.org/pdf/1706.03762.pdf). Per nohup, `avg. time per step was 1.714s`.

    *** Validation loss: 1.6273 
    *** Eval BLUE score: 0.369
    *** Finished training
    *** Avg time per step: 1.714s
    *** Avg objects per second: 36410.491
#### 12. How does that correlate with the observed network utilization between nodes?
Network utilization was mostly operating @ 80% of peak. Noting the size of the model (871 MB), it is apparent that the entire model can not be exchanged and updated every 1.7s over a 1 Gbps (125 MB/s) connection. I am interested to understand what subset of the model is being exchanged over MPI distributed computed scheme. Research has not yeilded this level of information. 
