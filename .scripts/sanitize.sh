#!/bin/bash

BUILD="build"
DISTRIBUTION="dist"
BUILD_INFO="agrow.egg-info"
LIBRARIES="*.so"
SRC="agrow"

rm -rf $DISTRIBUTION $BUILD $BUILD_INFO
find $SRC -name $LIBRARIES -exec rm -f {} \;
