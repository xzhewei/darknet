cd ..
./darknet detector train cfg/scut.data cfg/yolov3-scut-batch2.cfg cfg/darknet53.conv.74 -gpus 2
./darknet detector valid cfg/scut.data cfg/yolov3-scut-batch2.cfg backup/batch02/yolov3-scut-batch2_final.weights -gpus 2

./darknet detector train cfg/scut-C2.data cfg/yolov3-scut-batch2-C2.cfg cfg/darknet53.conv.74 -gpus 2
./darknet detector valid cfg/scut-C2.data cfg/yolov3-scut-batch2-C2.cfg backup/batch02-C2/yolov3-scut-batch2-C2_final.weights -gpus 2

./darknet detector train cfg/scut-C2.data cfg/yolov3-scut-batch2-C2.cfg cfg/darknet53.conv.74 -gpus 2

./darknet detector train cfg/scut.data cfg/yolov2-scut.cfg cfg/darknet19_448.conv.23 -gpus 3
./darknet detector valid cfg/scut.data cfg/yolov2-scut.cfg backup/batch64/yolov2-scut_final.weights -gpus 3

./darknet detector train cfg/scut-B64-C2.data cfg/yolov3-scut-C2.cfg cfg/darknet53.conv.74 -gpus 2,3

./darknet detector train cfg/scut-B2-C2.data cfg/yolov2-scut-batch2-C2.cfg cfg/darknet19_448.conv.23 -gpus 3

./darknet detector train cfg/scut.data cfg/yolov1-scut.cfg cfg/extraction.conv.weights -gpus 3
./darknet detector valid cfg/scut.data cfg/yolov1-scut.cfg backup/batch64/yolov1-scut_final.weights -gpus 3
python scripts/comp2res.py --result results/batch64/yolov3