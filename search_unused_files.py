#! /usr/bin/python
# -*- coding:utf-8 -*-

# 找出Xcode工程某个文件夹中未使用到的文件

import os
import re
from sys import argv
import hh_print

def find_all_headers(path):
	command = 'ag -lg "\.h$" %s' % (path)
	header_paths = os.popen(command).readlines()
	hh_print.print_color_string("总共有%s个文件。" % (len(header_paths)))
	return header_paths

def header_name_in_path(header_path):
	header_name = header_path.split('/')[-1]
	header_name = header_name[0 : (len(header_name) - 3)]
	return header_name

def result_of_search_single_file(search_path, name):
	command = 'ag -lw "%s" "%s"' % (name, search_path)
	name_paths = os.popen(command).readlines()
	name_header = name + ".h"
	name_implementation = name + ".m"
	pbxproj = ".pbxproj"
	for path in name_paths:
		if (name_header not in path) and (name_implementation not in path) and (pbxproj not in path):
			return True
	return False

def search_all_files_info(path, headers):
	index = 0
	total = len(headers)
	total_info = {}
	hh_print.print_color_string("Start searching ^_^ : ", "green")
	for temp_header_path in headers:
		index = index + 1
		header_name = header_name_in_path(temp_header_path)
		if "+" in header_name:
			continue
		hh_print.print_progress(index, total)
		result = result_of_search_single_file(path, header_name)
		total_info[header_name] = [result, temp_header_path.strip()]
	return total_info

def analyse_total_infos(total_infos):
	unused_files = []
	for key,result in total_infos.items():
		if not result[0]:
			unused_files.append(key + ": " + result[1])
	hh_print.print_array(unused_files, "未使用到的文件", "b_red")

if __name__ == '__main__':
    if len(argv) < 2:
    	hh_print.print_color_string("Parameters error: Usage: python %s search_path header_path(optional)" % (__file__), "b_red")
    	exit(0)
    search_path = argv[1]
    header_path = search_path
    if len(argv) > 2:
    	header_path = argv[2]
    all_headers_path = find_all_headers(header_path)
    total_infos = search_all_files_info(search_path, all_headers_path)
    analyse_total_infos(total_infos)
