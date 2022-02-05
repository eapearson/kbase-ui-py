
APPNAME=$1
SCRIPT_HOME=`pwd`/tools/scripts/create-app
APP_HOME=`pwd`/django/$APPNAME
echo "Creating app: $APPNAME"
cd django
python manage.py startapp $APPNAME 
mkdir -p $APP_HOME/templates/$APPNAME
cp $SCRIPT_HOME/template-index.txt $APP_HOME/templates/$APPNAME/index.html
cp $SCRIPT_HOME/views.txt $APP_HOME/views.py
cp $SCRIPT_HOME/urls.txt $APP_HOME/urls.py
cat $SCRIPT_HOME/instructions.txt