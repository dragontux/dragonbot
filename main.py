#!/usr/bin/env python3
import irc
import input
import sys
import time

config = { }
config_file = "default.conf"

def read_config( conf_file ):
    try:
        fp = open( conf_file, "r" );
    except IOError as e:
        print( "Config file error:", e );
        exit(1)

    buf = fp.readline()
    while ( len( buf ) > 0 ):
        options = buf.split();
        if ( len( options ) > 1 ):
            config.update({ options[0]:options[1:] })
        buf = fp.readline()

if __name__ == "__main__":
    if len( sys.argv ) > 1:
        config_file = sys.argv[1]
    read_config(config_file);

    print( "[ bot ] Connecting to %s..." % ( config["server"][0] ))
    server = irc.irc_server(config)
    #server.identify( config["nick"][0] )

    in_thread = input.in_thread(server);
    in_thread.start();
    print( "[ bot ] Started input thread" )

    #server.join(config["channels"])
    print( "[ bot ] Connected to %s as %s." % ( config["server"][0], config["nick"][0] ))
