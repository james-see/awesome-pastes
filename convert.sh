#!/bin/bash
pip3 install markdown_to_json
md_to_json README.md -o pastebins.json
echo "Converted successfully to pastebins.json!"