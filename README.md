# Reshade2Basalt
This python3 scripts will convert Reshade .ini presets to vkBasalt .conf files, changing shader settings directly in .fx files.

# Dependencies
- Python >= 3.4
- vkBasalt

# Usage
After downloading it, you are ready to start using, with ```python3 run.py [--args] ```  command.

# Options

Because method of handle arguments, all arguments must to be passed with python types (True/False,  "str", etc). These are the types that script will use:



| Type | Description                                               | Example                |
|------|-----------------------------------------------------------|------------------------|
| bool | A True or False argument                                  | --arg=True             |
| str  | A phrase/word wrapped in quotes                           | --arg="Str1,Str2..." 
| path | A complete path to file or folder, looking at system root | --arg="/home/user/dir" |

Arguments syntax are the following ```--arg=value```, and can contain various arguments. Bellow, you will find the complete arguments list.

| Option                | Description                                               | Required | Default                                      | Type |
|-----------------------|-----------------------------------------------------------|----------|----------------------------------------------|------|
| --help                | Show help menu                                            | No       | False                                        | bool |
| --verbose             | Show some extra debug messages. Use when reporting issues | No       | False                                        | bool |
| --shaders-repo, --fxr | Set a different one reshade-shaders git repository        | No       | "https://github.com/crosire/reshade-shaders" | str  |
| --shaders-branch, --fxb | Shaders repository branch                                                                                                                                      | No       | master          | str  |
| --preset, --p           | Path to reshade .ini file.                                                                                                                                     | No       | $PWD/preset.ini | path |
| --ignore-shaders, --fxi | Shaders that are preset in preset, but that you want to ignore. Util when vkBasalt can't handle correctly the shader. Pass without spaces, divided by a comma. | No       | ""              | str  |
| --output-dir | Path to save shaders after setting them up. Default is current directory (note that if you want to change shaders folder path, you must to change it on generate vkBasalt.conf too) | No       | $PWD/output/ | path |

# Contributions
All contributions to source are welcome, just create a pull request in this repo and i will verify as soon possible.

If you can try different presets (for now, only part of reshade default shaders are noticable 100% working in vkBasalt) in looking for issues, you would already help me a lot. Please report any issue with default shaders in Issues section of this repo.

And if you're a Linux gamer entusiast and want to helpe-me and encourage to do more linux games utilities, buy me a coffe! You can enter in contact to me to receive a payment link to donate how much you want and can to give-me.

# Project status

This is a Beta 1.0.0 version, with obviously various bugs to map and fix, and improvements to do. Updates by author will only occur in weekends, so you can enter here each sunday night to check for status

Below, a list of updates that you can do, or wait for me:

* Test various presets to map bugs, and register then in issues.
* A better documentation
* A argument that allow user to include custom shaders in .temp dir
* A better argument handler
* Special treatment to shaders that contains a .fxh file included (e.g. SMAA/FXAA, that is current not supported)
* A install script to make it available globally
* A argument that allow user to automatically creates a .sh/.desktop for some game/application already with vkBasalt configuration variables in command.
* A argument that allow user to live test presets (with vkcube) before write shaders/settings in output_dir
* .sh to run script with arguments directly as a shell script

# Authors
* Emmy Gomes | <aou-emmy@outlook.com> | +55 (11) 9537-8163.
