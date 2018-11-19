import re

# https://www.vatsim.net/pilot-resource-centre/general-lessons/interpreting-metars-and-tafs

def decode_metar_date(metar_date_string):
    day = metar_date_string[:2]
    time = metar_date_string[2:]
    return {'day':day, 'time': time}


def decode_metar_wind(metar_wind_string):
    direction = metar_wind_string[:3]
    speed = metar_wind_string[3:5]
    unit = re.findall('[a-zA-Z]+$', metar_wind_string)[0]
    wind_dict = {'direction':direction,
                 'speed': speed,
                 'unit': unit}
    if 'G' in metar_wind_string:
        gust_index = metar_wind_string.find('G') + 1
        wind_dict['gust'] = metar_wind_string[gust_index:gust_index+2]
    return wind_dict


def decode_metar_variable_wind(metar_variable_wind_string):
    varying_from_to = metar_variable_wind_string.split('V')
    return {
        'from': varying_from_to[0],
        'to': varying_from_to[1]
    }

def decode_metar_variable_visibility(metar_string):
    statute_viz_regex = """[[\d]{1,3}]* *[[\d]{0,2}[\/]*[\d]{0,2}SM]*"""
    meters_viz_regex = """ \d{4} """
    runway_visual_range_regex = """R\d{2}R/\d*[a-zA-Z]*"""

    statute_viz_result = re.findall(statute_viz_regex, metar_string)
    meters_viz_result = re.findall(meters_viz_regex, metar_string)
    runway_visual_range_result = re.findall(runway_visual_range_regex, metar_string)

    viz_dict = {}

    if statute_viz_result:
        viz_dict['Visibility']= statute_viz_result[0]
    if meters_viz_result:
        viz_dict['Visibility']= meters_viz_result[0]
    if runway_visual_range_result:
        viz_dict['Runway Visual Range']= runway_visual_range_result[0]

    return viz_dict


def decode_metar(metar_string):
    metar_parts = metar_string.split(' ')
    airfield = metar_parts[0]
    print('Airfield: {}'.format(airfield))

    metar_date_time = decode_metar_date(metar_parts[1])
    print('Day of current month: {}'.format(metar_date_time['day']))
    print('Time: {}'.format(metar_date_time['time']))

    metar_wind = decode_metar_wind(metar_parts[2])
    print('Direction: {}'.format(metar_wind['direction']))
    print('Speed: {}'.format(metar_wind['speed']))
    print('Unit: {}'.format(metar_wind['unit']))
    try:
        print('Gust: {}'.format(metar_wind['gust']))
    except KeyError:
        pass

    if 'V' in metar_parts[3]:
        varying_wind = decode_metar_variable_wind(metar_parts[3])
        print('Varying from: {}'.format(varying_wind['from']))
        print('Varying to: {}'.format(varying_wind['to']))


    decoded_metar_visibility = decode_metar_variable_visibility(metar_string)
    for part in decoded_metar_visibility:
        print('{}: {}'.format(part, decoded_metar_visibility[part]))






metar = "KJAX 020256Z 02003KT 10SM TSRA OVC01OCB SCT100 BKN130 18/17 A2996"
decode_metar(metar)

print("===========================")
metar = "KPIT 151124Z 28016G20KT 2 3/4SM R28R/2600FT TSRA OVC01OCB 18/16 A2992 RMK SLPO13 T01760158 "
decode_metar(metar)

print("===========================")
metar = "EGLL 060326Z 20013G23KT 8000 SCT014 BKN025 Q1013 "
decode_metar(metar)

print("===========================")
metar = "EGLL 060326Z 20013G23KT 180V260 8000 SCT014 BKN025 Q1013 "
decode_metar(metar)

print("===========================")
metar = "EGPH 111150Z 10004KT 070V130 9999 FEW020 08/07 Q0990"
decode_metar(metar)