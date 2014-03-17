#!/bin/bash
python ../Scripts/chicago_hrr.py

clean_build=1

# Build FDS Verification Guide
pdflatex -interaction nonstopmode Chicago_Fire &> Chicago_Fire.err
bibtex Chicago_Fire &> Chicago_Fire.err
pdflatex -interaction nonstopmode Chicago_Fire &> Chicago_Fire.err
pdflatex -interaction nonstopmode Chicago_Fire &> Chicago_Fire.err

# Scan and report any errors in the LaTeX build process
if [[ `grep -E "Error:|Fatal error|! LaTeX Error:|Paragraph ended before|Missing \\\$ inserted|Misplaced" -I Chicago_Fire.err | grep -v "xpdf supports version 1.5"` == "" ]]
   then
      # Continue along
      :
   else
      echo "LaTeX errors detected:"
      grep -E "Error:|Fatal error|! LaTeX Error:|Paragraph ended before|Missing \\\$ inserted|Misplaced" -I Chicago_Fire.err | grep -v "xpdf supports version 1.5"
      clean_build=0
fi

# Check for LaTeX warnings (undefined references or duplicate labels)
if [[ `grep -E "undefined|multiply defined|multiply-defined" -I Chicago_Fire.err` == "" ]]
   then
      # Continue along
      :
   else
      echo "LaTeX warnings detected:"
      grep -E "undefined|multiply defined|multiply-defined" -I Chicago_Fire.err
      clean_build=0
fi

if [[ $clean_build == 0 ]]
   then
      :
   else
      echo "Chicago_Fire built successfully!"
fi    
