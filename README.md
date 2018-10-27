![Darknet Logo](http://pjreddie.com/media/files/darknet-black-small.png)

# Darknet #
Darknet is an open source neural network framework written in C and CUDA. It is fast, easy to install, and supports CPU and GPU computation.

For more information see the [Darknet project website](http://pjreddie.com/darknet).

For questions or issues please use the [Google Group](https://groups.google.com/forum/#!forum/darknet).

# For Pedestrian Detection task
Darknet is available for training and testing on VOC and COCO datasets, this repo modified it for [SCUT](https://github.com/SCUT-CV/SCUT_FIR_Pedestrian_Dataset) datasets. 
Use the same step, it also can training on Caltech and KAIST dataset.

## 1. Download data
Go to the [SCUT](https://github.com/SCUT-CV/SCUT_FIR_Pedestrian_Dataset) download `videos`, `annotations.zip` and `annotaions_vbb.zip` to `data/scut` dir.
Unzip all files, make sure the directory structure like this.
```
data/scut/
- videos/
    - set00/
        - V000.seq
        - V001.seq
        - V002.seq
    - set01/
        ...
    ...
- annotations/
    - set00/
        - V000.txt
        - V001.txt
        - V002.txt
    - set01/
        ...
    ...
- annotations_vbb/
    - set00/
        - V000.vbb
        - V001.vbb
        - V002.vbb
    - set01/
        ...
    ...
```

## 2. Download toolbox
The dataset has two toolbox. 
`datatool` is a matlab toolbox based on caltech toolbox. 
`pydatatool` is a python package for convert caltech style annotation to other style.

```bash
cd data/scut
git clone https://github.com/xzhewei/datatool.git
mkdir data-scut
ln -s <project-root>/data/scut/annoations ./
git clone https://github.com/xzhewei/pydatatool.git
```
Make & install pydatatool
```bash
cd pydatatool
make install
```

## 3. Convert dataset
Now we need to generate the label files that Darknet uses.
```bash
python scripts/vbb2yolo.py
```
After a few minutes, this script will generate all of the requisite files.

In `cfg/scut.data`, there some parameters the specific path.
```
classes= 6
train  = <path-to-scut>/train.txt
valid  = <path-to-scut>/test.txt
names = data/scut.names
backup = backup
results = results
```
## 4. Training
Download the pretrain weigth file.
```bash
cd cfg
wget https://pjreddie.com/media/files/darknet53.conv.74
cd ..
```
Training Yolov3 on SCUT dataset.
```bash
./darknet detector train cfg/scut.data cfg/yolov3-scut.cfg cfg/darknet53.conv.74 -gpus 0
```

## 5. Testing
Change the batch=1 in `cfg/yolov3-scut.cfg`, like this:
```
[net]
# Testing
batch=1
subdivisions=1
# Training
# batch=64
# subdivisions=16
```
And testing on 
```bash
./darknet detector valid cfg/scut.data cfg/yolov3-scut.cfg backup/yolov3-scut_final.weights -gpus 0
```
After testing, the `results` directory will generate 6 files which is every class detection results.
```
comp4_det_test_people.txt
comp4_det_test_people?.txt
comp4_det_test_person?.txt
comp4_det_test_ride_person.txt
comp4_det_test_squat_person.txt
comp4_det_test_walk_person.txt
```
Run `scripts/comp2res.py` to convert the results file to caltech toolbox style.
After convert it will evaluate by toolbox.
```
python scripts/comp2res.py --result results
```
