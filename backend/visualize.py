import numpy as np
from PIL import Image, ImageDraw


def visualize_yolo_annotation(image_path, annotation_path):
    # Load the image
    image = Image.open(image_path)
    w, h = image.size
    draw = ImageDraw.Draw(image)

    # Read the annotation file
    with open(annotation_path, "r") as file:
        for line in file:
            parts = line.strip().split()

            x_center = float(parts[1]) * w
            y_center = float(parts[2]) * h
            width = float(parts[3]) * w
            height = float(parts[4]) * h
            mask_points = list(map(float, parts[5:]))

            # Draw bounding box
            x1 = x_center - width / 2
            y1 = y_center - height / 2
            x2 = x_center + width / 2
            y2 = y_center + height / 2
            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)

            # Draw segmentation mask
            mask_points = [
                (mask_points[i] * w, mask_points[i + 1] * h)
                for i in range(0, len(mask_points), 2)
            ]
            draw.polygon(mask_points, outline="blue")
            image_np = np.array(image)

    return image_np


def visualize_detection(frame_number, image_path, annotation_path):
    img, frame = None, None
    if image_path and annotation_path:
        image_number = int(image_path.stem.split("_")[1])
        annotation_number = int(annotation_path.stem.split("_")[1])

        if image_number == frame_number and annotation_number == frame_number:
            img = visualize_yolo_annotation(image_path, annotation_path)

        if img is not None:
            frame = img[:, :, ::-1]
    return frame
