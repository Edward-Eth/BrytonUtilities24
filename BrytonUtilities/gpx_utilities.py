from datetime import datetime

orst2brt = {
    0: 3,
    1: 2,
    2: 7,
    3: 6,
    4: 5,
    5: 4,
    6: 1,
    7: 10,
    8: 8,
    9: 12,
    10: 1,
    11: 1,
    12: 9,
    13: 8,
    14: 1,
}


def decode_gpx_ors(gpx_path):
    gpx_file = open(gpx_path, "r")
    gpx_file = gpx_file.read()
    # breaks single line file in multiple files
    gpx_file = gpx_file.split("<")

    latitude = []
    longitude = []
    altitude = []
    instruction = []
    name = []
    number_items = 0
    for line in gpx_file:
        line = "<" + line
        if line.find("lat=") != -1:
            lat = line.split('"')[1]
            latitude.append(lat)
            lon = line.split('"')[3]
            longitude.append(lon)
            ins = 15
            instruction.append(ins)
            alt = 0
            altitude.append(alt)
            nam = "none"
            name.append(nam)
            number_items += 1
        elif line.find("<type>") != -1 and number_items > 0:
            ins = int(line.lstrip().removeprefix("<type>"))
            instruction.pop()
            instruction.append(ins)
        elif line.find("<name>") != -1 and number_items > 0:
            nam = line.strip().removeprefix("<name>")
            name.pop()
            name.append(nam)
        elif line.find("<ele>") != -1 and number_items > 0:
            alt = line.lstrip().removeprefix("<ele>")
            altitude.pop()
            altitude.append(alt)

    for i in range(0, len(name) - 1):
        if name[i] == name[i + 1]:
            instruction[i + 1] = 15
    decoded_gpx = {
        "latitude": latitude,
        "longitude": longitude,
        "altitude": altitude,
        "Instruction": instruction,
        "name": name,
    }
    return decoded_gpx


def decode_gpx_plotaroute(gpx_path):
    gpx_file = open(gpx_path, "r")
    gpx_file = gpx_file.read()
    # breaks single line file in multiple files
    gpx_file = gpx_file.split("\n")

    latitude = []
    longitude = []
    altitude = []
    instruction = []
    name = []
    time = []
    number_items = 0
    for line in gpx_file:
        if line.find("lat=") != -1:
            lat = line.split('"')[1]
            latitude.append(lat)
            lon = line.split('"')[3]
            longitude.append(lon)
            instruction.append("none")
            altitude.append(0)
            name.append("none")
            time.append("none")
            number_items += 1
        elif line.find("<sym>") != -1 and number_items > 0:
            ins = line.lstrip().removeprefix("<sym>").removesuffix("</sym>")
            instruction.pop()
            instruction.append(ins)
        elif line.find("<desc>") != -1 and number_items > 0:
            nam = line.strip().removeprefix("<desc>").removesuffix("</desc>")
            name.pop()
            name.append(nam)
        elif line.find("<ele>") != -1 and number_items > 0:
            alt = line.lstrip().removeprefix("<ele>").removesuffix("</ele>")
            altitude.pop()
            altitude.append(alt)
        elif line.find("<time>") != -1 and number_items > 0:
            tim = datetime.fromisoformat(
                line.lstrip()
                .removeprefix("<time>")
                .removesuffix("</trkpt>")
                .removesuffix("</time>")
            ).timestamp()
            time.pop()
            time.append(tim)

    # After extraction, we need to slot in the waypoints where needed by sorting the lists according
    # to the time values extracted
    sorted_zip = sorted(zip(time, latitude, longitude, instruction, name, altitude))
    stripped_time = []
    stripped_latitude = []
    stripped_longitude = []
    stripped_instruction = []
    stripped_name = []
    stripped_altitude = []

    for i, point in enumerate(sorted_zip):
        if (
            (point[3] != "none" or point[4] != "none")
            or (i == 0 and (point[0] != sorted_zip[i + 1][0]))
            or (point[0] != sorted_zip[i - 1][0] and point[0] != sorted_zip[i + 1][0])
        ):  # If the Point has an Instruction, keep it
            stripped_time.append(point[0])
            stripped_latitude.append(point[1])
            stripped_longitude.append(point[2])
            stripped_instruction.append(point[3])
            stripped_name.append(point[4])
            if i!=0:
                stripped_altitude.append(sorted_zip[i-1][5])
            else:
                stripped_altitude.append(sorted_zip[i + 1][5])

    for i in range(0, len(name) - 1):
        if name[i] == name[i + 1]:
            instruction[i + 1] = 15

    decoded_gpx = {
        "latitude": stripped_latitude,
        "longitude": stripped_longitude,
        "altitude": stripped_altitude,
        "Instruction": stripped_instruction,
        "name": stripped_name,
    }
    return decoded_gpx


def decode_gpx_gmaps(gpx_path):
    # This function does not seem to work/I don't know what GPX format it
    # is supposed to be used with.
    gpx_file = open(gpx_path, "r")
    latitude = []
    longitude = []
    altitude = []
    instruction = []
    name = []
    for line in gpx_file:
        ins = "null"
        if line.find("lat=") != -1:  # If the line contains a latitude value
            lat = line.split('"')[1]
            latitude.append(lat)  # Store latitude
            lon = line.split('"')[3]
            longitude.append(lon)  # Store longitude
            ins = "none"
            instruction.append(ins)  # Store no Instruction
            alt = 0
            altitude.append(alt)
            nam = ""
            name.append(nam)
        if line.find("<cmt>") != -1:
            ins = line.lstrip().removeprefix("<cmt>").removesuffix("</cmt>\n")
            instruction.pop()
            instruction.append(ins)
        if line.find("<ele>") != -1:
            alt = line.lstrip().removeprefix("<ele>").removesuffix("</ele>\n")
            altitude.pop()
            altitude.append(alt)

    decoded_gpx = {
        "latitude": latitude,
        "longitude": longitude,
        "altitude": altitude,
        "Instruction": instruction,
        "name": name,
    }

    return decoded_gpx
    # if line.find()


def decode_gpx(gpx_path):
    gpx_file = open(gpx_path, "r")
    line = gpx_file.read()
    if "<name>openrouteservice</name>" in line:
        decoded_gpx = decode_gpx_ors(gpx_path), "ors"
    elif "<desc>Route created on plotaroute.com</desc>" in line:
        decoded_gpx = decode_gpx_plotaroute(gpx_path), "par"
    else:
        decoded_gpx = decode_gpx_gmaps(gpx_path), "gmp"

    return decoded_gpx
