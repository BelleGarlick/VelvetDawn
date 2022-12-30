echo $1

if [ $1 = "start" ]
then
  # Start the server in prod mode
  export PYTHONPATH=src/server/src:$PYTHONPATH
  python src/server/src/velvet_dawn/server/app.py

elif [ $1 = "dev" ]
then
  # Start the server in dev mode
  export PYTHONPATH=src/server/src:$PYTHONPATH
  export DEV=true
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
  export PYTHONPATH=src/server/src:$PYTHONPATH
  python -m pytest
  cd src/frontend
  npm run test

elif [ $1 = "test-server" ]
then
  # Test all
  export PYTHONPATH=src/server/src:$PYTHONPATH
  python -m pytest

elif [ $1 = "test-frontend" ]
then
  cd src/frontend
  npm run test

else
  echo "Missing argument: start, dev, dev-fe, build, test, test-server, test-frontend"
fi