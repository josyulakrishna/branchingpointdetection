try:
    # ignore ShapelyDeprecationWarning from fvcore
    from shapely.errors import ShapelyDeprecationWarning
    import warnings
    warnings.filterwarnings('ignore', category=ShapelyDeprecationWarning)
except:
    pass

import copy
import itertools
import logging
import os

from collections import OrderedDict
from typing import Any, Dict, List, Set
import tqdm
from detectron2.data.datasets import register_coco_instances
from detectron2.data import MetadataCatalog
from detectron2.data import DatasetCatalog
from detectron2.engine import DefaultTrainer
from detectron2.engine import DefaultPredictor
from detectron2.evaluation import COCOEvaluator
from predictor import VisualizationDemo

import argparse
import glob
import multiprocessing as mp
import os

import torch

import detectron2.utils.comm as comm
from detectron2.checkpoint import DetectionCheckpointer
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog, build_detection_train_loader
from detectron2.engine import (
    DefaultTrainer,
    default_argument_parser,
    default_setup,
    launch,
)
from detectron2.evaluation import (
    CityscapesInstanceEvaluator,
    CityscapesSemSegEvaluator,
    COCOEvaluator,
    COCOPanopticEvaluator,
    DatasetEvaluators,
    LVISEvaluator,
    SemSegEvaluator,
    verify_results,
)
from detectron2.projects.deeplab import add_deeplab_config, build_lr_scheduler
from detectron2.solver.build import maybe_add_gradient_clipping
from detectron2.utils.logger import setup_logger



# MaskFormer
from mask2former import (
    COCOInstanceNewBaselineDatasetMapper,
    COCOPanopticNewBaselineDatasetMapper,
    InstanceSegEvaluator,
    MaskFormerInstanceDatasetMapper,
    MaskFormerPanopticDatasetMapper,
    MaskFormerSemanticDatasetMapper,
    SemanticSegmentorWithTTA,
    add_maskformer2_config,
)



def setup_cfg(args):
    # load config from file and command-line arguments
    cfg = get_cfg()
    add_deeplab_config(cfg)
    add_maskformer2_config(cfg)
    cfg.merge_from_file(args.config_file)
    # cfg.merge_from_list(args.opts)
    cfg.DATASETS.TRAIN = ("bpTrain",)
    cfg.DATASETS.TEST = ("bpTest",)
    cfg.freeze()
    return cfg


def get_parser():
    parser = argparse.ArgumentParser(description="maskformer2 demo for builtin configs")
    parser.add_argument(
        "--config-file",
        default="/home/josyula/Programs/branchingpointdetection/Mask2Former/configs/coco/panoptic-segmentation/maskformer2_R50_bs16_50ep.yaml",
        metavar="FILE",
        help="path to config file",
    )
    return parser


if __name__ == "__main__":
    ######## REGISTER DATASET #################
    print("registering")
    register_coco_instances("bpTrain", {}, "/home/josyula/Programs/branchingpointdetection/coco/annotation/train.json",
                            "/home/josyula/Programs/branchingpointdetection/coco/labelled")
    # register_coco_instances("pruningVal", {}, "/home/josyula/Documents/DataAndModels/labeled_data/val/runs/labelme2coco/val.json", "/home/josyula/Documents/DataAndModels/labeled_data/val")
    register_coco_instances("bpTest", {}, "/home/josyula/Programs/branchingpointdetection/coco/annotation/test.json",
                            "/home/josyula/Programs/branchingpointdetection/coco/labelled")
    # dataset_dicts = DatasetCatalog.get("prunningTrain")

    for data_ in ["bpTrain", "bpTest"]:
        dataset_dicts = DatasetCatalog.get(data_)
        pruning_meta_data = MetadataCatalog.get(data_).thing_classes
        print(pruning_meta_data)
    mp.set_start_method("spawn", force=True)
    args = get_parser().parse_args()
    setup_logger(name="fvcore")
    logger = setup_logger()
    logger.info("Arguments: " + str(args))


    cfg = setup_cfg(args)

    demo = VisualizationDemo(cfg)

    if args.input:
        if len(args.input) == 1:
            args.input = glob.glob(os.path.expanduser(args.input[0]))
            assert args.input, "The input path(s) was not found"
        for path in tqdm.tqdm(args.input, disable=not args.output):
            # use PIL, to be consistent with evaluation
            img = read_image(path, format="BGR")
            start_time = time.time()
            predictions, visualized_output = demo.run_on_image(img)
            logger.info(
                "{}: {} in {:.2f}s".format(
                    path,
                    "detected {} instances".format(len(predictions["instances"]))
                    if "instances" in predictions
                    else "finished",
                    time.time() - start_time,
                )
            )

            if args.output:
                if os.path.isdir(args.output):
                    assert os.path.isdir(args.output), args.output
                    out_filename = os.path.join(args.output, os.path.basename(path))
                else:
                    assert len(args.input) == 1, "Please specify a directory with args.output"
                    out_filename = args.output
                visualized_output.save(out_filename)
            else:
                cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
                cv2.imshow(WINDOW_NAME, visualized_output.get_image()[:, :, ::-1])
                if cv2.waitKey(0) == 27:
                    break  # esc to quit
