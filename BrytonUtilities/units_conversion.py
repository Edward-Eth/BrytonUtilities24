import unidecode


def instruction_conversion_ors(instruction_data):
    instruction_data_converted = []
    for instruction in instruction_data:
        if instruction == 0:
            ins = b"\x03"  # left
        elif instruction == 1:
            ins = b"\x02"  # right
        elif instruction == 2:
            ins = b"\x07"  # close left
        elif instruction == 3:
            ins = b"\x06"  # close right
        elif instruction == 4:
            ins = b"\x05"  # slight left
        elif instruction == 5:
            ins = b"\x04"  # slight right
        elif instruction == 6:
            ins = b"\x01"  # go ahead
        elif instruction == 7:
            ins = b"\x01"  # go ahead
        elif instruction == 8:
            ins = b"\x08"  # exit right
        elif instruction == 9:
            ins = b"\x07"  # uturn left
        elif instruction == 10:
            ins = b"\x01"  # go ahead
        elif instruction == 11:
            ins = b"\x01"  # go ahead
        elif instruction == 12:
            ins = b"\x09"  # exit left
        elif instruction == 13:
            ins = b"\x08"  # exit right
        elif instruction == 14:
            ins = b"\x01"  # go ahead
        else:
            ins = b"\xff"  # none
        instruction_data_converted.append(ins)
    return instruction_data_converted


def instruction_conversion_par(instruction_data):
    instruction_data_converted = []
    for instruction in instruction_data:
        if instruction == "Left":
            ins = b"\x03"  # left
        elif instruction == "Right":
            ins = b"\x02"  # right
        elif instruction == "Left_sharp":
            ins = b"\x07"  # close left
        elif instruction == "Right_sharp":
            ins = b"\x06"  # close right
        elif instruction == "Left_slight":
            ins = b"\x05"  # slight left
        elif instruction == "Right_slight":
            ins = b"\x04"  # slight right
        elif instruction == "Straight":
            ins = b"\x01"  # go ahead
        elif instruction == "Flag, Blue":
            ins = b"\x01"  # go ahead
        elif instruction == 8:
            ins = b"\x08"  # exit right
        elif instruction == 9:
            ins = b"\x07"  # uturn left
        elif instruction == 12:
            ins = b"\x09"  # exit left
        elif instruction == 13:
            ins = b"\x08"  # exit right
        else:
            ins = b"\xff"  # none
        instruction_data_converted.append(ins)
    return instruction_data_converted


def name_conversion_ors(name_data):
    name_data_converted = []
    for name in name_data:
        name = unidecode.unidecode(name)

        name = name.replace("A(c)", "e")
        name = name.replace("A!", "a")
        name = name.replace("A'", "o")
        name = name.replace("ASS", "c")
        name = name.replace("APS", "a")
        name = name.replace("A3", "o")

        name = name.replace("Rua", "R")
        name = name.replace("Avenida", "Av")
        name = name.replace("Professora", "Prf")
        name = name.replace("Professor", "Prf")
        name = name.replace("Doutora", "Dr")
        name = name.replace("Doutor", "Dr")
        name = name.replace("Estrada", "Est")

        name = name.replace("Eduardo", "Edu")
        name = name.replace("Monte", "Mt")
        name = name.replace("Viaduto", "Via")
        name = name.replace("Passagem", "Ps")
        name = name.replace("Navel", "Nv")
        name = name.replace("Engenheira", "Eng")
        name = name.replace("Engenheiro", "Eng")
        name = name.replace("Marechal", "Mrc")

        name_data_converted.append(name[:32])
    return name_data_converted


def name_conversion_par(name_data):
    name_data_converted = []
    for name in name_data:
        name = unidecode.unidecode(name)

        name = name.replace("Road", "Rd")
        name = name.replace("Avenue", "Av")
        name = name.replace("Street", "Est")
        name = name.replace("Lane", "Ln")
        name = name.replace("Passage", "Ln")
        name = name.replace("Turn right", "")
        name = name.replace("Turn left", "")
        name = name.replace("Turn slight right", "")
        name = name.replace("Turn slight left", "")
        name = name.replace("Keep right", "")
        name = name.replace("Keep left", "")
        name = name.replace("onto", "")

        name_data_converted.append(name[:32])
    return name_data_converted


def convert_input_units(decoded_data, source):
    latitude_data = decoded_data["latitude"]
    longitude_data = decoded_data["longitude"]
    altitude_data = decoded_data["altitude"]
    instruction_data = decoded_data["Instruction"]
    name_data = decoded_data["name"]

    if source == "ors":
        instruction_data_converted = instruction_conversion_ors(instruction_data)
    elif source == "par":
        instruction_data_converted = instruction_conversion_par(instruction_data)
    else:
        raise ValueError("Unsupported GPX source")

    skipped_instructions = [[i, name, orig_instruction] for i, (name, orig_instruction, instruction) in enumerate(zip(name_data, instruction_data, instruction_data_converted)) if
                            instruction == b"\xff" and orig_instruction != ""]

    if len(skipped_instructions) > 0:
        import csv

        with open('SkippedInstructions.csv', 'w') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(skipped_instructions)

    latitude_data_converted = []
    longitude_data_converted = []
    altitude_data_converted = []

    # converting lat, lon and alt to units used in .fit files
    for latitude in latitude_data:
        latitude_data_converted.append(int(float(latitude) * 1000000))
    for longitude in longitude_data:
        longitude_data_converted.append(int(float(longitude) * 1000000))
    for altitude in altitude_data:
        altitude_data_converted.append(int((float(altitude) * 5) + 2500))

    if source == "ors":
        name_data_converted = name_conversion_ors(name_data)
    elif source == "par":
        name_data_converted = name_conversion_par(name_data)
    else:
        raise ValueError("Unsupported GPX source")

    converted_data = {
        "latitude": latitude_data_converted,
        "longitude": longitude_data_converted,
        "altitude": altitude_data_converted,
        "Instruction": instruction_data_converted,
        "name": name_data_converted,
    }

    return converted_data
