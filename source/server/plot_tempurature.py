    f8 = open('tmpPltFile', 'w')
    f8.write( "reset;\n" )
    f8.write( "set terminal unknown;\n" )
    f8.write( "plot 'tmpDataFile' using 1:2;\n" ) 
    f8.write( "set terminal gif font 'Arial' 12;\n" )
    f8.write( "set output '"+filename+"_"+ClientState+"_temperature.png';\n" )
    f8.write( "set term png size 1000, 600;\n" )
    f8.write( "set multiplot layout 3, 1 title '"+ClientState+"' font 'Arial-Bold, 19';\n" )
    f8.write( "set key top horizontal left;\n" )
    f8.write( "set xlabel 'Time (Seconds)';\n" )
    f8.write( "set tmargin 0.5;\n" )
    f8.write( "set style line 1 lt 1 pt 1 ps 1 lc rgb 'red' lw 1\n" )
    f8.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'blue' lw 1\n" )
    f8.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'forest-green' lw 1\n" )
    f8.write( "set style line 4 lt 1 pt 4 ps 1 lc rgb 'orange' lw 1\n" )
    f8.write( "set style line 5 lt 1 pt 4 ps 1 lc rgb 'violet' lw 1\n" )
    f8.write( "set ylabel 'Throghtput (Mbps)';\n" )
    f8.write( "set ytics nomirror;\n" )
    f8.write( "set ytics textcolor rgb 'red';\n" )
    # f8.write( "unset key;\n" )
    f8.write( "plot 'tmpDataFile' using 1:10 ls 1 title 'Throughput (mean:"+str(tput_mean)+")' with linespoints,\\\n " )
    f8.write( "    'tmpDataFile_for_tempurature' using 1:9 rgb 'red' title 'modem-lte-sub6-pa1' with linespoints,\\\n " )
    f8.write( "    'tmpDataFile_for_tempurature' using 1:10 rgb 'orange' title 'modem-0-usr' with linespoints,\\\n " )
    f8.write( "    'tmpDataFile_for_tempurature' using 1:3 rgb 'violet' title 'modem-mmw0-usr' with linespoints,\\\n " )
    f8.write( "    'tmpDataFile_for_tempurature' using 1:4 rgb 'forest-green' title 'modem-mmw1-usr' with linespoints,\\\n " )
    f8.write( "    'tmpDataFile_for_tempurature' using 1:5 rgb 'gray' title 'modem-mmw2-usr' with linespoints,\n " )

    f8.write( "set ylabel 'Temp (C)';\n" )
    f8.write( "set ytics textcolor rgb 'forest-green';\n" )
    f8.write( "set y2label '';\n" )
    f8.write( "set ytics textcolor rgb 'black';\n" )
    # f8.write( "unset key;\n" )
    f8.write( "plot 'tmpDataFile_for_tempurature' using 1:2 ls 1 title 'Battery' with linespoints,\\\n " )
    f8.write( "    'tmpDataFile_for_tempurature' using 1:7 rgb 'red' title 'cpu-0-0-step' with linespoints,\\\n " )
    f8.write( "    'tmpDataFile_for_tempurature' using 1:8 rgb 'red' title 'cpu-0-1-step' with linespoints,\n " )

    cmd = "gnuplot tmpPltFile\n cp tmpDataFile probedata"
    f.close()
    f8.close()
    cmd_run(cmd)
#  time :1 
                # battery_t = tmpTemperature_info[77] 2
            # modem-mmw0-usr = tmpTemperature_info[39] 3
            # modem-mmw1-usr = tmpTemperature_info[40] 4
            # modem-mmw2-usr = tmpTemperature_info[41] 5
            # modem-mmw3-usr = tmpTemperature_info[42] 6
            # cpu-0-0-step = tmpTemperature_info[23] 7
            # cpu-0-1-step = tmpTemperature_info[25] 8
            # modem-lte-sub6-pa1 = tmpTemperature_info[37] 9
            # modem-lte-sub6-pa2 = tmpTemperature_info[38] 10
            # modem-0-usr = tmpTemperature_info[47] 11
            # modem-1-usr = tmpTemperature_info[48]12 