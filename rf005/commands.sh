# cluster
baggage-cluster

#cloud SQL 
# crear la base de datos tipo development, ip privada / seleccionar red y rango de red

# authetication
gcloud init

# Docker daemon socket permission
sudo chmod 666 /var/run/docker.sock 

# imagenes
sudo docker build -t us-central1-docker.pkg.dev/proyectogrupo3/repository-baggage/users:1.0 ./users/.
docker push us-central1-docker.pkg.dev/proyectogrupo3/repository-baggage/users:1.0

sudo docker build -t us-central1-docker.pkg.dev/proyectogrupo3/repository-baggage/offers:1.0 ./offers/.
docker push us-central1-docker.pkg.dev/proyectogrupo3/repository-baggage/offers:1.0

sudo docker build -t us-central1-docker.pkg.dev/proyectogrupo3/repository-baggage/routes:1.0 ./routes/.
docker push us-central1-docker.pkg.dev/proyectogrupo3/repository-baggage/routes:1.0

sudo docker build -t us-central1-docker.pkg.dev/proyectogrupo3/repository-baggage/posts:1.0 ./posts/.
docker push us-central1-docker.pkg.dev/proyectogrupo3/repository-baggage/posts:1.0

sudo docker build -t us-central1-docker.pkg.dev/proyectogrupo3/repository-baggage/scores:1.0 ./score/.
docker push us-central1-docker.pkg.dev/proyectogrupo3/repository-baggage/scores:1.0

sudo docker build -t us-central1-docker.pkg.dev/proyectogrupo3/repository-baggage/rf003:1.0 ./rf003/.
docker push us-central1-docker.pkg.dev/proyectogrupo3/repository-baggage/rf003:1.0

sudo docker build -t us-central1-docker.pkg.dev/proyectogrupo3/repository-baggage/rf004:1.0 ./rf004/.
docker push us-central1-docker.pkg.dev/proyectogrupo3/repository-baggage/rf004:1.0

sudo docker build -t us-central1-docker.pkg.dev/proyectogrupo3/repository-baggage/rf005:1.0 ./rf005/.
docker push us-central1-docker.pkg.dev/proyectogrupo3/repository-baggage/rf005:1.0

# network
gcloud compute networks create vpn-baggage --project=myproject-8ceb8 --subnet-mode=custom --mtu=1460 --bgp-routing-mode=regional

gcloud compute networks subnets create red-k8s-baggage --range=192.168.32.0/19 --network=vpn-baggage --region=us-central1 --project=myproject-8ceb8

gcloud compute addresses create red-dbs-baggage --global --purpose=VPC_PEERING --addresses=192.168.0.0 --prefix-length=24 --network=vpn-baggage --project=myproject-8ceb8

gcloud services vpc-peerings connect --service=servicenetworking.googleapis.com --ranges=red-dbs-baggage --network=vpn-baggage --project=myproject-8ceb8

gcloud compute firewall-rules create allow-db-ingress --direction=INGRESS --priority=1000 --network=vpn-baggage --action=ALLOW --rules=tcp:5432 --source-ranges=192.168.1.0/24 --target-tags=basesdedatos --project=myproject-8ceb8

# K8s Cluster
gcloud container clusters get-credentials baggage-cluster --region us-central1 --project myproject-8ceb8

# Deploment
kubectl delete all --all -n default

kubectl apply -f k8s-base-layer-deployment.yaml 
kubectl apply -f k8s-new-services-deployment.yaml 
kubectl apply -f k8s-ingress-deloyment.yaml 


# Pub/Sub 

gcloud pubsub topics create card-verification --message-retention-duration=1h

gcloud pubsub topics create send-email --message-retention-duration=1h

gcloud functions deploy funcion-test-endpoint --entry-point enviar_mensaje --runtime python39 --trigger-http --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1 --set-env-vars TOPIC=card-verification,PROJECT_ID=myproject-8ceb8

gcloud functions deploy funcion-pubsub-card-verifier --entry-point verifier --runtime python39 --trigger-topic card-verification --retry --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1 --set-env-vars INGRESS_PATH=34.120.71.197,SECRET_TOKEN=qwerty

gcloud functions deploy funcion-pubsub-send-email --entry-point send --runtime python39 --trigger-topic send-email --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1 --set-env-vars INGRESS_PATH=34.120.71.197,SECRET_TOKEN=qwerty

