"""
Logger for actions

@author Derek Garcia
"""
import datetime
import json

global DEFAULT_LOG_PATH, LOG_PATH
DEFAULT_LOG_PATH = "quotebot_log.json"


def init_log(log_path=None):
    """
    Inits the log files on boot-up

    :param log_file_name: optional log file name
    """

    # set log file to given, else use default
    global LOG_PATH
    if log_path is not None:
        LOG_PATH = f"{log_path}.json"
    else:
        LOG_PATH = f"{DEFAULT_LOG_PATH}"

    # Make new file if needed, load data otherwise
    try:
        f = open(LOG_PATH)
        f.close()
    except FileNotFoundError:
        f = open(LOG_PATH, "x")
        f.write('{"logs": []}')
        f.close()

    return


def log(user, action, is_success, add_info=None):
    """
    Logs action into data log

    :param user: User who performed action
    :param action: Action
    :param is_success: result of action
    :param add_info: any additional info, optional
    :return:
    """
    # Get log data
    global LOG_PATH
    with open(LOG_PATH) as log_file:
        data = json.load(log_file)

    # make report
    report = {
        'id': len(data['logs']),
        'time': str(datetime.datetime.now()),
        'user': str(user),
        'action': str(action),
        'is_success': str(is_success),
        'add_info': "null"
    }

    # add extra info if given
    if add_info is not None:
        report['add_info'] = str(add_info)

    # update data
    data['logs'].append(report)

    # update file
    with open(LOG_PATH, "w") as log_file:
        log_file.write(json.dumps(data, indent=4))

    return
