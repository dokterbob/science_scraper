#!/usr/bin/env python

import argparse
import os
import sys
import importlib

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('module')
	args = parser.parse_args()
	module_name = args.module

	current_dir = os.path.dirname(os.path.abspath(__file__))

	os.environ.setdefault("JATS_DIR", os.path.join(current_dir, "jats_files"))
	os.environ.setdefault("DOWNLOAD_DIR", os.path.join(current_dir, "fulltext"))

	sys.path.append(current_dir)

	module = importlib.import_module(module_name)

if __name__ == '__main__':
    main()
