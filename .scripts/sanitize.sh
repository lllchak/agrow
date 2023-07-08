#!/bin/bash

BUILD="build"
BUILD_INFO="agrow.egg-info"
LIBRARIES="*.so"
SRC="agrow"

rm -rf $BUILD $BUILD_INFO 
find $SRC -name $LIBRARIES -exec rm -f {} \;
