import argparse
import sys
import pydatatool as pdt
import os
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert comp4_det_test_* results to datatool evaluate format.'
    )
    parser.add_argument(
        '--result',
        dest='result_dir',
        default='results',
        type=str
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()

def parse_comp(all_boxes,file,cls_ind,imgn):
    '''Parse Yolo test result file to all_box[cls][img_ind] struct.'''
    comp = open(file,'r')
    for line in comp.readlines():
        tmp = line.strip().split(' ')
        imgind = imgn.index(tmp[0])
        all_boxes[cls_ind][imgind].append(box_convert(tmp[1:]))
    comp.close()

    for imind, im_n in enumerate(imgn):
        all_boxes[cls_ind][imind] = np.array(all_boxes[cls_ind][imind])

    return all_boxes

def box_convert(box):
    box = map(float,box)
    s = box[0]
    xmin = box[1]
    ymin = box[2]
    xmax = box[3]
    ymax = box[4]

    return (xmin,ymin,xmax,ymax,s)

def empty_results(num_classes, num_images):
    all_boxes = [[[] for _ in range(num_images)] for _ in range(num_classes)]
    return all_boxes

def write_scut_results_files(classes, imgs, all_boxes, res_dir):
    print(
        'Writing bbox results to: {}'.format(os.path.abspath(res_dir)))
    img_names = [os.path.splitext(img['file_name'])[0] for img in imgs]
    img_names.sort()
    pdt.scut.write_voc_results_file(
        all_boxes, img_names, res_dir, classes)

def do_matlab_eval(path, res_dir, output_dir):
    import subprocess
    print('-----------------------------------------------------')
    print('Computing results with the official MATLAB eval code.')
    print('-----------------------------------------------------')
    cmd = 'cd {} && '.format(path)
    cmd += '{:s} -nodisplay -nodesktop '.format('matlab')
    cmd += '-r "dbstop if error;'
    cmd += 'startup;'
    cmd += 'scut_eval(\'{:s}\',\'{:s}\',\'{:s}\'); quit;"' \
        .format(
            os.path.abspath(res_dir),
            os.path.abspath(output_dir),
            'yolo')
    print('Running:\n{}'.format(cmd))
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
    while p.poll() is None:
        line = p.stdout.readline()
        line = line.strip()
        if line:
            print('Subprogram output: [{}]'.format(line))
    if p.returncode == 0:
        print('Subprogram success')
    else:
        print('Subprogram failed')

def main():
    pwd = os.getcwd()
    # comp_dir = pwd + '/results/batch64/yolov3'
    args = parse_args()
    comp_dir = args.result_dir

    print('Loading vbb annotations.')
    vbbs = pdt.scut.load_vbbs('data/scut/annotations_vbb')
    image_ids_test = pdt.scut.get_image_ids('scut_test', vbbs, 25)
    classes = pdt.scut.get_classes()
    imgn = [img['file_name'].split('.')[0] for img in image_ids_test]
    print('Done.')

    print('Parse yolo results files.')
    all_boxes = empty_results(len(classes), len(image_ids_test))
    for cls_ind, cls in enumerate(classes[:-2]):
        if cls_ind == 0:
            continue
        fname = comp_dir + '/comp4_det_test_{}.txt'.format(cls)
        if os.path.exists(fname):
            all_boxes = parse_comp(all_boxes,fname,cls_ind,imgn)
    print('Done.')

    res_dir = os.path.join(comp_dir,'scut_eval','yolo')
    write_scut_results_files(classes, image_ids_test, all_boxes, res_dir)
    devkit_dir = pwd+'/data/scut/datatool'

    do_matlab_eval(
        devkit_dir,
        res_dir,
        os.path.join(comp_dir, 'scut_eval')
    )

if __name__ == '__main__':
    main()