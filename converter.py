# -*- coding: utf-8 -*-
import sys
import os
import re

class Converter:
  def __init__(self):
    self.pwd = os.getcwd() + "/"

  def get_config_update(self, shader, config, new_val):
    # Add a identifier to isolate config from rest of file
    config_regex = r"(.+) {}?(.+)".format(config)
    config_start = re.sub(config_regex, r'|||||||\1 {}\2'.format(config), shader, count=1)
    config_end = "|||||||" + re.sub(r"> =(.+)", r"> =\1|||||||", config_start.split("|||||||")[1], count=1)

    # Get old config and new config string
    old_config = config_end.split('|||||||')[1]
    new_config = re.sub(r"\> \= (.+)", " > = {};".format(new_val) , old_config, count=1)

    return {
      "old": old_config,
      "new": new_config
    }

  def update_file(self, filename, shader, configs, verbose = False):
    if verbose:
      print("\nOperation: Converting file {}".format(filename))

    for config in configs:
      if config == '':
        continue

      # Get param name and new value
      param = config.split("=")[0]
      value = config.split("=")[1]

      if verbose:
        print("\n--------------------------------------------------------------------------------------------------------------------------------")
        print("Param: " + param)
        print("Value: {}\n".format(value))

      # Get and treat setting replaces
      replaces = self.get_config_update(shader, param, value)
      replaces["new"] = self.treat_update_values_conversion(replaces["old"], replaces["new"])

      if verbose:
        print("Replace: " + replaces["old"] + "\n")
        print("With: " + replaces["new"])
        print("--------------------------------------------------------------------------------------------------------------------------------")

      # Replace config in shader
      shader = shader.replace(replaces["old"], replaces["new"])
    
    return shader

  def treat_update_values_conversion(self, old, new):
    # Treatments conditions
    bool_cond = old.find("> = false") != -1 or old.find("> = true")
    float_cond = old.find("float3(") != -1 or old.find("float2(") != -1 or old.find("float4(") != -1

    # Treats booleans
    if bool_cond:
      new = new.replace("> = 0;", "> = false;")
      new = new.replace("> = 1;", "> = true;")

    # Treats float
    if float_cond:
      value = new.split("> = ")[1].replace(";", "")
      funcType = ""

      # Prevent errors with float type (2, 3 or 4 values)
      if old.find("float2(") != -1:
        funcType = "2"
      elif old.find("float3(") != -1:
        funcType = "3"
      elif old.find("float4(") != -1:
        funcType = "4"

      new = new.replace(value, "float{}({});".format(funcType, value))

    return new

converter = Converter()
