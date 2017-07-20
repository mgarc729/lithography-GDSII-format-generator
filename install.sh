#!/bin/bash

mkdir /usr/local/gds_lithograpy_generator
cp gui.py /usr/local/gds_lithography_generator
cp grid.py /usr/local/gds_lithography_generator
cp wafer.py /usr/local/gds_lithography_generator
cp pillar.py /usr/local/gds_lithography_generator
cp tools.py /usr/local/gds_lithography_generator

echo "python gui.py" >> run.sh
ln -s /usr/local/gds_lithograpy_generator/run.sh /usr/bin/gds_lithography


