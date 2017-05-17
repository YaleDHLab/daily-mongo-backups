# Daily Mongo Backups
> Get daily backups of your mongo databases

This repository contains a simple Python utility that can be used to send a daily backup of a mongo database to an email address. These backups can then be used to restore the database if anything catastrophic should happen to the server running the given database.

This utility is configured to run on Unix machines with mongo installed. Windows users could substitute Cygwin.

## Installation

To install the utility and its dependencies, run:

```
git clone https://github.com/YaleDHLab/daily-mongo-backups
cd daily-mongo-backups
pip install -r requirements.txt
```

## Configuration

Once you've installed the dependencies, you just need to specify your database name and email address in config.json:

```
{
  "db_name": "sample_db",
  "email_from_address": "douglas.duhaime@gmail.com",
  "email_to_address": "douglas.duhaime@gmail.com",
  "email_subject": "daily mongo backup",
  "email_message": "here is the daily mongo backup"
}
```

## Example usage

To create database backups, you'll need a mongo database with some data in it. For demonstration purposes, let's make a sample database and insert a simple record in that db:

```
mongo
use sample_db
db.items.insert({'hello':'world'})
exit()
```

Next, change `db_name` in config.json to "sample_db" (the db into which we just inserted a record). Once that's set, you can run:
```
python daily_mongo_backups.py
```

Once an email arrives, load the .tar.gz file onto your server and run:
```
tar -zxf dump.tar.gz
mongorestore --db sample_db_backup dump/sample_db

mongo sample_db_backup
db.items.find()
```
You should see the hello world document created above in your new database. If you do, then you're all set to start backing up your databases!