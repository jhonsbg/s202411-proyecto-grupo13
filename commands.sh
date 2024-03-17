# cluster
baggage-cluster

#cloud SQL 
# crear la base de datos tipo development, ip privada / seleccionar red y rango de red

# authetication
gcloud init

# Docker daemon socket permission
sudo chmod 666 /var/run/docker.sock 

# imagenes
sudo docker build -t us-central1-docker.pkg.dev/proyectogrupo3/repository-baggage/cards:3.0 ./cards/.
docker push us-central1-docker.pkg.dev/proyectogrupo3/repository-baggage/cards:3.0

sudo docker build -t us-central1-docker.pkg.dev/proyectogrupo3/repository-baggage/users:2.0 ./users/.
docker push us-central1-docker.pkg.dev/proyectogrupo3/repository-baggage/users:2.0

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
gcloud compute networks create vpn-baggage --project=proyectogrupo3 --subnet-mode=custom --mtu=1460 --bgp-routing-mode=regional

gcloud compute networks subnets create red-k8s-baggage --range=192.168.32.0/19 --network=vpn-baggage --region=us-central1 --project=proyectogrupo3

gcloud compute addresses create red-dbs-baggage --global --purpose=VPC_PEERING --addresses=192.168.0.0 --prefix-length=24 --network=vpn-baggage --project=proyectogrupo3

gcloud services vpc-peerings connect --service=servicenetworking.googleapis.com --ranges=red-dbs-baggage --network=vpn-baggage --project=proyectogrupo3

gcloud compute firewall-rules create allow-db-ingress --direction=INGRESS --priority=1000 --network=vpn-baggage --action=ALLOW --rules=tcp:5432 --source-ranges=192.168.1.0/24 --target-tags=basesdedatos --project=proyectogrupo3

# K8s Cluster
gcloud container clusters get-credentials baggage-cluster --region us-central1 --project proyectogrupo3

# Deploment
kubectl delete all --all -n default

kubectl apply -f k8s-base-layer-deployment.yaml 
kubectl apply -f k8s-new-services-deployment.yaml 
kubectl apply -f k8s-ingress-deloyment.yaml 


# Pub/Sub 

gcloud pubsub topics create card-verification --message-retention-duration=1h

gcloud pubsub topics create send-email --message-retention-duration=1h

gcloud functions deploy funcion-test-endpoint --entry-point enviar_mensaje --runtime python39 --trigger-http --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1 --set-env-vars TOPIC=card-verification,PROJECT_ID=proyectogrupo3

gcloud functions deploy funcion-pubsub-card-verifier --entry-point verifier --runtime python39 --trigger-topic card-verification --retry --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1 --set-env-vars INGRESS_PATH=34.128.166.237,SECRET_TOKEN=qwerty

gcloud functions deploy funcion-pubsub-send-email --entry-point send --runtime python39 --trigger-topic send-email --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1 --set-env-vars INGRESS_PATH=34.128.166.237,SECRET_TOKEN=qwerty


# IP red local: 
ip addr show | grep 'inet '

# Pub Sub local: 

gcloud projects add-iam-policy-binding proyectogrupo3 --member="user:hmaury1@gmail.com" --role=roles/pubsub.admin


# Pub Sub + k8

kubectl create namespace namespace-baggage-cluster

kubectl create serviceaccount service-account-baggage -n default

gcloud iam service-accounts create service-account-baggage --project=proyectogrupo3

gcloud projects add-iam-policy-binding proyectogrupo3  --member=serviceAccount:service-account-baggage@proyectogrupo3.iam.gserviceaccount.com  --role=roles/pubsub.editor  
gcloud projects add-iam-policy-binding proyectogrupo3  --member=serviceAccount:service-account-baggage@proyectogrupo3.iam.gserviceaccount.com  --role=roles/iam.workloadIdentityUser   
gcloud projects add-iam-policy-binding proyectogrupo3  --member=serviceAccount:service-account-baggage@proyectogrupo3.iam.gserviceaccount.com  --role=roles/pubsub.admin   
