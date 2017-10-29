# coding: utf-8
import os

def start_extract(configVarMap, secret_path = "secret-data", kv_separator = ":", hierarchy_separator = "-"):	
	if os.path.isdir(secret_path):
		for file_path in os.listdir(secret_path):
			if file_path == "__init__.py":continue
			if os.path.isfile(secret_path + "/" + file_path):
				with open(secret_path + "/" + file_path) as hfile:
					__parse_configuration(hfile, configVarMap, kv_separator, hierarchy_separator)
	else:
		raise Exception("Not valid configuration data path: " + secret_path)

def __parse_configuration(hfile, configVarMap, kv_separator, hierarchy_separator):
	for line in hfile:
		line = line.strip()
		if line is not "":
			try:
				keychain, value = line.split(kv_separator, 1)
				keys = keychain.split(hierarchy_separator)
				var_name = None
				configVar = configVarMap
				for key in keys[:-1]:
					var_name = key
					if var_name in configVar:
						configVar = configVar[var_name]
					else:
						configVar = None
						break
				if configVar is not None and keys[-1] in configVar:
					configVar[keys[-1]] = value	
			except:
				pass