import logging

data_points = []


def parse_file(input_file_name):
    logging.debug(f'file is: {input_file_name}')
    with open(input_file_name, 'r') as input_file:
        for line_num, line in enumerate(input_file):
            _parse_line(line_num, line)
    return data_points


def _parse_line(line_num, line):
    line_split = line.split()
    if _is_valid(line_split):
        data_points.append(tuple(int(x) for x in line_split))
    else:
        logging.error(f'failed to process line number {line_num + 1}. line is: [{line.strip()}]')


def _is_number(element):
    try:
        float(element)
    except ValueError:
        return False
    return True


def _is_dim_equal_to_prev_line(line):
    if len(data_points) == 0: return True
    return len(line) == len(data_points[-1])


def _is_valid(line):
    if len(line) == 0:
        return False
    for element in line:
        if not _is_number(element):
            return False
    if not _is_dim_equal_to_prev_line(line):
        logging.error(f'failed to process line: more elements than previous line.')
        return False
    return True