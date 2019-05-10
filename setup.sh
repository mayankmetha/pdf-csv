#!/bin/bash

if [[ "$OSTYPE" == "darwin"* ]]
then
    # macOS specific code
    brew install poppler tesseract
elif [[ "$OSTYPE" == "linux-gnu" || "$OSTYPE" == "linux" ]]
then
    # linux specific code - ubuntu
    sudo apt install tesseract-ocr libtesseract-dev poppler-utils
fi

if type conda > /dev/null 2>&1
then
    # install pip via conda
    conda install pip
    # pip install dependencies
elif type pip3 > /dev/null 2>&1
then
    #pip3 specific package installation
    pip3 install PyPDF2 pillow pdf2image pyocr pikepdf
fi