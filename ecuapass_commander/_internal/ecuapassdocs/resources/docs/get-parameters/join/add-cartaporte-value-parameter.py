#!/usr/bin/env python
import json

inputFile = "input_parameters_manifiesto.json"
outputFile = "input_parameters_manifiesto-VALUE.json"

inputs = json.load (open (inputFile))

for key in inputs:
	inputs [key]["value"] = ""

json.dump (inputs, open (outputFile, "w"), indent=4, sort_keys=True)
