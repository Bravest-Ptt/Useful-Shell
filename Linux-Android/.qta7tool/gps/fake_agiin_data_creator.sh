#!/bin/bash

while [ "1" = "1" ]
do
    echo "\$GPRMC,092000.000,A,3221.7233,N,11924.6708,E,0.0,0.0,290817,,,A*61
    \$GPGGA,092000.000,3221.7233,N,11924.6708,E,1,09,1.0,23.0,M,6.1,M,,*58
    \$GPGLL,3221.7233,N,11924.6708,E,092000.000,A,A*53
    \$GPVTG,0.0,T,,M,0.0,N,0.0,K,A*0D
    \$GPGNS,092001.000,3221.7233,N,11924.6708,E,ANNN,09,1.0,23.0,6.1,,*7C
    \$GPGSV,3,1,09,02,60,114,31,05,61,007,31,06,15,124,44,07,09,047,46*7D
    \$GPGSV,3,2,09,13,69,183,41,15,36,219,26,20,40,293,43,29,43,286,19*7D
    \$GPGSV,3,3,09,30,21,078,25*48
    \$GPGGA,092001.000,3221.7233,N,11924.6708,E,1,09,1.0,23.0,M,6.1,M,,*59
    \$GPGLL,3221.7233,N,11924.6708,E,092001.000,A,A*52
    \$GPVTG,0.0,T,,M,0.0,N,0.0,K,A*0D
    \$GPGSA,A,3,02,05,06,07,13,15,20,29,30,,,,1.8,1.0,1.4*35
    \$GPRMC,092002.000,A,3221.7233,N,11924.6708,E,0.0,0.0,290817,,,A*63
    \$GPGGA,092002.000,3221.7233,N,11924.6708,E,1,09,1.0,23.0,M,6.1,M,,*5A
    \$GPGLL,3221.7233,N,11924.6708,E,092002.000,A,A*51" >> "$1"
    sleep 1
done

