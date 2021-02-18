#!/bin/sh

#./hw4_topcfg.sh $1 $2

#./hw4_parser.sh $2 $3 $4

#/dropbox/20-21/571W/hw4/tools/evalb -p /dropbox/20-21/571W/hw4/tools/COLLINS.prm /opt/dropbox/20-21/571W/hw4/data/parses.gold $4 > $6

#./hw4_improved_parser.sh $2 $3 $5

#/dropbox/20-21/571W/hw4/tools/evalb -p /dropbox/20-21/571W/hw4/tools/COLLINS.prm /opt/dropbox/20-21/571W/hw4/data/parses.gold $5 > $7

./hw4_topcfg.sh /opt/dropbox/20-21/571W/hw4/data/parses.train hw4_trained.pcfg

./hw4_parser.sh hw4_trained.pcfg /opt/dropbox/20-21/571W/hw4/data/sentences.txt parses_base.out

/dropbox/20-21/571W/hw4/tools/evalb -p /dropbox/20-21/571W/hw4/tools/COLLINS.prm /opt/dropbox/20-21/571W/hw4/data/parses.gold parses_base.out > parses_base.eval

./hw4_improved_parser.sh hw4_trained.pcfg /opt/dropbox/20-21/571W/hw4/data/sentences.txt parses_improved.out

/dropbox/20-21/571W/hw4/tools/evalb -p /dropbox/20-21/571W/hw4/tools/COLLINS.prm /opt/dropbox/20-21/571W/hw4/data/parses.gold parses_improved.out > parses_improved.eval
