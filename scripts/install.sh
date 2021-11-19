echo "Ingresando..."
echo "Clonando repositorio git"
rm -Rf polijira
git clone git@github.com:kukiamarilla/polijira.git
cd polijira
echo "Haciendo checkout de tag"
git checkout $1
if [ $2 = 'produccion' ]
then
    echo "Ingresando a Produccion"
    sh ../prod.sh $1
else
    echo "Ingresando a Desarrollo"
    sh ../dev.sh
fi
