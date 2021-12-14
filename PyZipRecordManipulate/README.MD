# Zip Record Manipulator

Helper scripts to dump data from MTM's DATA.ZIP, and rebuild it in the same order as the original file.

Please note that you will need to modify the PK Headers for each file/dir entry you modified, every file has to remain present, and you cannot add files.

Note: As of the current version, a DATA.IDX must be present for PyZipRecordCombine so that the script can attempt to update every file offset to prevent crashes in the event of larger files.
