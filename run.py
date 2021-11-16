# -*- coding: utf-8 -*-
from files import files
from converter import converter
from shell import shell
from messages import *
import sys

# Arguments variations
repo = ["shaders-repo", "fxr"]
branch = ["shaders-branch", "fxb"]
preset = ["preset", "p"]
exclude_shaders = ["ignore-shaders", "fxi"]
verbose = ["verbose"]
include_shaders = ["include-shaders-dir"]
cache = ["use-cached-shaders"]
output_dir = ["output-dir"]

# Get script arguments
shell.get_args(sys.argv)

# Verifies if user want's to see help menu
if (shell.get_arg("help")):
  print(help_str)
  sys.exit()

# Add exclude rules
files.add_excludes(shell.get_arg(exclude_shaders))

# Init temp dirs and download shaders
files.init_temp_dirs(shell.get_arg(cache))
shell.download_shaders(shell.get_arg(repo), shell.get_arg(branch), shell.get_arg(cache))

# Get ini configurations
settings = files.get_preset_ini(shell.get_arg(preset))

# Loop settings to convert files
debug = shell.get_arg(verbose)
for shader in settings["configurations"]:
  old_shader_file = files.get_shader_content(shader)
  new_shader_file = converter.update_file(shader, old_shader_file, settings["configurations"][shader], debug)

  files.write_new_temp_shader(new_shader_file, shader)

# Get reshade core to shaders path, and copy textures folder to prevent errors
files.copy_reshade_core_to_temp()
files.copy_reshade_textures_to_temp()

# Create vkBasalt.conf file
output_dir_path = files.create_conf(settings["effects"], shell.get_arg(output_dir))

# Move converted files to output dir
shell.move_temp_to_output(output_dir_path)
