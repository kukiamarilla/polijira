#!/bin/bash
echo "Ingresar varriables de entorno..."

# while : ; do
#     read -n 1 -s key <&1 > /dev/null
#     if [[ $key = q ]] ; then
#         exit
#     else
#         break
#     fi
# done

echo -n "Firebase Api Key: "
read fApiKey
echo -n "Firebase Auth Domain: "
read fAuthDomain
echo -n "Firebase Project ID: "
read fProjectId
echo -n "Firebase database url: "
read fDatabaseUrl
echo -n "Firebase Storage Bucket: "
read fStorageBucket
echo -n "Firebase Messaging Sender ID: "
read fMessagingSenderId
echo -n "Firebase App ID: "
read fAppId
echo -n "Firebase Private Key: "
read fPrivateKey
echo -n "Firebase Client Email: "
read fClientEmail
echo -n "Firebase Token URI: "
read fTokenUri
echo -n "Database Name: "
read dbName
echo -n "Database User: "
read dbUser
echo -n "Database Password: "
read -s dbPassword
echo " "
echo -n "Test User Email: "
read testEmail
echo -n "Test User Password: "
read -s testPassword

#if linux
if [ "$OSTYPE" = "linux-gnu" ]
then
    sudo su postgres <<EOF
    psql -c "DROP DATABASE $dbName"
    psql -c "DROP ROLE $dbUser"
    psql -c "CREATE USER $dbUser WITH PASSWORD '$dbPassword'"
    psql -c "ALTER USER $dbUser CREATEDB"
    psql -c "CREATE DATABASE $dbName OWNER $dbUser"
    echo "Postgres user '$dbUser' y database '$dbName' creado"
EOF
elif [ "$OSTYPE" = "darwin19" ]
then
    psql -U postgres -c "DROP DATABASE $dbName"
    psql -U postgres -c "DROP ROLE $dbUser"
    psql -U postgres -c "CREATE USER $dbUser WITH PASSWORD '$dbPassword'"
    psql -U postgres -c "ALTER USER $dbUser CREATEDB"
    psql -U postgres -c "CREATE DATABASE $dbName OWNER $dbUser"
    echo "Postgres user '$dbUser' y database '$dbName' creado"
fi

#.env en code
{
    echo 'CYPRESS_SETTINGS=backend.settings.cypress'
    echo ''
    echo 'FIREBASE_APP_ID='$fAppId
    echo 'FIREBASE_PROJECT_ID='$fProjectId
    echo 'FIREBASE_PRIVATE_KEY='$fPrivateKey
    echo 'FIREBASE_CLIENT_EMAIL='$fClientEmail
    echo 'FIREBASE_TOKEN_URI='$fTokenUri
    echo ''
    echo 'VUE_APP_FIREBASE_AUTH_DOMAIN='$fAuthDomain
    echo 'VUE_APP_FIREBASE_PROJECT_ID='$fProjectId
    echo 'VUE_APP_FIREBASE_DATABASE_URL='$fDatabaseUrl
    echo 'VUE_APP_FIREBASE_STORAGE_BUCKET='$fStorageBucket
    echo 'VUE_APP_FIREBASE_MESSAGE_SENDER_ID='$fMessagingSenderId
    echo 'VUE_APP_FIREBASE_APP_ID='$fStorageBucket
    echo ''
    echo 'TESTING_USER_EMAIL='$testEmail
    echo 'TESTING_USER_PASSWORD='$testPassword
} > .env

echo "INSTALANDO BACKEND"
echo "Creando entorno virtual..."
virtualenv -p python3 venv
echo ""
echo "Ingresando al entorno virtual..."
source venv/bin/activate
echo ""
echo "Intalando dependecias..."
pip install -r requirements.txt
echo ""
echo "Migrando DB..."
python manage.py migrate
echo ""
echo "Poblando DB..."
python manage.py flush
python manage.py loaddata backend/api/fixtures/initial/dev/*.json
echo ""
echo "PROYECTO DJANGO INSTALADO"
deactivate
echo ""


echo "INSTALANDO FRONTEND"

echo "Instalando dependencias npm..."
rm -Rf node_modules > /dev/null
npm install
npm run build

echo ""
echo "FRONTEND INSTALADO"
