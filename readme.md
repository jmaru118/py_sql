Jonathan Martinez
PA2 Design Document
3/12/19

Program uses Python 2.7
Run using "python pa2 < PA2_test.sql"

	My program has the ability accept input via command line arugments, redirection operator (<), or filename input once inside the program. This file must reside within the same directory as the pa1.py file and is case sensitive. Once the file is located, the contents are then read in and parsed into a stack. The stack of commands are then executed until there are no more actions to run.
	This program will grab the current directory once it is run and use this as the main directory for database file manipulation. We will refer to this as the root. Whenever a new database is created it will always be created at the root. A database is represented by a new folder within the root. Folders are case sensitive and you can have as many as you like so long as the names do no conflict. 
Tables can only be created inside databases. Tables are represented by text files that reside inside the folders and just like folders you can have as many as you like so long as the names do not conflict. 
The create table function will check to see if you are working inside of a database, if you are then it will create the new table so long as the current table name does not already exist. You can have the same table name so long as they exist within differing databases, for example tbl1 can exist within db1 and db2, but db1 cannot have more than one copy of tbl1. 
The create database function will grab the root directory and check to see if the database to be created already exists, if it does exist then nothing will happen. If the database does not exist then it will go ahead and create the new database. You cannot create a database within a database. Databases can only be created in the root directory and are case sensitive. 
This new iteration adds in the following extra functions
		# INSERT
		Adds extra data into the table
        # MODIFY
        Helper function for the update function
        # UPDATE
        Updates data within a table
        # DELETE
        Deletes lines in a table depending on criterion