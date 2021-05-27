#!/bin/bash
# COPA
git clone https://bitbucket.org/sandesh_dhawaskar/modified_copa.git

# SPROUT
git clone https://github.com/keithw/sprout.git


mv ~/modified_copa/genericCC ~/genericCC
cd ~/genericCC
cp ~/5G_measurement_tool/source/other/copa/sender.cc ~/genericCC
cp ~/5G_measurement_tool/source/other/copa/client.cc ~/genericCC
cp ~/5G_measurement_tool/source/other/copa/markoviancc.cc ~/genericCC
cp ~/5G_measurement_tool/source/other/copa/udp-socket.cc ~/genericCC  # put your server IP address @line.22
makepp



# # install sprout
cd ~/sprout
cp ~/5G_measurement_tool/source/other/sprout/sproutconn.cc ~/sprout/src/network/
./autogen.sh && ./configure --enable-examples && make