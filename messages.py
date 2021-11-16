# -*- coding: utf-8 -*-

version = "v1.0.0"

help_str = """
Reshade2Basalt.

{}
Author: Emmy Gomes
Email: aou-emmy@outlook.com
Issues: https://github.com/eemmy/Reshade2Basalt/issues

To donate, please contact +55 11 95837-8163 on Whatsapp, or send-me a email.


Syntax: python3 run.py [--argument=value]

Types:
bool    True/False (uppercase).
int     0,1,2...
float   0.4,0.5,0.6...
path    Absolute path to files or folders
str     Phrase or word wrapped in quotes (ex: \"Shaders, Textures, etc...\") 


Options:

--help=bool                    Show this menu instead running script.
--verbose=bool                 Add a high debug output. Recommended to report issues.
[--shaders-repo, --fxr]=str    Git clone string to shaders repository (default is Reshade Shaders in packages section).
[--shaders-branch, --fxb]=str  Shaders repository branch (default is master).
[--preset, --p]=path           Path to reshade .ini file. If not specified, the script will assume that the file is in the current directory, as preset.ini
[--ignore-shaders, --fxi]=str  Inform which preset using shaders you want to ignore. This is util with complex shaders that vkBasalt can't handle correctly. Pass without spaces, divided by a comma.
--use-cached-shaders=bool      Inform to script does not re-download shaders from remote git repository if it already exists.
--include-shaders-dir=path     Inform a path to folder with custom shaders that you want to include in script job. This shaders will replace remote shaders. 
--output-dir=path              Path to save shaders after setting them up. Default is current directory (note that if you want to change shaders folder path, you must to change it on generate vkBasalt.conf too)


Packages:

List of packages that work with this script, that the conversion result might be useful, or that inspired or were used to build this script.

Reshade by Crosire: https://reshade.me, https://github.com/crosire/reshade
reshade-shaders by Crosire: https://github.com/crosire/reshade-shaders
vkBasalt by DadSchoorse: https://github.com/DadSchoorse/vkBasalt

""".format(version)
