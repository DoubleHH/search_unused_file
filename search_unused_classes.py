#! /usr/bin/python
# -*- coding:utf-8 -*-

import os
import time
import glob
import re
from sys import argv
import hh_print
from optparse import OptionParser
import linecache

def class_name_from_implemetation_string(string):
	if not string:
		return None
	start_flag = "@implementation"
	end_flags = ["{", "("]
	start = string.find(start_flag)
	if start == -1:
		return None
	start = start + len(start_flag)
	for flag in end_flags:
		end = string.find(flag, start)
		if end != -1:
			break
	if end == -1:
		end = len(string)
	result = string[start:end].strip()
	return result

def class_name_from_interface_string(string):
	if not string:
		return None
	start_flag = "@interface"
	end_flags = [":", "("]
	start = string.find(start_flag)
	if start == -1:
		return None
	start = start + len(start_flag)
	for flag in end_flags:
		end = string.find(flag, start)
		if end != -1:
			break
	if end == -1:
		return None
	result = string[start:end].strip()
	return result

def path_from_interface_string(string):
	if not string:
		return None
	end = string.find(":")
	if end == -1:
		return None
	result = string[0:end].strip()
	result = result.split('/')[-1]
	return result

def find_all_classes(path):
	command = 'ag --objc " *@interface +\w* *:" %s' % (path)
	search_results = os.popen(command).readlines()
	classes_set = set()
	classes_info = []
	duplicate_files = []
	for line in search_results:
		clean_line = line.strip()
		interface = class_name_from_interface_string(clean_line)
		# print clean_line
		# print interface
		if interface and interface not in classes_set:
			classes_set.add(interface)
			classes_info.append([interface, path_from_interface_string(clean_line)])
		else:
			duplicate_files.append(interface)
	hh_print.print_array(duplicate_files, "可能存在重复定义或者在文件夹内但没有拖进工程的文件", "b_red")
	return classes_info

def class_name_of_the_line(file_path, line_number):
	lines = linecache.getlines(file_path)
	count = len(lines)
	class_name = None
	is_in_note_block = False
	is_in_double_note = False
	for x in range(line_number,0,-1):
		print ("line:" + str(x))
		single_line = lines[x].strip()
		hh_print.print_color_string("single_line :" + single_line)
		if len(single_line) == 0:
			continue
		if single_line.endswith('*/'):
			if not single_line.startswith('/*'):
				is_in_note_block = True
			else:
				continue
		if single_line.startswith('/*'):
			if is_in_note_block:
				is_in_note_block = False
				continue
			else:
				# indicate the line is in note block
				is_in_double_note = True
				break
		if single_line.startswith('/') or single_line.startswith('#pragma'):
			continue
		if cmp(single_line, "@end") == 0:
			break
		if single_line.startswith('@interface'):
			class_name = class_name_from_interface_string(single_line)
		elif single_line.startswith('@implementation'):
			class_name = class_name_from_implemetation_string(single_line)
		print ("class_name from singleline: %s" % class_name)
		if class_name != None:
			break
	return [is_in_double_note, class_name]

def is_used_class(class_info, path):
	class_name = class_info[0]
	class_path = class_info[1]
	command = 'ag --objc -w %s %s' % (class_name, path)
	search_results = os.popen(command).readlines()
	for one_result in search_results:
		clean_one = one_result.strip()
		params = clean_one.split(':')
		if len(params) < 3:
			continue
		file_path = params[0]
		line_number = params[1]
		code = ':'.join(params[2:]).strip()
		# hh_print.print_color_string("file_path: " + file_path)
		# hh_print.print_color_string("line_number: " + line_number)
		# hh_print.print_color_string("code: " + code)
		prefixs = ['/', '#import', '@interface', '@implementation', '#pragma']
		is_hit_prefix = False
		for prefix in prefixs:
			if code.startswith(prefix):
				is_hit_prefix = True
				break
		if is_hit_prefix:
			continue
		name_result = class_name_of_the_line(file_path, int(line_number) - 1)
		if name_result[0]:
			hh_print.print_color_string("class in note: %s" % (class_name), "b_red")
			continue
		class_name_for_current_line = name_result[1]
		# hh_print.print_color_string("class_name_for_current_line : %s" % class_name_for_current_line)
		if not class_name_for_current_line or cmp(class_name_for_current_line, class_name) != 0:
			hh_print.print_color_string("class not match: %s, %s" % (class_name, class_name_for_current_line), "b_red")
			return True
	hh_print.print_color_string("False", "b_red")
	return False

if __name__ == '__main__':
    if len(argv) < 2:
    	hh_print.print_color_string("Parameters error: Usage: python %s source_path search_path" % (__file__), "b_red")
    	exit(0)
    source_path = argv[1]
    if len(argv) > 2:
    	search_path = argv[2]
    else:
    	search_path = source_path
    classes = find_all_classes(source_path)
    hh_print.print_array(classes, "所有类")
    unused_classes = []
    for class_ext in classes:
    	result = is_used_class(class_ext, search_path)
    	if not result:
    		unused_classes.append(class_ext)
    hh_print.print_array(unused_classes, "所有没有被使用的类")
    # progress = 0
    # total = len(files)
    # for file_path in files:
    # 	check_single_file(file_path)
    # 	hh_print.print_progress(progress, total)
    # 	progress = progress + 1

    # current_line = '       NSArray *itemArray = [subview valueForKeyPath:@"_viewData.item"];'
    # group = re.match(r'.*[^A-Za-z0-9_"]_[A-Za-z0-9].*', current_line)
    # if group == None:
    # 	print "None..."
    # else:
    # 	print group.group()
    