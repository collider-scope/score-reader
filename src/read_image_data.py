from dataclasses import dataclass

import numpy as np
from PIL import Image

def load_image(infilename) :
    image = Image.open(infilename).convert('L')
    data = np.asarray(image, dtype="int32")
    return data


def get_zero_one_image_data(relative_image_path):
    image_data = load_image(relative_image_path)
    image_data[np.where(image_data < 255)] = 1
    image_data[np.where(image_data == 255)] = 0
    return image_data

def show_label_image(img_labeled, label):
    label_arr = np.ones(img_labeled.shape) * 256
    label_arr[np.where(img_labeled == label )] = 0
    image_out = Image.fromarray(label_arr)
    image_out.show()


@dataclass
class EntityProperties:
    mean_array: np.array
    start_value: float
    end_value: float
    distance_values: np.array
    length: float


def get_entity_data(img_labeled):
    max_label = np.max(img_labeled)
    entities = []

    for label in range(1, max_label + 1):
        x_values = np.where(img_labeled == label)[1]
        y_values = np.where(img_labeled == label)[0]

        y_values = y_values.ravel()[x_values.argsort(axis=None).reshape(x_values.shape)]
        x_values.sort()

        changes = np.where(np.diff(x_values) > 0)[0]
        y_values_groups = np.split(y_values, changes)
        max_array = []
        min_array = []
        distance_array = []
        mean_array = []
        for group in y_values_groups:
            min_array.append(np.min(group))
            max_array.append(np.max(group))
            distance_array.append(np.max(group) - np.min(group))
            mean_array.append(img_labeled.shape[0] - np.mean(group))

        properties = EntityProperties(
            mean_array=mean_array,
            start_value=np.min(x_values),
            end_value=np.max(x_values),
            distance_values=distance_array,
            length=np.max(x_values) - np.min(x_values)
        )
        entities.append(properties)
    return entities
