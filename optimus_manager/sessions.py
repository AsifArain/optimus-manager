from optimus_manager.bash import exec_bash, BashError


class SessionsError(Exception):
    pass


def logout_all_desktop_sessions():

    print("Logging out any open desktop session")

    sessions_list = _get_sessions_list()

    for session_id in sessions_list:
        session_type = _get_session_type(session_id)
        if session_type == "x11" or session_type == "wayland":
            _terminate_session(session_id)


def is_there_a_wayland_session():

    sessions_list = _get_sessions_list()

    for session_id in sessions_list:
        session_type = _get_session_type(session_id)
        if session_type == "wayland":
            return True
    else:
        return False


def _get_sessions_list():

    try:
        sessions_list_str = exec_bash("loginctl list-sessions --no-legend | awk '{print $1}'").stdout.decode('utf-8')[:-1]
    except BashError as e:
        raise SessionsError("Cannot list sessions : %s" % str(e))

    sessions_list = list(sessions_list_str.splitlines())

    return sessions_list


def _get_session_type(session_id):

    try:

        session_info = exec_bash("loginctl show-session %s" % session_id).stdout.decode('utf-8')[:-1]

    except BashError as e:
        raise SessionsError("Error checking type of session %s : error running loginctl : %s" % (session_id, str(e)))

    for line in session_info.splitlines():
        if "Type=" in line:
            equal_sign_index = line.find("=")
            session_type = line[equal_sign_index+1:]
            return session_type
    else:
        raise SessionsError("Error checking type of session %s : no Type value")


def _terminate_session(session_id):

    try:
        exec_bash("loginctl terminate-session %s" % session_id)
    except BashError as e:
        raise SessionsError("Error terminating session %s : error running loginctl : %s" % (session_id, str(e)))
