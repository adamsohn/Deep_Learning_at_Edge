# W251 HW11 Submission
#### Adam Sohn
____________
## Configuration Summary

| Configuration                   | Loss                    | Optimizer | Train Treshhold | Total Iter | Epochs | Retrain Modulo | Successful Landings | Best Model                                                                                                                                                                                                                            |
|-------------------------|-------------------------|-----------|-----------------|------------|--------|----------------|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 - Baseline            | mean-squared-error      | adam      | 3000            | 50000      | 10     | 1000           | 52                  | [Link - Model 1 - 46k Iter](https://cossohn.s3.us-east.cloud-object-storage.appdomain.cloud/model1_frame46000.mp4) <br><br> [Link - Model 1 - 10k Iter](https://cossohn.s3.us-east.cloud-object-storage.appdomain.cloud/model1_frame10000.mp4) |
| 2 - Modify Optimizer    | mean-squared-error      | **sgd**   | 3000            | **10000**  | 10     | 1000           | 6                   | [Link- Model 2 - 10k Iter](https://cossohn.s3.us-east.cloud-object-storage.appdomain.cloud/model2_frame10000.mp4)                                                                                                                     |
| 3 - Modify Loss         | **mean-absolute-error** | adam      | 3000            | **10000**  | 10     | 1000           | 1                   | [Link - Model 3 - 10k Iter](https://cossohn.s3.us-east.cloud-object-storage.appdomain.cloud/model3_frame10000.mp4)                                                                                                                    |
| 4 - Modify Train Params | mean-squared-error      | adam      | **6000**        | **10000**  | **2**  | **2000**       | 0                   | [Link - Model 4 - 10k Iter](https://cossohn.s3.us-east.cloud-object-storage.appdomain.cloud/model4_frame10000.mp4)                                                                                                                    |

## What parameters did you change? What values did you try?
**Configuration 1** 
The baseline configuration was ran for a basis of comparison. As the model grew in iterations, the motion of the lander was under more control, however the successful landing count did not significantly improve. 

**Configuration 2**  
ML practitioners have noted that the `adam` optimizer performance towards convergence is outstanding based on well-set initial weights. To test the concept that initial weights might not be well-set for the simulation, Configuration 2 will choose `Stochastic Gradient Descent`w/ default arguments to test for quicker convergence, and thus better performance. To improve information-turns, `TotalIter` was capped at 10k. Models will therefore be compared on this basis for a fair comparison. 

The result for Configuration 2 was (6) successful landings by 10k Total Iterations. Compared to Configuration 1, this is on-pace, and not a large departure. However, comparing videos @ 10k, lander motion is more stable.

**Configuration 3**
Next approach is to explore using the `mean-squared-error` loss function to over-compensate for extreme inputs, as it is apparent that the lander performs over-correction movements. To test this, Configuration 3 will chose `mean-absolute-error` for the loss function to minimize over-reaction to extreme inputs. 

The result for Configuration 3 was (1) successful landing by 10k Total Iterations. Compared to either prior configuration, this is poor, yet not necessarily indicative of differing performance. Comparing videos, it appears the 10k node is learning negative behaviors, such as not descending!

## Did you try any other changes that made things better or worse? Did they improve or degrade the model?
**Configuration 4**
Finally, an attempt was in Configuration 4 to tweak the baseline model to initially train longer (6k vs. 3k steps), reduce epochs (successive epochs did not show itself to improve loss function performance after initial rounds), increase retrain modulo (2k vs. 1k), and cap Total Iter at 10k. The theory is that additional train data would result in a better converging, more generalizable, model. 

The result of Configuration 4 was no successful landings, indicating that perhaps the baseline configuration will not converge. Also, videos show very poor lander handling (tipping).

## Based on what you observed, what conclusions can you draw about the different parameters and their values?
**Loss function** Changing the loss function was a negative change. Changing from `mean-squared-error` to `mean-absolute-error` caused odd lander handling. This indicates that the lander simulation does not have sufficient outliers that need handling. In fact, reducing the effects of boundary cases caused the models to not generalize well.<br>
**Optimizer** Changing the optimizer was the best lever for positive change. Changing from `adam` to `sgd` improved handling of the lander to limit over-corrections. <br>
**Train Threshold** From my observations, I did not note a change by doubling the Train Threshold. <br>
**Total Iter** The lander does perform better with more iterations, however this is costly in compute time, and does not bring performance into an acceptable range for applying to actual space hardware. <br>
**Epochs** An increasing epoch count does reduce loss, however its value may not be significant. In early training sessions, over 10 epochs, a 30% reduction in loss can be seen. In later training sessions, minimal loss reduction is seen.<br>
**Retrain Modulo** Increasing retrain modulo does not help a model that is poor performing. Poor performing models need to re-trained more frequently.

## Next steps for further improvement
1. Reduce retrain modulo.
2. Use `sgd` optimizer.
3. Run many iterations, economizing on compute time by reducing epochs.
4. Explore modification of model layers (nnmodel)
5. Port model to GPU to better use TX2
