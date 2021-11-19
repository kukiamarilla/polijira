heroku login

echo -n "Ingrese el nombre de la aplicación de heroku"
read app

heroku apps:create $app
heroku git:remote -a $app
heroku addons:create heroku-postgresql:hobby-dev -a $app
heroku buildpacks:add heroku/nodejs -a $app
heroku buildpacks:add heroku/python -a $app

echo -n "Firebase Client Email: "
read fClientEmail
fPrivateKey=`cat ../firebase_private.prod.key`
echo -n "Firebase Project ID: "
read fProjectId
echo -n "Firebase Token URI: "
read fTokenUri
echo -n "Firebase Api Key: "
read fApiKey
echo -n "Firebase App ID: "
read fAppId
echo -n "Firebase Auth Domain: "
read fAuthDomain
echo -n "Firebase Messaging Sender ID: "
read fMessagingSenderId
echo -n "Firebase Storage Bucket: "
read fStorageBucket

heroku config:set DJANGO_SECRET_KEY=92429d82a41e930486c6de5ebda9602d55c39986  -a $app
heroku config:set DJANGO_SETTINGS_MODULE=backend.settings.prod  -a $app

heroku config:set FIREBASE_CLIENT_EMAIL=$fClientEmail -a $app
heroku config:set FIREBASE_PRIVATE_KEY="$fPrivateKey" -a $app
heroku config:set FIREBASE_PROJECT_ID=$fProjectId -a $app
heroku config:set FIREBASE_TOKEN_URI=$fTokenUri -a $app
heroku config:set VUE_APP_FIREBASE_API_KEY=$fApiKey -a $app
heroku config:set VUE_APP_FIREBASE_APP_ID=$fAppId -a $app
heroku config:set VUE_APP_FIREBASE_AUTH_DOMAIN=$fAuthDomain -a $app
heroku config:set VUE_APP_FIREBASE_MESSAGING_SENDER_ID=$fMessagingSenderId -a $app
heroku config:set VUE_APP_FIREBASE_PROJECT_ID=$fProjectId -a $app
heroku config:set VUE_APP_FIREBASE_STORAGE_BUCKET=$fStorageBucket -a $app

git push heroku $1:master