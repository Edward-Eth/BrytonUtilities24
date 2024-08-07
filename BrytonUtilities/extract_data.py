from geopy import distance


def safediv(num, den):
    if den == 0:
        if num == 0:
            return 0
        elif num > 0:
            return 9999
        else:
            return -9999
    else:
        return num / den


def add_poi_to_instructions(
    instruction_distance, instruction_data, points_of_interest, name_data
):
    poi_name = points_of_interest[0][0]
    poi_type = points_of_interest[0][1]
    poi_distance = points_of_interest[0][2]
    poi_identification = points_of_interest[0][3]

    for i in range(0, len(poi_name)):
        instruction_data.append(poi_type)
        instruction_distance.append(poi_distance)
        name_data.append(poi_name)

    return [instruction_data, instruction_distance, name_data, poi_identification]


# work in progress
def add_poi_by_climb(points_of_interest, point_attribute):
    distance_from_last_point = point_attribute["DistFromLastPoint"]
    altitude_from_last_point = point_attribute["AltFromLastPoint"]

    # for i in range(0,len(distance_from_last_point)):
    #   print(distance_from_last_point[i],altitude_from_last_point[i])
    poi_name = []
    poi_type = []
    poi_distance = []
    poi_identification = []

    mountain_start = 0
    mountain_finish = 0
    mountain = []

    distance_from_start = [0.0]

    # creates array indicating distance from start for each Point
    for i in range(1, len(distance_from_last_point)):
        distance_from_start.append(
            distance_from_start[i - 1] + distance_from_last_point[i]
        )

    i = 0
    while i < len(distance_from_last_point):
        in_mountain = False
        current_distance = 0
        current_delta_altitude = 0
        for j in range(i + 1, len(distance_from_last_point)):
            current_distance += distance_from_last_point[j]
            current_delta_altitude += altitude_from_last_point[j]
            if current_distance >= 500:
                grade = (current_delta_altitude / current_distance) * 100
                if (grade >= 3) and (
                    safediv(altitude_from_last_point[j], distance_from_last_point[j])
                    * 100
                    > -2
                ):
                    climb_score = grade * current_distance
                    if climb_score >= 3500:
                        if not in_mountain:
                            mountain_start_point = i
                            mountain_start_distance = distance_from_start[i]
                            in_mountain = True
                    else:
                        if in_mountain:
                            mountain_finish_point = j
                            mountain_finish_distance = distance_from_start[j]

                        break
                else:
                    if in_mountain:
                        mountain_finish_point = j
                        mountain_finish_distance = distance_from_start[j]

                    break
        i += 1
        if in_mountain:
            poi_name.append(
                "st "
                + str(int(grade))
                + "% "
                + str(
                    int(
                        float(
                            (mountain_finish_distance - mountain_start_distance)
                            / 1000.0
                        )
                    )
                )
                + "km"
            )
            poi_type.append(b"\x65")
            poi_distance.append(mountain_start_distance)
            poi_identification.append(mountain_start_point)

            poi_name.append(
                "end"
                + str(int(current_delta_altitude))
                + "m "
                + str(int(climb_score))
                + "sc"
            )
            poi_type.append(b"\x65")
            poi_distance.append(mountain_finish_distance)
            poi_identification.append(mountain_finish_point)

            i = j

    points_of_interest = [poi_name, poi_type, poi_distance, poi_identification]

    return points_of_interest


def add_poi_by_distance(points_of_interest, point_attribute, inserted_poi):
    distance_from_last_point = point_attribute[0]
    altitude_from_last_point = point_attribute[1]

    poi_name = inserted_poi[0]
    poi_type = inserted_poi[1]
    poi_distance = inserted_poi[2]
    poi_identification = 0
    distance_from_start = 0
    for i in range(0, len(point_attribute)):
        distance_from_start += distance_from_last_point[i]
        if float(poi_distance) < distance_from_start:
            poi_identification = i - 1
            poi_distance = distance_from_start - distance_from_last_point[i]
            break

    points_of_interest.append([poi_name, poi_type, poi_distance, poi_identification])

    return points_of_interest


def calculate_points_attributes(latitude_data, longitude_data, altitude_data):
    distance_from_last_point = [0]
    distance_to_point = [0]
    delta_altitude_from_last_point = [0]

    for i in range(1, len(latitude_data)):
        current_point = (latitude_data[i] / 1000000, longitude_data[i] / 1000000)
        last_point = (latitude_data[i - 1] / 1000000, longitude_data[i - 1] / 1000000)
        distance_from_last_point.append(distance.distance(current_point, last_point).m)
        distance_to_point.append(distance_to_point[i - 1] + distance_from_last_point[i])
        delta_altitude_from_last_point.append((altitude_data[i] - altitude_data[i - 1]))

    point_attributes = {
        "DistFromLastPoint": distance_from_last_point,
        "PointDistance": distance_to_point,
        "AltFromLastPoint": delta_altitude_from_last_point,
    }

    return point_attributes


def calculate_instruction_distance(instruction_data, latitude_data, longitude_data):
    current_instruction_point = (latitude_data[0], longitude_data[0])
    # iterates over each Point excluding last
    current_instruction_distance = 0
    instruction_distance = [0]
    for i in range(0, len(instruction_data) - 1):
        current_point = (latitude_data[i] / 1000000, longitude_data[i] / 1000000)
        next_point = (latitude_data[i + 1] / 1000000, longitude_data[i + 1] / 1000000)
        current_instruction_distance += distance.distance(current_point, next_point).m

        if instruction_data[i + 1] != b"\xff":
            instruction_distance.append(int(float(current_instruction_distance)))
            current_instruction_distance = 0
        else:
            instruction_distance.append(int(0))

    return instruction_distance


def calculate_number_data(instructions_data, points_of_interest):
    number_points = len(instructions_data)
    number_instructions = 0
    for instruction_point in instructions_data:
        if instruction_point != b"\xff":
            number_instructions += 1

    number_pois = len(points_of_interest[0])

    number_data = [number_points, number_instructions, number_pois]
    return number_data


def calculate_alt_bounding_box(altitude_data):
    maximum_altitude = max(altitude_data)
    minimum_altitude = min(altitude_data)

    alt_bounding_box = [maximum_altitude, minimum_altitude]
    return alt_bounding_box


def calculate_distance_between_points(latitude_data, longitude_data):
    # iterates over each Point excluding last
    distance_between_points = []
    for i in range(0, len(latitude_data) - 1):
        current_point = (latitude_data[i] / 1000000, longitude_data[i] / 1000000)
        next_point = (latitude_data[i + 1] / 1000000, longitude_data[i + 1] / 1000000)
        distance_between_points.append(distance.distance(current_point, next_point).m)

    return distance_between_points


def calculate_total_distance(latitude_data, longitude_data):
    # iterates over each Point excluding last
    total_distance = 0
    for i in range(0, len(latitude_data) - 1):
        current_point = (latitude_data[i] / 1000000, longitude_data[i] / 1000000)
        next_point = (latitude_data[i + 1] / 1000000, longitude_data[i + 1] / 1000000)
        total_distance += distance.distance(current_point, next_point).m

    return total_distance


def calculate_lat_lon_bounding_box(latitude_data, longitude_data):
    # maximum latitude
    lat_ne_bounding_box = max(latitude_data)
    # minimum latitude
    lat_sw_bounding_box = min(latitude_data)
    # maximum longitude
    lon_ne_bounding_box = max(longitude_data)
    # minimum longitude
    lon_sw_bounding_box = min(longitude_data)

    lat_lon_bounding_box = [
        lat_ne_bounding_box,
        lat_sw_bounding_box,
        lon_ne_bounding_box,
        lon_sw_bounding_box,
    ]
    return lat_lon_bounding_box


def extract_attributes(converted_data):
    latitude_data = converted_data["latitude"]
    longitude_data = converted_data["longitude"]
    altitude_data = converted_data["altitude"]
    instruction_data = converted_data["Instruction"]
    points_of_interest = []

    lat_lon_bounding_box = calculate_lat_lon_bounding_box(latitude_data, longitude_data)

    total_distance = calculate_total_distance(latitude_data, longitude_data)

    alt_bounding_box = calculate_alt_bounding_box(altitude_data)

    instruction_distance = calculate_instruction_distance(
        instruction_data, latitude_data, longitude_data
    )

    point_attribute = calculate_points_attributes(
        latitude_data, longitude_data, altitude_data
    )

    # points_of_interest = add_poi_by_distance(points_of_interest, point_attribute,inserted_poi)

    points_of_interest = add_poi_by_climb(points_of_interest, point_attribute)

    number_data = calculate_number_data(instruction_data, points_of_interest)

    extracted_attributes = {
        "lat_lon_bounding_box": lat_lon_bounding_box,
        "total_distance": total_distance,
        "alt_bounding_box": alt_bounding_box,
        "number_data": number_data,
        "instruction_distance": instruction_distance,
        "points_distance": point_attribute["PointDistance"],
        "points_of_interest": points_of_interest,
    }

    return extracted_attributes
