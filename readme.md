docker exec -it <mycontainer> bash

docker exec -it flask-flask-1 python train_model.py

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"flower":"1,23,4,4"}' \
  http://localhost:5000/iris_post

curl --header "Content-Type: application/json" --request POST --data '{"flower":"1,23,4,4"}'  http://localhost:5000/iris_post

curl -H "Content-Type: application/json" -X POST http://localhost:5000/iris_post -d "{"flower":"1,23,4,4"}"

curl -X POST http://localhost:5000/iris_post -H "Content-type:application/json" -d "{\"name\":\"Spring Forever\",\"author\":\"pivotal\"}"