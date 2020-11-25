Adam Sohn

Part 1: Image Annotation <br>
1. All 384 images were tagged.
```
root@duct:/home/kollel/Documents/Homework/MIDS_HW8/images# ls -1 | wc -l
384
```

2. 296 Millennium Falcons and 266 TIE Fighters were tagged.
```
root@duct:/home/kollel/Documents/Homework/MIDS_HW8/annotations# cat * | grep -c Falcon
296
root@duct:/home/kollel/Documents/Homework/MIDS_HW8/annotations# cat * | grep -c Fighter
266
```
3. Based on this experience, annotating a large data set by hand can not be done with the assumption that the result would be high quality. This experience gave insight that person-person bias would show in the presence of labels for difficult sightings and the buffer around each annotation would be variable. For a large data set, the recommendation would be to employ a image recognition classifier to perform the work. If the classifier does not have a trained model, training the model would be needed.

4. In a completely naive system (human annotation only), image augmentation would introduce a source of confusion, which would translate to error. In a smarter system, image augmentation on already annotated dataset could be automatic and high quality.
<br>
Part 2: Image Augmentation <br>
1. <br>
* Flip - Rotate image about vertical axis <br>
* Rotation - Rotate image about horizontal axis <br>
* Scale - Not shown in notebook. Zooming in or out to a sub-section of the image according to either a fixed width/height parameter or a variable width/height scalar. <br>
* Crop - Not shown in in notebook. Removing portions of an image, leaving behind a sub-section of the original image. <br>
* Translation - Moving the image within the frame of the containing matrix <br>
* Noise - Overlay image w/ random pixels <br>
<br>
Part 3: Audio Annotation <br>
1. In the model of CrowdCurio, audio annotations require start/end time and classes.

