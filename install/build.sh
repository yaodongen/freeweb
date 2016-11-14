

echo "输入mysql密码..."
mysql_config_editor set --login-path=local --user=root --password

echo "建立数据库和表..."
mysql --login-path=local <database.sql 





