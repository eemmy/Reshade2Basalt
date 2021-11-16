# -*- coding: utf-8 -*-
from shell import shell
import shutil
import sys
import os

class Files:
  def __init__(self):
    self.pwd = os.getcwd() + "/"
    self.ini_path = self.pwd + "preset.ini"
    self.shaders_path = self.pwd + ".temp/shaders/Shaders/"

    self.replace_shaders_rules = {
      "BloomAndLensFlares.fx": "Bloom.fx"
    }

    self.exclude_shaders_rules = [
      "Tint.fx",
      ""
    ]


  def add_excludes(self, extra_excludes = False):
    if extra_excludes != False:
      extra_excludes = extra_excludes.split(",")

      for extra in extra_excludes:
        if extra.find(".fx") == -1:
          extra = extra + ".fx"
        
        self.exclude_shaders_rules.append(extra)
        pass
      pass
    pass

  def init_temp_dirs(self, use_cache = False):
    # Verifies if temp dir exists, and remove it case exists
    if os.path.exists("{}.temp".format(self.pwd)):
      try:
        if use_cache:
          shutil.rmtree("{}.temp/output".format(self.pwd))
        else:
          shutil.rmtree("{}.temp".format(self.pwd))
      except:
        print("Error when trying to delete old temporary dir")
        sys.exit()
    
    # Create temporary directories
    try:
      if use_cache == False:
        os.mkdir(".temp")
        os.mkdir(".temp/shaders/")
      
      os.mkdir(".temp/output/")
      os.mkdir(".temp/output/shaders")
    except:
      print("Error when trying to create temporary directories.")
      sys.exit()

  def get_preset_ini(self, path = False):
    # Verifies if preset file is a custom one or default
    if path == False:
      path = self.ini_path
    
    # Verifies if preset exists
    if not os.path.exists(path):
      print("Cannot found preset file. Informed path: {}".format(path))
      sys.exit()

    file_contents = open(path, "r").read()
    settings = {
      "effects": [],
      "configurations": {}
    }

    # Get used effects
    effects = file_contents.split("Techniques=")[1].split("TechniqueSorting=")[0].replace(" ", "").replace("\n", "").split(",")
    
    # Get effects names
    for effect in effects:
      if effect.find(".fx") == -1:
        effect = effect + ".fx"

      # Treat replace rule for shader name, if was
      if effect in self.replace_shaders_rules:
        effect = self.replace_shaders_rules[effect]

      # Exclude shader if it is not supported
      if effect in self.exclude_shaders_rules:
        continue

      settings["effects"].append(effect)

    # Get effects settings
    for effect in settings['effects']:
      try:
        effect_key = "[{}]\n".format(effect)
        effect_settings = file_contents.split(effect_key)[1].split("\n\n")[0].split("\n")

        settings["configurations"][effect] = effect_settings
      except:
        print("Shader {} not found, add it to extra shaders or ignore this file".format(effect))
        sys.exit()

    return settings
  
  def get_shader_content(self, shader):
    # Verifies if shader exists
    if not os.path.exists(self.shaders_path + shader):
      print("Shader file {} not exists".format(self.shader))
      sys.exit()

    content = open(self.shaders_path + shader, "r").read()

    return content

  def write_new_temp_shader(self, file_content, filename):
    try:
      new_file = open("{}.temp/output/shaders/{}".format(self.pwd, filename), "w")
      new_file.write(file_content)
      new_file.close()
    except:
      print("Error when trying to write new shader file in temp folder. Filename: " + filename)
      sys.exit()

  def copy_reshade_core_to_temp(self):
    try:
      current_path = [
        self.pwd + ".temp/shaders/Shaders/ReShade.fxh",
        self.pwd + ".temp/shaders/Shaders/ReShadeUI.fxh"
        ]
      new_path = [
        self.pwd + ".temp/output/shaders/ReShade.fxh",
        self.pwd + ".temp/output/shaders/ReShadeUI.fxh"
      ]
      
      shutil.copyfile(current_path[0], new_path[0])
      shutil.copyfile(current_path[1], new_path[1])
    except:
      print("Error when trying to copy Reshade Core file to temporary output folder.")
      sys.exit()

  def copy_reshade_textures_to_temp(self):
    try:
      current_path = self.pwd + ".temp/shaders/Textures/"
      new_path = self.pwd + ".temp/output/textures/"
      
      shutil.copytree(current_path, new_path)
    except:
      print("Error when trying to copy Reshade Textures to temporary output folder.")
      sys.exit()

  def create_conf(self, effects, output_dir = False):
    # Verifies if user want to use default output dir
    if output_dir == False:
      output_dir = self.pwd + "output"

    # Verifies if output dir exists, and han
    if os.path.exists(output_dir):
      create_dir = input("Output directory already exists. Want to overwrite it? [S/n]: ")

      if create_dir == "n" or create_dir == "N":
        print("Exiting the program")
        sys.exit()
      else:
        os.system("cd {} && rm -rf * && rm -rf .*".format(output_dir))
    else:
      os.system("mkdir {}".format(output_dir))

    if output_dir[-1] != "/":
      output_dir = output_dir + "/"

    # Variables
    textures_path = output_dir + "textures/"
    shaders_path = output_dir + "shaders/"
    used_effects_str = "effects = "
    effects_path_str = ""

    # Loop effects to build file
    for effect in effects:
      name = effect.lower().replace(".fx", "")

      used_effects_str += "{}:".format(name)
      effects_path_str += "{} = {}{}\n    ".format(name, shaders_path, effect)

    file_content = """
    reshadeTexturePath = {}
    reshadeIncludePath = {}

    {}

    {}
    """.format(textures_path, shaders_path, effects_path_str, used_effects_str[:-1]).replace("    ", "")

    # Write config file
    conf_file = open(self.pwd + ".temp/output/vkBasalt.conf", "w")
    conf_file.write(file_content)
    conf_file.close()

    return output_dir

    
files = Files()
