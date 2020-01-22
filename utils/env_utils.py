import os
import utils.constants as const


def check_env_variables():
    if const.TRANSLATE_ENV_VAR not in os.environ:
        print(const.WARNING, 'Please set the ', const.TRANSLATE_ENV_VAR, ' Environment Variable to continue....', const.END)
        return False
    if const.MYSQL_PASS_ENV_VAR not in os.environ:
        print(const.WARNING, 'Please set the ', const.MYSQL_PASS_ENV_VAR, ' Environment Variable to continue....', const.END)
        return False
    if const.MYSQL_HOST_ENV_VAR not in os.environ:
        print(const.WARNING, 'Please set the ', const.MYSQL_HOST_ENV_VAR, ' Environment Variable to continue....', const.END)
        return False
    return True
