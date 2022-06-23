# -*- coding: utf-8 -*-
import click
import configparser
from git import Repo
import logging
import os
from os.path import join as path_join
import re
import shutil
import sys
import tempfile

# TODO: Improve options help
# TODO: Remove constant "shaders" folder and put it as argument

# Use click (https://click.palletsprojects.com) to create a nice CLI
@click.command()
@click.option("--preset", "-p", default="preset.ini", show_default=True,
              help="Name of the preset .ini file to convert.")
@click.option("--output-dir", "-o", "output", default="output/")
@click.option("--shaders-repo", "-r", "repos", multiple=True,
              default=["https://github.com/crosire/reshade-shaders.git"], show_default=True)
@click.option("--shaders-branch-prompt", "-b", "branch",
              default=False, help="Ask to use different branches than master")
@click.option("--ignore-shaders", "-i", "ignored_shaders", multiple=True, type=str,
              help="Shader to ignore. Repeatable option.")
@click.option("--use-cached-shaders", "-c", "use_cache", default=True,
              help="Clear the shaders directory first")
@click.option("--verbose", "-v", "verbosity", count=True)  # Verbosity level unused for now, equivalent to boolean
def run(preset, output, repos, branch, ignored_shaders, use_cache, verbosity):
    logging.basicConfig(level=max(10, 40-verbosity*10))
    if os.path.exists(output):
        create_dir = input("Output directory already exists. Want to overwrite it? [y/N]: ")
        if create_dir.lower().strip() != "y":
            logging.warning("Exiting the program")
            sys.exit()
    os.makedirs(output, exist_ok=True)

    if not (use_cache and os.path.exists(".cache")):
        if os.path.exists(".cache"):
            confirm = input("Going to delete .cache! Continue? [y/N]")
            if confirm.lower != "y":
                sys.exit(1)
        shutil.rmtree(".cache", ignore_errors=True)
        os.makedirs(".cache", exist_ok=True)

        for repo in repos:
            cur_branch = "master"
            if branch:
                cur_branch = input(f"Branch to use for {repo} ? [master]") or "master"
            init_shaders(repo, cur_branch)

    # Create output folder structure
    out_shaders = path_join(output, "shaders/")
    out_textures = path_join(output, "textures/")
    os.makedirs(out_shaders, exist_ok=True)
    os.makedirs(out_textures, exist_ok=True)

    settings = get_preset_ini(preset, ignored_shaders)
    for shader, config in settings["configurations"].items():
        shader_path = path_join(".cache/Shaders", shader)
        try:
            with open(shader_path, "r") as f:
                old_shader_file = f.read()
        except FileNotFoundError as e:
            if "_" not in shader:
                raise
            logging.warning(f"{shader_path} not found, trying to find a subfolder...")
            new_path = path_join(".cache/Shaders", shader.split("_")[0], shader)
            with open(new_path, "r") as f:
                old_shader_file = f.read()
        logging.info(f"Converting shader {shader_path}")
        new_shader_file = update_file(old_shader_file, config, verbosity)
        with open(path_join(output, "shaders/", shader), "w") as f:
            f.write(new_shader_file)

    shutil.copy(".cache/Shaders/ReShade.fxh", out_shaders)
    shutil.copy(".cache/Shaders/ReShadeUI.fxh", out_shaders)
    shutil.copytree(".cache/Textures", out_textures, dirs_exist_ok=True)
    create_conf(settings["effects"], output)


def init_shaders(repo, branch):
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_dir = path_join(tmpdir)
        logging.info(f"Cloning repo {repo}")
        Repo.clone_from(repo, to_path=repo_dir, multi_options=[f"--branch={branch}"])
        shaders_path = path_join(repo_dir, "Shaders/")
        textures_path = path_join(repo_dir, "Textures/")

        if os.path.exists(shaders_path):
            shutil.copytree(shaders_path, ".cache/Shaders", dirs_exist_ok=True)
        if os.path.exists(textures_path):
            shutil.copytree(textures_path, ".cache/Textures", dirs_exist_ok=True)


def get_preset_ini(path, ignored_shaders):
    replace_shaders_rules = {"BloomAndLensFlares.fx": "Bloom.fx", "ADOF.fx": "DOF.fx",
                             "ContrastAdaptiveSharpen.fx": "CAS.fx"}
    exclude_rules = {"Tint.fx"}
    for ignored in ignored_shaders:
        if not ignored.endswith(".fx"):
            ignored += ".fx"
        exclude_rules.add(ignored)

    # Verifies if preset exists
    if not os.path.exists(path):
        logging.error("Cannot find preset file. Informed path: {}".format(path))
        sys.exit()

    # Read the content of the .ini file through configparser
    with open(path, "r") as f:
        contents = f.read()
    config = configparser.ConfigParser()
    config.optionxform = str  # Required to have case-sensitive keys
    try:
        config.read_string(path, source=path)
    except configparser.MissingSectionHeaderError:
        logging.warning("Invalid .ini, trying to add a [default] category")
        config.read_string("[root]\n"+contents, source=path)

    # TODO: This is partly redundant with configparser's structure, it could be done better
    settings = {
        "effects": [],
        "configurations": {}
    }

    # Get effects names
    for effect in {i.strip().split("@")[-1] for i in config["root"]["TechniqueSorting"].split(",")}:
        if not effect.endswith(".fx"):  # Is this needed (or even working as intended)?
            effect += ".fx"

        # Replace shader if a rule says so
        if effect in replace_shaders_rules:
            effect = replace_shaders_rules[effect]

        # Exclude shader if a rule says so
        if effect in exclude_rules:
            continue

        settings["effects"].append(effect)

    for effect in settings['effects']:
        try:
            settings["configurations"][effect] = dict(config[effect])
        except KeyError:
            logging.error(f"Shader {effect} not found, check config file (including filename-case), "
                          "that the shader exist, or add it to the ignored shaders")
            sys.exit()
    return settings


def create_conf(effects, output_dir):
    # Variables
    textures_path = path_join(output_dir, "textures/")
    shaders_path = path_join(output_dir, "shaders/")
    used_effects_str = "effects = "
    effects_path_str = ""

    # Loop effects to build file
    for effect in effects:
        if effect.lower().endswith(".fx"):
            name = effect[:-3]
        else:
            name = effect
        used_effects_str += f"{name}:"
        effects_path_str += f"{name} = {shaders_path}{effect}\n"

    file_content = "\n".join([
        f"reshadeTexturePath = {textures_path}",
        f"reshadeIncludePath = {shaders_path}"
        f"\n\n{effects_path_str}",
        f"\n{used_effects_str[:-1]}"
    ])

    # Write config file
    with open(path_join(output_dir, "vkBasalt.conf"), "w") as f:
        f.write(file_content)
    return output_dir


def update_file(shader: str, configs: dict, verbose=0):
    for param, value in configs.items():
        if verbose:
            logging.debug(f"Param: {param}\nValue: {value}")

        pattern = r"".join([
            "(^\[[:alnum:]]*\[[:blank:]]*)",  # "uniform" keyword or similar, group 1
            "(\[[:alnum:]]*)",  # variable type (bool, float, float2, etc), group 2
            "(\[[:blank:]]*{param}\[[:blank:]]*",  # name of the current parameter, group 3 until value assignment
            "<.*?>",  # content block between brackets
            "\[[:blank:]]*=\[[:blank:]])(.*?);$"  # value assignment (e.g. " = 1.00;"), with value captured as group 4
        ])  # Brackets have to be escaped (e.g. \[[:alnum:]]) to prevent a FutureWarning,
        # pycharm warns about invalid sequence because their regex handler probably still follows old norms

        # This custom function is passed to re.sub. This could have been done through a re.search followed by re.sub,
        # but would have implied running the regex twice, which is unnecessary. Instead we hijack the substitution
        # function to process and inject the new value.
        def transform_value(matchobj):
            """Process a config block to inject a new value inside without breaking everything"""
            value_type = matchobj.group(2)
            if value_type == "bool":
                new_value = "true" if int(value) == 1 else "false"
            elif re.search(r"float.+", value_type):  # floatX value type
                new_value = f"{value_type}({value})"  # value is a str containing multiple values (and not a tuple)
            else:
                new_value = value
            # FIXME: This return object is really ugly, there has to be a better way
            return "".join([matchobj.group(1), matchobj.group(2), matchobj.group(3), new_value, ";"])

        shader = re.sub(pattern, transform_value, shader)
    return shader


if __name__ == "__main__":
    run()
