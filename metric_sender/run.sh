#!/bin/bash
usage() {
  echo "Usage: $0 [ -c config-file-path ]" 1>&2
  exit 0
  }
CONFIG_FILE="config.txt"
while getopts ":h:c:" options; do
  case "${options}" in
    c)
      CONFIG_FILE=${OPTARG}
      echo ${CONFIG_FILE}
      ;;
    h)
      usage
      ;;
    *)
      usage
      ;;
  esac
done

docker build -t metric_sender .

while IFS= read -r line; do
  line=$(echo $line)
  # shellcheck disable=SC1073
  if  [[ "${line}" =~ [^a-zA-Z] ]]; then
    echo "${line}"
    tokens=( $line )
    # <metric-name> <metric-type[cpu|disk|memory]> <metric-count> <telegraph-host:port> <total-iteration-count> <sleep-between-iteration-in-seconds>
    NAME="${tokens[0]}"
    TYPE="${tokens[1]}"
    METRICS_COUNT="${tokens[2]}"
    HOST="${tokens[3]}"
    ITER_COUNT="${tokens[4]}"
    SLEEP_DURATION="${tokens[5]}"

    docker run -d --rm -it --net=host metric_sender -n "${NAME}" -t "${TYPE}" -c ${METRICS_COUNT} -s ${SLEEP_DURATION} \
          -i ${ITER_COUNT} -a "${HOST}"
  fi
done < "${CONFIG_FILE}"
docker container ls --no-trunc  | grep metric_sender


#docker run  --name=telegraf  -v $(pwd)/telegraf.conf:/etc/telegraf/telegraf.conf:ro  --add-host=host.docker.internal:host-gateway -p 8092:8092/udp telegraf --config /etc/telegraf/telegraf.conf
