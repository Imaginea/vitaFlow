import os

try:
    from grpc_predict import read_image, get_text_segmentation_pb
    from icdar_data import get_images
except:
    from vitaflow.playground.east.grpc_predict import read_image, get_text_segmentation_pb
    from vitaflow.playground.east.icdar_data import get_images

from tensorflow.contrib import predictor
from vitaflow import demo_config

from vitaflow.demo_config import create_dirs


def east_flow_predictions(input_dir=demo_config.IMAGE_ROOT_DIR,
                          output_dir=demo_config.EAST_OUT_DIR,
                          model_dir=demo_config.EAST_MODEL_DIR):
    images_dir = input_dir
    images = get_images(images_dir)
    predict_fn = predictor.from_saved_model(model_dir)
    for image_file_path in images:
        im, img_resized, ratio_h, ratio_w = read_image(image_file_path)
        result = predict_fn({'images': img_resized})
        get_text_segmentation_pb(img_mat=im,
                                 result=result,
                                 output_dir=output_dir,
                                 file_name=os.path.basename(image_file_path),
                                 ratio_h=ratio_h,
                                 ratio_w=ratio_w)


if __name__ == '__main__':
    create_dirs()
    east_flow_predictions()