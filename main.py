import pathlib

from skimage import measure

from src.read_image_data import get_zero_one_image_data, get_entity_data
from src.writer import TimeConfig, write_supercollider_file

output_path = pathlib.Path(__file__).parent / "super_collider_src" / "output.scd"
input_file = pathlib.Path(__file__).parent / "test"/ "data" / "example_image.png"

time_config = TimeConfig(
    seconds_per_unit=0.4,
    pixels_per_unit=100,
    transition=0.05,
    max_duration=10,
)

zero_one_image_data = get_zero_one_image_data(input_file)
img_labeled = measure.label(zero_one_image_data, connectivity=1)
# show_label_image(img_labeled, 1)
entities = get_entity_data(img_labeled)

write_supercollider_file(entities, output_path, time_config)