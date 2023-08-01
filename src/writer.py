from dataclasses import dataclass

@dataclass(frozen=True)
class TimeConfig:
    pixels_per_unit: int
    transition: float
    seconds_per_unit: float
    # Max Duration for single events
    max_duration: float
    # Transition period for amplitude
    transition: float

def get_event_time(number_of_pixels, time_config):
    return number_of_pixels / time_config.pixels_per_unit * time_config.seconds_per_unit

def write_values(name, entities, attr, file, sampling_size):
    file.write(f"~{name} =[")
    for idx, entity in enumerate(entities):
        entity_values = getattr(entity, attr)[0:-1:sampling_size]
        first_value = entity_values[0]
        last_value = entity_values[0]
        if idx > 0:
            file.write(",")
        file.write("[")
        file.write(f"{first_value},{first_value},")
        for value in entity_values:
            file.write(f"{value},")
        file.write(f"{last_value},{last_value}]")
    file.write("];")


def write_supercollider_file(entities, output_path, time_config):
    with open(output_path, "w") as file:
        write_values("mean", entities, "mean_array", file, time_config.pixels_per_unit)
        write_values("distance", entities, "distance_values", file, time_config.pixels_per_unit)

        file.write(f"~duration_amp =[")
        for idx, entity in enumerate(entities):
            if idx > 0:
                file.write(",")
            file.write(f"[{get_event_time(entity.start_value, time_config)},{time_config.transition},")
            for idx in range(len(entity.mean_array)//time_config.pixels_per_unit):
                file.write(f"{time_config.seconds_per_unit},")
            file.write(f"{time_config.transition}]")
        file.write("];")

        file.write(f"~amp =[")
        for idx, entity in enumerate(entities):
            if idx>0:
                file.write(",")
            file.write("[")
            file.write("0,0,")
            for mean_value in entity.mean_array[0:-1:time_config.pixels_per_unit]:
                file.write(f"{1.0},")
            file.write("0]")

        file.write("];")

        file.write(f"~duration_single =[")
        for idx, entity in enumerate(entities):
            if idx > 0:
                file.write(",")
            file.write(f"[Rest({get_event_time(entity.start_value, time_config)}),{time_config.max_duration}]")
        file.write("];")

        file.write(f"~length_single =[")
        for idx, entity in enumerate(entities):
            if idx > 0:
                file.write(",")
            file.write(f"[Rest({get_event_time(entity.start_value, time_config)}),{get_event_time(entity.length, time_config)}]")
        file.write("];")
