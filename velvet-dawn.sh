#!/bin/bash


export PYTHONPATH=src/server/src:$PYTHONPATH


# Setup optional flags -c -d -p
clean="false"
datapack=""
port=""
while getopts 'cd:p:' flag; do
  case "${flag}" in
    c) clean="true" ;;
    d) data_pack="${OPTARG}" ;;
    p) port="${OPTARG}" ;;
    *) error "Unexpected option ${flag}" ;;
  esac
done
shift $(($OPTIND-1))
echo $1


# If the '-c' flag is used:
if [ ${clean} = "true" ]
then
  # Drop all tables from the game database
  python src/server/src/velvet_dawn/dao/clean.py
fi

if [ $1 = "start" ]
then
  # Start the server in prod mode
  python src/server/src/velvet_dawn/server/app.py

elif [ $1 = "dev-fe" ]
then
  # Run the FE server for developing the front end
  cd src/frontend
  npx webpack serve

elif [ $1 = "build" ]
then
  # Build the front end so the server runs it (maybe automate in github)
  cd src/frontend
  npm run magic

elif [ $1 = "test" ]
then
  # Test all
  mvn test --file pom.xml
  cd src/frontend
  npm run test

elif [ $1 = "test-server" ]
then
  # Test server
  mvn test --file pom.xml

elif [ $1 = "test-frontend" ]
then
  # Test frontend
  cd src/frontend
  npm run test

else
  echo "Missing argument: start, dev, dev-fe, build, test, test-server, test-frontend"
fi
