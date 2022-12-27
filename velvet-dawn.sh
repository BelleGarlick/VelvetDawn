echo $1

if [ $1 == "start" ]
then
  export PYTHONPATH=server:$PYTHONPATH
  python server/velvet_dawn/server/app.py

elif [ $1 == "test" ]
then
  pytest
fi
