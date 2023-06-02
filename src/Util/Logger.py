"""
Logger for actions

@author Derek Garcia
"""
import datetime
import json

global DEFAULT_LOG_FILE_NAME, LOG_PATH, LOG_FILE
DEFAULT_LOG_FILE_NAME = "quotebot_log.json"
LOG_FILE = {'logs': []}


def init_log(log_dir, log_file_name=None):
    """
    Inits the log files on boot-up

    :param log_dir: source directory to check for existing logs
    :param log_file_name: optional log file name
    """
    global LOG_PATH
    # set log file name if given, else default
    if log_file_name is None:
        LOG_PATH = f"{log_dir}/{DEFAULT_LOG_FILE_NAME}"
    else:
        LOG_PATH = f"{log_dir}/{log_file_name}.json"

    # Make new file if needed, load data otherwise
    try:
        f = open(LOG_PATH)
        global LOG_FILE
        LOG_FILE = json.load(f)
        f.close()
    except FileNotFoundError:
        f = open(LOG_PATH, "x")
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

    # make report
    report = {
        'id': len(LOG_FILE['logs']),
        'time': str(datetime.datetime.now()),
        'user': str(user),
        'action': str(action),
        'is_success': str(is_success),
        'add_info': "null"
    }

    # add extra info if given
    if add_info is not None:
        report['add_info'] = str(add_info)
    LOG_FILE['logs'].append(report)

    # update files
    with open(f"{LOG_DIR}/{LOG_FILE}", "w") as log_file:
        log_file.write(json.dumps(LOG_FILE, indent=4))

    return
