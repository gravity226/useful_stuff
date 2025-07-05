### build docker image
docker build -t dnn-clustering .

### run docker image
docker run -it --rm -p 8888:8888 -v "$(pwd)":/workspace dnn-clustering

### TODO
- https://stats.stackexchange.com/questions/140148/how-can-an-artificial-neural-network-ann-be-used-for-unsupervised-clustering


