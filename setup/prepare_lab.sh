#!/usr/bin/env bash

TIMEOUT_CMD=`which timeout`
if [ $? -eq 0 ]; then
  TIMEOUT_CMD="${TIMEOUT_CMD} 5 "
else
  TIMEOUT_CMD=""
fi

# Obtain the true location of this script
SCRIPT_TRUEPATH="$( readlink -f $0 )"

# Extract the path of this script from the true path
SCRIPT_BASEPATH="$( dirname ${SCRIPT_TRUEPATH} )"

# Location of the participant code
CODE_PATH="${SCRIPT_BASEPATH}/../code/tasks"

# Where lab files should be copied
TARGET_DIRECTORY=~/event-lab

test_netbox()
{
  NETBOX_UI_TARGET=200

  printf "%40s" "NetBox UI status: "
  NETBOX_UI_RESULT=$(${TIMEOUT_CMD}curl -s -o /dev/null -w "%{http_code}" "${NETBOX_URL}")
  if [ "x${NETBOX_UI_RESULT}" = "x${NETBOX_UI_TARGET}" ]; then
    echo "OK"
  else
    ERROR_COUNT=${ERROR_COUNT+1}
    ERROR_MESSAGES="${ERROR_MESSAGES}\t- The NetBox UI is not accessible.\n"
    echo "FAIL"
  fi

  printf "%40s" "NetBox API status: "
  NETBOX_API_RESULT=$(${TIMEOUT_CMD}curl -fsv \
    "${NETBOX_URL}/api/status/" 2>&1)

  if [ $? -ne 0 ] ; then
    ERROR_COUNT=${ERROR_COUNT+1}
    ERROR_MESSAGES="${ERROR_MESSAGES}\t- The NetBox API is not accessible.\n"
    echo "FAIL"
  else
    echo "OK"
  fi
}

test_tickets()
{
  TICKET_UI_TARGET=200

  TICKET_UI_URL=`echo ${TICKET_URL} | sed -e 's/api\/v1\///'`
  printf "%40s" "Ticket system UI status: "
  TICKET_UI_RESULT=$(${TIMEOUT_CMD}curl -s -o /dev/null -w "%{http_code}" "${TICKET_UI_URL}")
  if [ "x${TICKET_UI_RESULT}" = "x${TICKET_UI_TARGET}" ]; then
    echo "OK"
  else
    ERROR_COUNT=${ERROR_COUNT+1}
    ERROR_MESSAGES="${ERROR_MESSAGES}\t- The ticket system UI is not accessible.\n"
    echo "FAIL"
  fi

  printf "%40s" "Ticket system API status: "
  TICKET_API_RESULT=$(${TIMEOUT_CMD}curl -s -o /dev/null -w "%{http_code}" \
      -u "${TICKET_USERNAME}:${TICKET_PASSWORD}" "${TICKET_URL}")

  if [ $? -ne 0 ] ; then
    ERROR_COUNT=${ERROR_COUNT+1}
    ERROR_MESSAGES="${ERROR_MESSAGES}\t- The ticket system API is not accessible.\n"
    echo "FAIL"
  else
    echo "OK"
  fi
}

# Execute the setup tasks....
echo
echo "******************************************************************************"
echo "Beginning lab preparation tasks..."
echo "******************************************************************************"
echo

echo
echo "******************************************************************************"
echo "Copying lab activity files..."
echo "******************************************************************************"
echo

mkdir -p ${TARGET_DIRECTORY}
rsync -ar ${CODE_PATH}/ ${TARGET_DIRECTORY}/

echo
echo "******************************************************************************"
echo "Testing pod services..."
echo "******************************************************************************"
echo

echo ""
echo "TEST 1: Checking connectivity to NetBox in Pod ${PODID}:"
test_netbox

echo ""
echo "TEST 2: Checking connectivity to ticket system in Pod ${PODID}:"
test_tickets


echo
echo "******************************************************************************"
echo "Lab preparation tasks complete!"
echo "******************************************************************************"
echo
