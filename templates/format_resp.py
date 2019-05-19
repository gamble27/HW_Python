def _format_resp(self, resp_file, arg_list=None):
    """
    потому что сраный css со своими четырежды уебанными фигурными скобками не может блять не помешать
    :param resp_file: html file with response
    :param arg_list: list of tuples like this: ("param_name", value)
    :return: formatted response without any errors!
    """
    with open(resp_file) as f:
        lines = f.readlines()

    if arg_list is None:
        return ''.join(lines)

    for (key, value) in arg_list:
        for j, line in enumerate(lines):
            keyword = "{" + key + "}"
            if keyword in line:
                i = line.find(keyword)
                lines[j] = line[:i] + str(value) + line[i + len(keyword):]
    return ''.join(lines)