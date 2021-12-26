# PMX to BMD

Very early WIP conversion for mmd PMX files to MTM BMD models

# PMXtoJSON.py

Currently supports converting vertices, faces, materials, and bones.

Breaks if any submesh/material uses more than 8 bones, and sometimes even with less than 8 bones.

# Usage

`py PMXtoJSON.py file.pmx`

Outputs file.json

# JSONtoBMD.py

Supports all parts of a BMD Model file except for IK Link info. 

That is to say that, besides TEST.BMD, converting the JSON output from the BMD to PMX converter back into a BMD file will create a file that should be the same size as the original, and functions identically to the original in-game, but isn't byte-for-byte identical due to the hashes inside the model file.

# Usage

`JSONtoBMD.py file.json`
