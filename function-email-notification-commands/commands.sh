# Creación del tema en Pub/Sub
gcloud pubsub topics create send-email --message-retention-duration=1h

# Creación de la función test para publicar
gcloud functions deploy funcion-pub-send-email-test --entry-point peticion_enviar_email --runtime python39 --trigger-http --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1

# Creación de la función para envío de emails 
gcloud functions deploy function-pubsub-send-emails --entry-point sub_send_email --runtime python39 --trigger-topic send-email --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1 --env-vars-file=env_vars.yaml