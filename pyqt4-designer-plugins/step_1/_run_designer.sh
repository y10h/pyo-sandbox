#!/bin/sh

PWD=`pwd`
export PYQTDESIGNERPATH="$PWD/plugins"
designer-qt4 $@

