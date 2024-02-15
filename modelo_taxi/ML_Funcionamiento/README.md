gcloud builds submit --tag gcr.io/shaped-faculty-413418/modelosml  --project=shaped-faculty-413418

gcloud run deploy --image gcr.io/shaped-faculty-413418/modelosml --platform managed  --project=shaped-faculty-413418 --allow-unauthenticated