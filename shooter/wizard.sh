#!/bin/sh

SHOOTER="python shooter.py"

one=`$SHOOTER A2 PUT cid c_OOOOOOOOOOOOOOOOOOOO print-context_gus`
if [ $? != 0 ]; then echo "\tError context creation " && exit; fi

two=`$SHOOTER A2 PUT cid c_OOOOOOOOOOOOOOOOOOOO print-context_gus`
if [ $? != 0 ]; then echo "\tError context creation " && exit; fi

three=`$SHOOTER A2 PUT cid c_OOOOOOOOOOOOOOOOOOOO print-context_gus`
if [ $? != 0 ]; then echo "\tError context creation " && exit; fi

four=`$SHOOTER A2 PUT cid c_OOOOOOOOOOOOOOOOOOOO print-context_gus`
if [ $? != 0 ]; then echo "\tError context creation " && exit; fi

rcvr1=`$SHOOTER A3 PUT rid r_AAAAAAAAAAAAAAAAAAAA print-receiver_gus raw \"$one\",\"$two\"`
if [ $? != 0 ]; then echo "\tError receiver1 creation " && exit; fi

rcvr2=`$SHOOTER A3 PUT rid r_AAAAAAAAAAAAAAAAAAAA print-receiver_gus raw \"$one\",\"$two\" variation 1`
if [ $? != 0 ]; then echo "\tError receiver2 creation " && exit; fi

rcvr3=`$SHOOTER A3 PUT rid r_AAAAAAAAAAAAAAAAAAAA print-receiver_gus raw \"$one\",\"$two\" variation 2`
if [ $? != 0 ]; then echo "\tError receiver3 creation " && exit; fi

rcvr4=`$SHOOTER A3 PUT rid r_AAAAAAAAAAAAAAAAAAAA print-receiver_gus raw \"$one\",\"$two\" variation 3`
if [ $? != 0 ]; then echo "\tError receiver4 creation " && exit; fi

rcvr5=`$SHOOTER A3 PUT rid r_AAAAAAAAAAAAAAAAAAAA print-receiver_gus raw \"$one\",\"$two\" variation 4`
if [ $? != 0 ]; then echo "\tError receiver5 creation " && exit; fi

echo "created four contexts: $one $two $three $four"
echo "created five receiver in context 1 and 2: $rcvr1 $rcvr2 $rcvr3 $rcvr4 $rcvr5"
