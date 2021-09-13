import os

yang_models_path = '/usr/local/yang-models'


def move_yang_models(test_path, test_name, test_yang_models):
    """ Move a test YANG models to known location """

    for yang_model in test_yang_models:
        src_path = os.path.join(test_path,
                                'cli_autogen_input',
                                test_name,
                                yang_model)
        cmd = 'sudo cp {} {}'.format(src_path, yang_models_path)
        os.system(cmd)


def remove_yang_models(test_yang_models):
    """ Remove a test YANG models to known location """

    for yang_model in test_yang_models:
        yang_model_path = os.path.join(yang_models_path, yang_model)
        cmd = 'sudo rm {}'.format(yang_model_path)
        os.system(cmd)


def backup_yang_models():
    """ Make a copy of existing YANG models """

    cmd = 'sudo cp -R {} {}'.format(yang_models_path, yang_models_path + '_backup')
    os.system(cmd)


def restore_backup_yang_models():
    """ Restore existing YANG models from backup """

    cmd = 'sudo cp {} {}'.format(yang_models_path + '_backup/*', yang_models_path)
    os.system(cmd)
    os.system('sudo rm -rf {}'.format(yang_models_path + '_backup'))
    