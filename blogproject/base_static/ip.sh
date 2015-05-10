#!/bin/bash
 
# download from apnic
rm -f delegated-apnic-latest
wget http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest
 
# IPs allocated to china.
grep 'apnic|CN|ipv4|' delegated-apnic-latest | cut -f 4 -d'|' > delegated-apnic-CN
 
# get detail of echo IP from apnic database.
rm -f apnic_CN.txt
while read ip
do
    # query apnic database
    echo "query who is $ip"
    whois -h whois.apnic.net $ip > tmp.txt
    grep inetnum  tmp.txt >> apnic_CN.txt          # IP range
    grep netname  tmp.txt >> apnic_CN.txt          # netname which include sp information  
    grep descr    tmp.txt >> apnic_CN.txt          # description which include province information
    echo ""  >> apnic_CN.txt           
done < delegated-apnic-CN
 
# clean up
rm -f tmp.txt
rm -f delegated-apnic-latest
rm -f delegated-apnic-CN
