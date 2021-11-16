# -*- coding: utf-8 -*-
import sys
import os

# Handle shell operations, like shade repositories management.
class Shell:
  def __init__(self):
    self.shaders_repo = "https://github.com/crosire/reshade-shaders.git"
    self.shaders_branch = "master"
    self.shaders_package = "crosire/reshade-shaders"

    self.pwd = os.getcwd() + "/"

    self.args = {}

  def download_shaders(self, repo = False, branch = False, use_cached = False):
    # Verifies if user want's to use cached shaders
    if use_cached:
      if os.path.exists(self.pwd + ".temp/shaders/Shaders"):
        return
      else:
        print("Can't find cached shaders. Downloading from remote.\n")

    # Verifies if branch/repo are a custom one or the defaults
    if repo == False:
      repo = self.shaders_repo
    if branch == False:
      branch = self.shaders_branch

    # Download shaders repo
    try:
      os.system("git clone {} {}.temp/shaders/".format(repo, self.pwd))
      os.system("cd {}.temp/shaders && git checkout {}".format(self.pwd, branch))
    except:
      print("Error when trying to download git-repository {} from {}:{}".format(self.shaders_package, repo, branch))
      sys.exit()

  def get_args(self, args):
    args_dict = {}
    args.pop(0)
    
    # Add arguments to dict
    for arg in args:
      # Verifies if argument is invalid
      if arg.find("--") == -1 or arg.find("=") == -1:
        if "invalid" not in args_dict:
          args_dict["invalid"] = [ arg ]
        else:
          args_dict["invalid"].append(arg)
      else:
        key_val = arg.split("=")
        args_dict[key_val[0].replace("--", "")] = key_val[1]

    # Validates arguments
    self.validate_args(args_dict)
    
    self.args = args_dict

  def validate_args(self, args):
    if not "invalid" in args:
      return True

    for invalid_arg in args["invalid"]:
      print("Invalid argument {}".format(invalid_arg))

    print("\nPlease consult supported arguments and arguments syntax.")
    sys.exit()

  def get_arg(self, name):
    if isinstance(name, list):
      for n in name:
        if n in self.args:
          return self.args[n]

      return False
    else:
      if not name in self.args:
        return False
      else:
        return self.args[name]

  def move_temp_to_output(self, path):
    try:
      os.system("mv {}.temp/output/* {}".format(self.pwd, path))
    except:
      print("Error when trying to move temporary output folder to final destination.")
      sys.exit()

shell = Shell()
