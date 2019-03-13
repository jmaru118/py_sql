# Author: Jonathan Martinez
# CS457
# PA2 - Python 2
# This program can be run without any arguments "python pa2.py"
# This program can be run with command line args "python pa2.py filename"
# This program can be run with redirection "python pa2.py < filename"
# The program will then parse through the sql commands and run them line by line
# or prompt for user input if no script is loaded


# File structure
    # IMPORTS
    # FUNCTION DEFINITIONS
        # CREATE
        # DROP
        # USE
        # SELECT
        # ALTER
        # parse_file
        # parseScript
        # INSERT
        # MODIFY
        # UPDATE
        # DELETE
    # MAIN
    
    
############################################################
#                       IMPORTS                            #
############################################################
import os, sys, shutil, re


############################################################
#                     GLOBAL VARS                          #
############################################################
MAIN_DIR = os.getcwd() # will be used for file manipulation




############################################################
#                    FUNCTION DEFS                         #
############################################################

#####################  DEFINE FUNCTION CREATE() ##################
# creates either a table or database if it does not
# already exist. This function has optional parameters
# for when a user is creating a table with metadata
def CREATE(item_type, item_name, *metadata):
    # strip semicolon from item_name if it exists
    if item_name.endswith(";"):
        item_name = item_name[:-1]
        
    # set directory for database or table
    newdb = MAIN_DIR + "/" + item_name + "/"
    newItem = os.getcwd() + "/" + item_name

    
    # TABLE
    if item_type == "TABLE" or item_type == "table":
        if os.path.exists(newItem):
            print("-- !Failed to create table " + item_name + " because it already exists.")
        else:
            #create the table
            f = open(item_name,"w+")
            #write metadata to table
            if len(metadata) > 0:
                metadata = metadata[0]
                for data in metadata:
                    if ',' in data:
                        data, discard = str(data).split(',')
                        f.write(str(data) + " | ")
                    else:
                        # strip last ) if it exists
                        if data.endswith(")"):
                            data = data[:-1]
                        f.write(str(data) + " ")
            f.write(" ")
            f.close()
            print("-- Table " + item_name + " created.")

    
    # DATABASE
    if item_type == "DATABASE" or item_type == "database":
        #check if the database already exists
        if os.path.exists(newdb):
            print("-- !Failed to create database " + item_name + " because it already exists.")
        else:
            os.mkdir(newdb)
            print("-- Database " + item_name + " created.")
        

#####################  DEFINE FUNCTION DROP() #####################
# can be used to delete table or database

def DROP(item_type, item_name):
    #remove ";" if it exists
    if item_name.endswith(";"):
        item_name = item_name[:-1]
    # SET paths
    dropdb = MAIN_DIR + "/" + item_name + "/"
    
    # TABLE
    if item_type == "TABLE" or item_type == "table":
        #append folder name to cwd
        dropTable = os.getcwd() + "/" + item_name
        #check if the table already exists
        if os.path.exists(dropTable):
            os.remove(dropTable)
            print("-- " + str(item_type).upper() + " " + item_name + " deleted")
        else:
            print("-- !Failed to delete table " + item_name + " because it does not exist.")
    
    # DATABASE
    if str(item_type).lower() == "database":
        #check if the database already exists
        if os.path.exists(dropdb):
            shutil.rmtree(dropdb, ignore_errors=True)
            print("-- " + str(item_type).upper() + " " + item_name + " deleted")
        else:
            print("-- !Failed to delete database " + item_name + " because it does not exist.")


#####################  DEFINE FUNCTION USE() #####################
def USE(db_name):
    # remove semicolon from db_name if it exists
    if db_name.endswith(";"):
        db_name = db_name[:-1]
    # create new path for new db to use
    useDb = MAIN_DIR + "/" + db_name
    
    # see if db exists
    if os.path.exists(useDb):
        os.chdir(useDb)
        print("-- Using database " + db_name)
    else:
        print("-- Error " + db_name + " does not exist, please create the database first then try again")
        

#####################  DEFINE FUNCTION SELECT() #####################
#     Returns data found within a table               #
def SELECT(*args):
    args = args[0]
    # select * from product
    # select name, price
    atr = args.pop(0)
    if str(atr).lower() == "*":
        args.pop(0) # remove from
        tbl_nm = args.pop(0)
        # remove semicolon from db_name if it exists
        if tbl_nm.endswith(";"):
            tbl_nm = tbl_nm[:-1]
    else:
        # grab args until done
        if str(atr).endswith(","): # we have more args to grab
            atr = atr[:-1] # strip comma
            atr2 = args.pop(0)
            args.pop(0) # pop "from"
            tbl_nm = args.pop(0)
            if args[0] == "where":
                args.pop(0)
                lhs = args.pop(0)
                comp = args.pop(0)
                rhs = args.pop(0)
                rhs = rhs[:-1]
        
    # create path for table to use
    use_tbl = os.getcwd() + "/" + str(tbl_nm).capitalize()

    # if atr = * then we want all the attributes
    if atr == '*':
        # see if tbl exists
        if os.path.exists(use_tbl):
            f = open(use_tbl, "r")
            file_contents = f.readlines()
            for line in file_contents:
                print("-- " + line[:-1])
            f.close()
    else: # defaulting to name and price
        if os.path.exists(use_tbl):
            f = open(use_tbl, "r")
            file_contents = f.readlines()
            f.close()
            for line in file_contents:
                if re.match("^pid", line):
                    print("-- "+line[10:-1])
                elif line.startswith("2"):
                    pass
                else:
                    print("-- "+line[3:])
            
            
    # section to allow for user input

#####################  DEFINE FUNCTION ALTER() #####################
def ALTER(item_type, item_name, cmd, *req):
    # create path for table to use
    item = os.getcwd() + "/" + item_name
    additions = "" # will be used for extra additions to table metadata
    
    # grab *req variables
    if len(req) > 1:
        for data in req:
            #strip semicolon if it exists
            if data.endswith(";"):
                data = data[:-1]
            additions = additions + data + " "

            
    # Check for TABLE
    if str(item_type).lower() == "table":
        # check if table exists
        if os.path.exists(item):
            # check for command
            if str(cmd).lower() == "add":
                with open(item) as f:
                    file_lines = f.readlines()
                    file_lines[0] = file_lines[0] + "| " + str(additions)
                    f.close()
                with open(item, "w") as f:
                    f.writelines(file_lines)
                    f.close()
                # print comfirmation
                print("-- Table " + item_name + " modified.")
            else:
                print("Only ADD has been implemented")
        else:
            # table doesn't exist or not found
            print("-- !Failed to query table tbl_1 because it does not exist.")
    
    # else DB
    elif str(item_type).lower() == "database" or str(item_type).lower() == "db":
        print("NOT YET IMPLEMENTED - ALTER(DATABASE)")

#####################  DEFINE FUNCTION parse_file() ##############################
#     takes in a text.sql and parses the commands    #
def parse_file(lhs,rhs,commands):
    #reassemble filename
    filename = lhs + "." + rhs
    
    # check if file exists
    cwd = os.getcwd()
    search = cwd + "/" + filename
    if os.path.exists(search):
        file = open(filename,"r")
        for line in file:
            # if line begins with a '.' it is a valid command
            if str(line[0]) == '.':
                commands.append(line.strip())
            # if line begins with an alphabet character it is a valid command
            elif str(line[0]).isalpha():
                # add command to the stack
                commands.extend(line.split())
    #if file doesn't exist return false
    else:
        return False
        
    return True

#####################  DEFINE FUNCTION parseScript() ##############################
#     takes in a stdin buffer and parses the commands #
def parseScript(cmd_arr):
    for line in sys.stdin:
        # cmd_arr.append(line.strip("\r\n"))
        # if line begins with a '.' it is a valid command
        if str(line[0]) == '.':
            cmd_arr.append(line.strip())
        # if line begins with an alphabet character it is a valid command
        elif str(line[0]).isalpha():
            # #remove the semicolon if it exists
            # if str(line[:-2]).endswith(";"):
            #     left, right = str(line).split(";",1)
            #     cmd_arr.extend(left.split())
            # else:
                # add command to the stack
            cmd_arr.extend(line.split())
    
#####################  DEFINE FUNCTION INSERT ##############################
#     adds new items into the requested table  #
def INSERT(*args):
    # variables
    # discard first arg
    args = args[0]
    args.pop(0)
    filename = args.pop(0)
    
    # check if table exists
    table = os.getcwd() + "/" + filename
    if os.path.exists(table):
        file = open(filename,"a")
        file.write("\n")
        for i in range(len(args)): # loop through and write all the args
            file.write(args.pop(0) + " ")
        file.close()
        print("-- 1 new record inserted.")

#####################  DEFINE FUNCTION MODIFY ##############################
#     helper for update function  #
def MODIFY(tbl, action, mod, where):
    where = where[:-1]
    
    # look for name to replace
    if str(action).lower() == "name":
        file = open(tbl, "r")
        data = file.read()
        file.close()
        
        data = data.replace(where,mod)
        wfile = open(tbl, "w")
        wfile.writelines(data)
        wfile.close()
        print("-- 1 record modified.")
    # look for price to replace
    elif str(action).lower() == "price":
        file = open(tbl, "r")
        data = file.readlines()
        file.close()
        for i in range(len(data)):
            if where in data[i]:
                data[i] = re.sub('\d+.\d+', mod, data[i])
        wfile = open(tbl, "w")
        wfile.writelines(data)
        wfile.close()
        print("-- 2 records modified.")
        

#####################  DEFINE FUNCTION UPDATE ##############################
#     updates data within a table  #
def update(tbl_name, *args):
    args = args[0]
    setname = " "
    setprice = 0
    where = " "

    # make sure table exists
    table = os.getcwd() + "/" + tbl_name
    if os.path.exists(table):
        if str(args.pop(0)).lower() == "set":
            updateAction = str(args.pop(0)).lower()
            if updateAction == "name":
                args.pop(0)
                setname = args.pop(0)
                args.pop(0)
                args.pop(0)
                args.pop(0)
                where = args.pop(0)
                MODIFY(table, "name", setname, where)
            elif updateAction == "price":
                args.pop(0)
                setprice = args.pop(0)
                args.pop(0)
                args.pop(0)
                args.pop(0)
                where = args.pop(0)
                MODIFY(table, "price", setprice, where)

#####################  DEFINE FUNCTION DELETE ##############################
#     deletes data within a table  #
def DELETE(tbl_name, *args):
    args = args[0]
    where = " "
    counter = 0
    m = None #used for regex matching
    
    # make sure table exists
    table = os.getcwd() + "/" + str(tbl_name).capitalize()
    if os.path.exists(table):
        args.pop(0) # pop extra word "where"
        updateAction = str(args.pop(0)).lower()
        
        # open file and begin delete lines with name
        file = open(str(tbl_name).capitalize(), "r")
        data = file.readlines()
        file.close()

        # go through file finding lines to delete
        mydata = [] # used to hold lines to write
            
            
        if updateAction == "name":
            args.pop(0) # removes =
            where = args.pop(0) # grabs name literal
            where = where[:-1]
            
            for line in data:
                if where not in line:
                    mydata.append(line)
                elif where in line:
                    counter += 1
            wfile = open(str(tbl_name).capitalize(), "w")
            wfile.writelines(mydata)
            wfile.close()
            print("-- " + str(counter) + " records deleted.")
            
        elif updateAction == "price":
            comp = args.pop(0) # grabs the comparator symbol
            where = args.pop(0) # grabs price value
            # check for lingering semicolon
            if ";" in where:
                where = where[:-1]
            # check price requirement
            if str(comp) == ">":
                for line in data:
                    mydata.append(line)
                    m = re.search('(\d+\.\d+)',line) # look for monetary values
                    if m:
                        if float(m.group(1)) > float(where): # check our comparator
                            mydata = mydata[:-1] # we ignore this line since we don't want it
                            counter += 1
                            
                wfile = open(str(tbl_name).capitalize(), "w")
                wfile.writelines(mydata)
                wfile.close()
                
        # remove extra space
        if counter > 0:
            with open(str(tbl_name).capitalize(), 'rb+') as filehandle:
                filehandle.seek(-1, os.SEEK_END)
                filehandle.truncate()
                
            print("-- " + str(counter) + " records deleted.")
                    
        

#####################################################################################
#                                    MAIN                                           #
#####################################################################################
if __name__ == '__main__':
    ############# variables #################################
    keep_alive = True
    action = ""
    commands = [] # will be used to store commands if read directly from a file
    meta = [] #will be used to hold metadata for tables
    # myinput = sys.stdin.readline()[:10]
    chkfile = True;
    
    # check for command line argument
    if len(sys.argv) > 1:
        action = sys.argv[1]
    else:
        action = raw_input()
        

    #################### BEGIN MAIN FUNCTIONALITY LOOP #########################
    while keep_alive or len(commands) > 0:
        # check menu option
        if str(action).lower() == ".exit":
            keep_alive = False
            if len(commands) > 0:
                commands[:] = []
                
            
        ######################### TEST for CS457 Script ##############################
        elif chkfile:
            if action[:10] == "--CS457 PA":
                parseScript(commands)
                action = commands.pop(0)
                keep_alive = False
                chkfile = False
            
        ######################### CREATE ACTION ######################################
        elif action == "CREATE" or action == "create":
            # if script is loaded use that to create
            if len(commands) > 0:
                create_type = commands.pop(0)
                create_name = commands.pop(0)

                # if creating a table we need metadata
                if str(create_type).lower() == 'table':
                    # clear metadata array
                    meta[:] = []
                    #grab metadata until we've reached ')'
                    while ';' not in commands[0]:
                        #remove first '('
                        temp = commands.pop(0)
                        if temp[0] == '(':
                            temp = temp[1:]
                        meta.append(temp)
                    # make sure we didn't miss an item
                    if ';' in commands[0]:
                        temp = commands.pop(0)
                        #strip final ';'
                        temp = temp[:-1]
                        meta.append(temp)
            # else grab user input
            else:
                create_type = raw_input("Create a TABLE or DATABASE? ")
                create_name = raw_input("Please name your " + str(create_type).upper() + ": ")
            
            # create desired item
            CREATE(create_type, create_name, meta)
            
            #update action if script still has more actions to run
            if len(commands) > 0:
                action = commands.pop(0)
            else:
                action = raw_input("Enter a command or Filename to execute: ")
                
                
        ######################## DROP ACTION ########################################
        elif action == "DROP" or action =="drop":
            # if script is loaded use that to create
            if len(commands) > 0 and keep_alive == False:
                drop_type = commands.pop(0)
                drop_name = commands.pop(0)
            else:
                drop_type = raw_input("DROP a TABLE or DATABASE? ")
                drop_name = raw_input("Which " + str(drop_type).upper() + "? ")
            DROP(drop_type, drop_name)
            
            #update action if script still has more actions to run
            if len(commands) > 0:
                action = commands.pop(0)
            else:
                action = raw_input("Enter a command or Filename to execute: ")
            
            
        ########################## USE ACTION ###################################
        elif action == "USE" or action =="use":
            # if script is loaded use that to create
            if len(commands) > 0 and keep_alive == False:
                USE(commands.pop(0))
            else:
                USE(raw_input("Use which DB? "))
                
            #update action if script still has more actions to run
            if len(commands) > 0:
                action = commands.pop(0)
            else:
                action = raw_input("Enter a command or Filename to execute: ")
                
        ########################## SELECT ACTION ###################################
        elif action == "SELECT" or action =="select":
            # go to the select function
            
            if len(commands) > 2:
                #               *            from           product
                SELECT(commands)
            else:
                print("NOT YET IMPLEMENTED OR NOT ENOUGH ITEMS IN COMMAND STACK")
                atr = raw_input("SELECT which atributes? Use * for ALL: ")
                tbl = raw_input("SELECT from which TABLE? ")
                SELECT(atr, "FROM", tbl)
                
            #update action if script still has more actions to run
            if len(commands) > 0:
                action = commands.pop(0)
            else:
                action = raw_input("Enter a command or Filename to execute: ")

            
        ########################## ALTER ACTION ###################################
        elif str(action).lower() == "alter":
            # go to the alter function
            # check if we're using a script
            if len(commands) > 3:
                # alter( item_type, item_name, cmd, req )
                # currently only works with 1 command at a time
                # i.e. ADD a3 float 
                ALTER(commands.pop(0), commands.pop(0), commands.pop(0), commands.pop(0), commands.pop(0))
            else:
                print("NOT YET IMPLEMENTED OR NOT ENOUGH ITEMS IN COMMAND STACK")
                
            #update action if script still has more actions to run
            if len(commands) > 0:
                action = commands.pop(0)
            else:
                action = raw_input("Enter a command or Filename to execute: ")
            
        ######################## INSERT ACTION ###################################################
        elif str(action).lower() == "insert":
            # if script is loaded use that to create
            if len(commands) > 0 and keep_alive == False:
                # clear metadata array
                meta[:] = []
                #grab metadata until we've reached ')'
                while ';' not in commands[0]:
                    #remove first '('
                    temp = commands.pop(0)
                    if temp.startswith("values("):
                        temp = temp[7:]
                    meta.append(temp)
                # make sure we didn't miss an item
                if ';' in commands[0]:
                    temp = commands.pop(0)
                    #strip final ';'
                    temp = temp[:-2]
                    meta.append(temp)
                INSERT(meta)
            else:
                insert_type = raw_input("Which insert action: ")
                insert_name = raw_input("Which table: ")
                insert_values = raw_input("Enter values to insert: ")
                INSERT(insert_type, insert_name, insert_values)
            
            #update action if script still has more actions to run
            if len(commands) > 0:
                action = commands.pop(0)
            else:
                action = raw_input("Enter a command or Filename to execute: ")
        
        ######################## UPDATE ACTION ###################################################
        elif str(action).lower() == "update":
            # if script is loaded use that to create
            if len(commands) > 0 and keep_alive == False:
                update(commands.pop(0), commands)
                
            else:
                table = raw_input("update which table? ")
                update(table)
                
            #update action if script still has more actions to run
            if len(commands) > 0:
                action = commands.pop(0)
            else:
                action = raw_input("Enter a command or Filename to execute: ")
                
        ######################## DELETE ACTION ###################################################
        elif str(action).lower() == "delete":
            # if script is loaded use that to create
            if len(commands) > 0 and keep_alive == False:
                commands.pop(0) # remove "from"
                DELETE(commands.pop(0), commands)
                
            else:
                table = raw_input("update which table? ")
                update(table)
                
            #update action if script still has more actions to run
            if len(commands) > 0:
                action = commands.pop(0)
            else:
                action = raw_input("Enter a command or Filename to execute: ")
              
        ################# EMPTY ACTION #########################
        elif action == "empty":
            keep_alive = True
            action = raw_input("Enter a command or Filename to execute: ")
        #####################################################    
        # checking for a filename with .sql
        else:
            try:
                lhs, rhs = action.split(".", 1)
            except ValueError:
                rhs = ' '
            if rhs == "sql":
                if parse_file(lhs,rhs,commands):
                    action = commands.pop(0)
                    keep_alive = False
                else:
                    action = "invalid"
            else:
                print("Invalid command - if you want to quit the program use .EXIT")
                print("If you are attempting to use a file please make sure the file is in the same directory")
                print("as pa1.py and then use FILENAME.sql")
                action = raw_input('Enter a command or filename to execute: ')

    
    print("-- All done.")