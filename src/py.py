from IOB_tagger import IOB_tagger as itgr
import sys
jomle = ''
for arg in sys.argv[1:]:
    jomle += arg + ' '
itgr(jomle)