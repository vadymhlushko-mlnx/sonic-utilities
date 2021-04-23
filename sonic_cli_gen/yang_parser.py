#!/usr/bin/env python

try:
    import os
    import sys
    from config.config_mgmt import ConfigMgmt
except ImportError as e:
    raise ImportError("%s - required module not found" % str(e))


class YangParser:
    """ YANG model parser """
    def __init__(self,
                 yang_model):
        self.yang_model = yang_model
        self.conf_mgmt = None

        try:
            self.conf_mgmt = ConfigMgmt()
        except Exception as e:
            raise Exception("Failed to load the {} class".format(str(e)))
                
    def fail(self, e):
        print(e)
        raise e

    def yang_to_dict(self):
        yang_model_type = self._determine_yang_model_type()

        if (yang_model_type == 'static'):
            print('static')
            pass
        else:
            pass

    def _determine_yang_model_type(self):
        cond = True
        if cond:
            return 'static'
        else:
            return 'dynamic'