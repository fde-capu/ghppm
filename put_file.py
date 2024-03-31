#!/usr/bin/env python3

import subprocess
import shutil
import os
import tempfile
import json
import sys
import argparse

def clone_and_copy_files(repo_info_list):
	for repo_info in repo_info_list:
		with tempfile.TemporaryDirectory() as temp_dir:
			clone_command = ['git', 'clone', repo_info['url'], temp_dir]
			subprocess.run(clone_command, check=True)
			for file in repo_info['file']:
				src_path = os.path.join(temp_dir, file)
				dest_path = os.path.join(os.getcwd(), file)
				shutil.copy(src_path, dest_path)

def pretty_print_repo_info(repo_info_list):
	for i, repo_info in enumerate(repo_info_list, start=1):
		print(f"Repository {i}:")
		print(f" URL: {repo_info['url']}")
		print(" Files to copy:")
		for file in repo_info['file']:
			print(f"	- {file}")
		print()

def load_repo_info_from_file():
	file_path = os.path.join(os.getcwd(), 'repo_info.json')
	if not os.path.exists(file_path):
		print(f"File {file_path} does not exist.")
		return []
	with open(file_path, 'r') as file:
		repo_info_list = json.load(file)
	return repo_info_list

def parse_arguments():
	parser = argparse.ArgumentParser(description='Personal package manager')
	parser.add_argument('--config', nargs='?', const='get', help='Set or get a persistent configuration for a variable.')
	return parser.parse_args()

def get_config(key):
	config_file = os.path.join(os.getcwd(), '.config')
	if os.path.exists(config_file):
		with open(config_file, 'r') as file:
			for line in file:
				if line.startswith(f"{key}="):
					return line.strip().split('=')[1]
	return None

def set_config(key, value):
	config_file = os.path.join(os.getcwd(), '.config')
	if not os.path.exists(config_file):
		with open(config_file, 'w') as file:
			file.write(f"{key}={value}\n")
	else:
		with open(config_file, 'r') as file:
			lines = file.readlines()
		key_exists = any(line.startswith(f"{key}=") for line in lines)
		if key_exists:
			with open(config_file, 'w') as file:
				for line in lines:
					if line.startswith(f"{key}="):
						file.write(f"{key}={value}\n")
					else:
						file.write(line)
		else:
			with open(config_file, 'a') as file:
				file.write(f"{key}={value}\n")

def main():
	args = parse_arguments()
	print(args)
	sys.exit()
	if args.config == 'get':
		username = get_config('github.user')
		if username:
			print(f"Current configured user name: {username}")
		else:
			print("No user name configured.")
	elif args.config:
		key, value = args.config, 'your_username'
		set_config(key, value)
		print(f"Configuration '{key}' set to '{value}'.")
	else:
		print("No configuration specified.")
	repo_info_list = load_repo_info_from_file()
	pretty_print_repo_info(repo_info_list)
	sys.exit()
	clone_and_copy_files(repo_info_list)

if __name__ == "__main__":
	main()
