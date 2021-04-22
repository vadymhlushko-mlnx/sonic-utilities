#!/usr/bin/env python

try:
    import os
    import sys
    import glob
    import yang as ly
except ImportError as e:
    raise ImportError("%s - required module not found" % str(e))


YANG_DIR = "/usr/local/yang-models/"

class YangParser:
    """ YANG model parser """
    def __init__(self,
                 yang_model):
        self.yang_model = yang_model
        self.ly_ctx = None

        try:
            self.ly_ctx = ly.Context(YANG_DIR)
        except Exception as e:
            self.fail(e)
                
    def fail(self, e):
        print(e)
        raise e

    def yang_to_dict(self):
        print ("YANG TO DICT")
        data = {
            'yang_dir': YANG_DIR.
            'yang_files': glob
        }
        pass