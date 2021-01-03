class predictor:
    def predict(file):
        import cv2
        import numpy as np
        import tensorflow as tf
        import sys
        import os

        sys.path.append("..")

        MODEL_NAME = 'inference_graph'

        CWD_PATH = os.getcwd()

        PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')
        PATH_TO_LABELS = os.path.join(CWD_PATH, 'object-detection.pbtxt')

        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
            sess = tf.Session(graph=detection_graph)

        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

        num_detections = detection_graph.get_tensor_by_name('num_detections:0')

        npimg = np.fromstring(file, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image_expanded = np.expand_dims(image_rgb, axis=0)

        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_expanded})

        ##label + score
        if classes[0][0] == 3 or classes[0][1] == 3:
            return 'Mask Worn Incorrectly'
        elif classes[0][0] == 1:
            return 'Wearing Mask'
        elif classes[0][0] == 2:
            return 'Not Wearing Mask'


'''
# Draw the results of the detection (aka 'visulaize the results')
vis_util.visualize_boxes_and_labels_on_image_array(
    image,
    np.squeeze(boxes),
    np.squeeze(classes).astype(np.int32),
    np.squeeze(scores),
    category_index,
    use_normalized_coordinates=True,
    line_thickness=8,
    min_score_thresh=0.60)

# All the results have been drawn on image. Now display the image.
imS = cv2.resize(image, (960, 960))
cv2.imshow('Object detector', imS)

# Press any key to close the image
cv2.waitKey(0)

# Clean up
cv2.destroyAllWindows()
'''
