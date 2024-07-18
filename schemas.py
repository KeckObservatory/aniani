# used for /getCurrent and /getPredict
reflectivity_input_schema = {
    "type": "object",
    "properties": {
        "mirror": {"type": "string", "enum": ["primary", "secondary", "tertiary"]},
        "telescope_num": {"type": "integer", "enum": [1, 2]},
        "measurement_type": {"type": "string", "enum": ["T", "S", "D"]}
    },
    "required": ["mirror", "telescope_num", "measurement_type"]
}

# to add new data into the MirrorSamples Table
# for /addReflectivityMeasurement
add_reflectivity_measurement_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "mirror": {"type": "string", "enum": ["primary", "secondary", "tertiary"]},
            "segment_id": {"type": "integer"},
            "mirror_type": {"type": "string", "enum": ["1", "2", "3", "4", "5", "6", "A", "B", "C"]},
            "measured_date": {"type": "string", "format": "date"},
            "install_date": {"type": "string", "format": "date"},
            "sample_status": {"type": "string", "enum": ["clean", "dirty"]},
            "telescope_num": {"type": "integer", "enum": [1, 2]},
            "segment_position": {"type": "integer"},
            "spectrum": {"type": "string", "enum": ["400-540", "480-600", "590-720", "900-1100"]},
            "measurement_type": {"type": "string", "enum": ["T", "S", "D"]},
            "reflectivity": {"type": "number"},
            "notes": {"type": "string"},
        },
        "required": ["mirror_type", "spectrum", "measurement_type"]
    }
}
