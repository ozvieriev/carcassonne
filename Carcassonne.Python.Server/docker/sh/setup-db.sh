#!/bin/bash
export sqlcmd="/opt/mssql-tools18/bin/sqlcmd -S . -C -U sa -P $MSSQL_SA_PASSWORD"

echo Dropping databases... $USER_PASSWORD
$sqlcmd -Q "EXEC msdb.dbo.sp_delete_database_backuphistory $GAME"
$sqlcmd -Q "if db_id('$GAME') is not null ALTER DATABASE [$GAME] SET SINGLE_USER WITH ROLLBACK IMMEDIATE"
$sqlcmd -Q "if db_id('$GAME') is not null DROP DATABASE [$GAME]"

echo Dropping user...
$sqlcmd -Q "if exists (select loginname from master.dbo.syslogins where name = '$USER') EXEC sp_droplogin @loginame='$USER'"

echo Creating user...
$sqlcmd -Q "EXEC sp_addlogin @loginame='$USER', @passwd='$USER_PASSWORD'"

echo Creating database $GAME...
export sqlpackage="/tmp/sqlpackage/sqlpackage /a:import /tsn:localhost /tdn:$GAME /sf:/backups/$GAME.bacpac  /tu:sa /tp:$MSSQL_SA_PASSWORD /ttsc:true"
$sqlpackage

$sqlcmd -d $GAME -Q "EXEC sp_adduser @loginame='$USER'"
$sqlcmd -d $GAME -Q "EXEC sp_addrolemember N'db_owner', N'$USER'"
 
echo Done