import struct


def write_instruction(instruction):
    pass


def calculate_file_size(numbers_data):
    number_point = numbers_data[0]
    number_instructions = numbers_data[1]
    number_pois = numbers_data[2]

    # Size of header adapted to obtain expected number, counted value was 139, need to understand where
    # difference comes from
    headers_size = 145
    alphabet_size = 3 * 1  # only 1 entry is in Alphabet
    points_size = number_point * 11
    instructions_size = (number_instructions + number_pois) * 44
    difference_file_size = 16

    size_attribute = (
        headers_size + points_size + instructions_size - difference_file_size
    )

    return size_attribute


def write_points(fit_file, converted_data):
    latitude_data = converted_data["latitude"]
    longitude_data = converted_data["longitude"]
    altitude_data = converted_data["altitude"]
    instruction_data = converted_data["Instruction"]

    for i in range(0, len(latitude_data)):
        # 1 byte
        byte = b"\x06"
        fit_file.write(byte)

        # 4 bytes
        # Point latitude
        point_latitude = latitude_data[i]
        byte = struct.pack("<i", point_latitude)
        fit_file.write(byte)

        # 4 bytes
        # Point longitude
        point_longitude = longitude_data[i]
        byte = struct.pack("<i", point_longitude)
        fit_file.write(byte)

        # 2 bytes
        # Point altitude
        point_altitude = altitude_data[i]
        byte = struct.pack("<H", point_altitude)
        fit_file.write(byte)


def write_instructions(
    fit_file,
    instruction_data,
    instruction_distance,
    name_data,
    points_of_interest,
    numbers_data,
):
    number_instructions = numbers_data[1]
    number_pois = numbers_data[2]

    poi_name = points_of_interest[0]
    poi_type = points_of_interest[1]
    poi_distance = points_of_interest[2]
    poi_identification = points_of_interest[3]

    # starts in -1 since first instructions should be 0
    instruction_identification = -1
    for i in range(0, len(instruction_data)):  # TBD Update number of points
        # increase identification to make sure that each Instruction is in the correct Point
        instruction_identification += 1

        # steps without turn instructions are identified with 15
        if instruction_data[i] != b"\xff":
            # 1 byte
            byte = b"\x04"
            fit_file.write(byte)

            # 2 bytes
            # Instruction identification
            instruction_identification = instruction_identification
            byte = struct.pack("<H", instruction_identification)
            fit_file.write(byte)

            # 1 bytes
            # Instruction direction
            byte = instruction_data[i]
            fit_file.write(byte)

            # 4 bytes
            # Instruction distance
            byte = int(float(instruction_distance[i]))
            byte = struct.pack("<I", byte)
            fit_file.write(byte)

            # 4 bytes
            # header
            byte = b"\xFF\xFF\xFF\xFF"
            fit_file.write(byte)

            # 32 bytes
            # Instruction description
            byte = str.encode(name_data[i], "utf-8")

            if len(byte) < 32:
                byte += b"\x00" * (32 - len(byte))
            else:
                byte = byte[:32]
            fit_file.write(byte)

    # write POI data
    i = 0
    for i in range(0, number_pois):  # TBD Update number of points
        # 1 byte
        byte = b"\x04"
        fit_file.write(byte)

        # 2 bytes
        # Instruction identification
        poi = poi_identification[i]
        byte = struct.pack("<H", poi)
        fit_file.write(byte)

        # 1 bytes
        # Instruction direction
        byte = poi_type[i]
        fit_file.write(byte)

        # 4 bytes
        # Instruction distance
        byte = int(float(poi_distance[i]))
        byte = struct.pack("<I", byte)
        fit_file.write(byte)

        # 4 bytes
        # header
        byte = b"\x00\x00\x00\x00"
        fit_file.write(byte)

        # 32 bytes
        # Instruction description
        byte = str.encode(poi_name[i], "utf-8")

        if len(byte) < 32:
            byte += b"\x00" * (32 - len(byte))
        else:
            byte = byte[:32]
        fit_file.write(byte)


def write_alphabet(fit_file):
    for i in range(0, 1500):
        # 1 byte
        byte = b"\x02"
        fit_file.write(byte)
        # 2 bytes
        alphabet_instruction = i
        byte = struct.pack("<H", alphabet_instruction)
        fit_file.write(byte)


def encode_fit(fit_path, converted_data, extracted_attributes):
    fit_file = open(fit_path, "wb")

    instruction_data = converted_data["Instruction"]
    name_data = converted_data["name"]

    lat_lon_bounding_box = extracted_attributes["lat_lon_bounding_box"]
    lat_ne_bounding_box = lat_lon_bounding_box[0]
    lat_sw_bounding_box = lat_lon_bounding_box[1]
    lon_ne_bounding_box = lat_lon_bounding_box[2]
    lon_sw_bounding_box = lat_lon_bounding_box[3]

    total_distance = int(extracted_attributes["total_distance"])
    alt_bounding_box = extracted_attributes["alt_bounding_box"]
    maximum_altitude = alt_bounding_box[0]
    minimum_altitude = alt_bounding_box[1]
    numbers_data = extracted_attributes["number_data"]
    number_point = numbers_data[0]
    number_instructions = numbers_data[1]
    number_pois = numbers_data[2]
    instruction_distance = extracted_attributes["instruction_distance"]
    points_of_interest = extracted_attributes["points_of_interest"]

    # 4 bytes
    # header
    byte = b"\x0E\x10\x6C\x00"
    fit_file.write(byte)

    # 4 bytes
    # file size
    file_size = calculate_file_size(numbers_data)
    byte = struct.pack("<i", file_size)
    fit_file.write(byte)

    # 4 bytes
    # header
    byte = b"\x2E\x46\x49\x54"
    fit_file.write(byte)

    # 2 bytes
    # checksum
    byte = b"\x00\x00"
    fit_file.write(byte)

    # 32 bytes
    # header
    byte = (
        b"\x41\x00\x00\xFE\x00\x08\x01\x02\x84\x02\x04\x85\x03\x04\x85\x04\x04\x85\x05\x04\x85\x06"
        b"\x04\x86\x07\x02\x84\x08\x02\x84\x01"
    )
    fit_file.write(byte)

    # 2 bytes
    # number of points
    number_points = number_point
    byte = struct.pack("<H", number_points)
    fit_file.write(byte)

    # 4 bytes
    # lat NE bounding box
    lat_ne_bounding_box = lat_ne_bounding_box
    byte = struct.pack("<i", lat_ne_bounding_box)
    fit_file.write(byte)

    # 4 bytes
    # lat SW bounding box
    lat_sw_bounding_box = lat_sw_bounding_box
    byte = struct.pack("<i", lat_sw_bounding_box)
    fit_file.write(byte)

    # 4 bytes
    # lon NE bounding box
    lon_ne_bounding_box = lon_ne_bounding_box
    byte = struct.pack("<i", lon_ne_bounding_box)
    fit_file.write(byte)

    # 4 bytes
    # lon SW bounding box
    lon_sw_bounding_box = lon_sw_bounding_box
    byte = struct.pack("<i", lon_sw_bounding_box)
    fit_file.write(byte)

    # 4 bytes
    # total distance in meters
    total_distance = total_distance
    byte = struct.pack("<I", total_distance)
    fit_file.write(byte)

    # 2 bytes
    # maximum altitude
    maximum_altitude = maximum_altitude
    byte = struct.pack("<H", maximum_altitude)
    fit_file.write(byte)

    # 2 bytes
    # minimum altitude
    minimum_altitude = minimum_altitude
    byte = struct.pack("<H", minimum_altitude)
    fit_file.write(byte)

    # 9 bytes
    # header
    byte = b"\x42\x00\x00\xFB\x00\x01\x01\x02\x84"
    fit_file.write(byte)

    # 3 bytes
    # Alphabet
    byte = b"\x02\x00\x00"
    fit_file.write(byte)
    # empirical tests show that the presence of the Alphabet does not affect the unit handling of the file
    # write_alphabet(fit_file)

    # 10 bytes
    # header
    byte = b"\x43\x00\x00\xFD\x00\x01\x01\x02\x84\x03"
    fit_file.write(byte)

    # 2 bytes
    number_instructions = number_instructions + number_pois
    byte = struct.pack("<H", number_instructions)
    fit_file.write(byte)

    # 21 bytes
    # header
    byte = b"\x44\x00\x00\xFA\x00\x05\x01\x02\x84\x02\x01\x00\x03\x04\x86\x04\x04\x86\x05\x20\x07"
    fit_file.write(byte)

    write_instructions(
        fit_file,
        instruction_data,
        instruction_distance,
        name_data,
        points_of_interest,
        numbers_data,
    )

    # 10 bytes
    # header
    byte = b"\x45\x00\x00\xFC\x00\x01\x01\x02\x84\x05"
    fit_file.write(byte)

    # 2 bytes
    # number of points
    number_points = number_points
    byte = struct.pack("<H", number_points)
    fit_file.write(byte)

    # 15 bytes
    # header
    byte = b"\x46\x00\x00\xF9\x00\x03\x01\x04\x85\x02\x04\x85\x03\x02\x84"
    fit_file.write(byte)

    write_points(fit_file, converted_data)

    byte = b"\x00\x00"
    fit_file.write(byte)
