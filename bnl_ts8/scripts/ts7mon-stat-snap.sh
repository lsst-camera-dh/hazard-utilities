cd /home/ts8prod/utilities/BNL2/
python ./ccsingest.py ts7-enviro-mon2.py | grep ^time | tee -a ts7mon.log
