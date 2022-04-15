url="<apache-server-http-url like http://54.183.167.231>"
ports=(8081 8082 8083 8084 8085 8086 8087 8088)
concurrent_sessions=50
duration="6h"

for index in "${!ports[@]}";
do

rm -rf "${ports[$index]}.txt" && nohup ./hey -z ${duration} -c ${concurrent_sessions} "${url}:${ports[$index]}" 2>&1 > "${ports[$index]}.txt" < /dev/null &
done
