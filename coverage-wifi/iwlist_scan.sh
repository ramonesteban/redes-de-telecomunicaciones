touch scan.dat
rm scan.dat
touch scan.dat

response=`sudo iwlist eth1 scan | grep -e Quality -e ESSID`
echo $response
echo $response >> scan.dat
