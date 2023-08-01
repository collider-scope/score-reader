import pathlib
import tempfile

from skimage import measure
from src.read_image_data import get_zero_one_image_data, show_label_image, get_entity_data
from src.writer import TimeConfig, write_supercollider_file


def test_basic():
    with tempfile.TemporaryDirectory() as dir:
        output_path = pathlib.Path(dir) / "output.scd"
        input_file = pathlib.Path(__file__).parent / "data" / "example_image.png"

        time_config = TimeConfig(
            seconds_per_unit=0.4,
            pixels_per_unit=100,
            transition=0.05,
            max_duration=10,
        )

        zero_one_image_data = get_zero_one_image_data(input_file)
        img_labeled = measure.label(zero_one_image_data, connectivity=1)
        #show_label_image(img_labeled, 1)
        entities = get_entity_data(img_labeled)

        write_supercollider_file(entities, output_path, time_config)

        import filecmp
        assert filecmp.cmp(output_path, pathlib.Path(__file__).parent /
                           "data" / "example_ref.scd", shallow=False)



