# Author: Jonathan Martinez
# CS457
# PA1
# run "python pa1.py" without any command line arguments. You will be prompted
# to enter a command or file to run. Please only use local .sql files if you are
# importing a file
# The program will then parse through the sql commands and run them line by line


# File structure
    # IMPORTS
    # FUNCTION DEFINITIONS
        # CREATE
        # DROP
        # USE
        # SELECT
        # ALTER
        # parse_file
    # MAIN
    
    
############################################################
#                       IMPORTS                            #
############################################################
import os, sys, shutil


############################################################
#                     GLOBAL VARS                          #
############################################################
MAIN_DIR = os.getcwd() # will be used for file manipulation




############################################################
#                    FUNCTION DEFS                         #
############################################################

#######  DEFINE FUNCTION CREATE() ##################
# creates either a table or database if it does not
# already exist. This function has optional parameters
# for when a user is creating a table with metadata
def CREATE(item_type, item_name, *metadata):
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
        

#######  DEFINE FUNCTION DROP() #####################
# can be used to delete table or database

def DROP(item_type, item_name):
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


#######  DEFINE FUNCTION USE() #####################
def USE(db_name):
    # create new path for new db to use
    useDb = MAIN_DIR + "/" + db_name + "/"
    
    # see if db exists
    if os.path.exists(useDb):
        os.chdir(useDb)
        print("-- Using database " + db_name)
    else:
        print("-- Error " + db_name + " does not exist, please create the database first then try again")
        

#######  DEFINE FUNCTION SELECT() #####################
#     Returns data found within a table               #
def SELECT(atr, frm, tbl_nm):
    
    # create path for table to use
    use_tbl = os.getcwd() + "/" + tbl_nm

    # if atr = * then we want all the attributes
    if atr == '*':
        # see if tbl exists
        if os.path.exists(use_tbl):
            f = open(use_tbl, "r")
            file_contents = f.read()
            print("-- " + file_contents)
            f.close()
    else:
        print("ONLY ATRRIBUTE * HAS BEEN IMPLEMENTED")
            
    # section to allow for user input

#######  DEFINE FUNCTION ALTER() #####################
def ALTER(item_type, item_name, cmd, *req):
    # create path for table to use
    item = os.getcwd() + "/" + item_name
    additions = "" # will be used for extra additions to table metadata
    
    # grab *req variables
    if len(req) > 1:
        for data in req:
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

#######  DEFINE FUNCTION parse_file() ################
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
                #remove the semicolon
                left, right = str(line).split(";",1)
                # add command to the stack
                commands.extend(left.split())
    #if file doesn't exist return false
    else:
        return False
        
    return True
    
    
    
############################################################
#                         MAIN                             #
############################################################
if __name__ == '__main__':
    ############# variables #################################
    keep_alive = True
    action = ""
    commands = [] # will be used to store commands if read directly from a file
    meta = [] #will be used to hold metadata for tables
    
    
    # check for command line argument
    if len(sys.argv) > 1:
        action = sys.argv[1]
    else:
        print("no command line arguments issued")
        action = raw_input('Enter a command or filename to execute: ')
        

    #################### BEGIN MAIN FUNCTIONALITY LOOP #########################
    while keep_alive or len(commands) > 0:
        # check menu option
        if action == ".EXIT":
            keep_alive = False
            if len(commands) > 0:
                commands[:] = []
                
            
        ################ CREATE ACTION ######################################
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
                    while ')' not in commands[0]:
                        #remove first '('
                        temp = commands.pop(0)
                        if temp[0] == '(':
                            temp = temp[1:]
                        meta.append(temp)
                    # make sure we didn't miss an item
                    if ')' in commands[0]:
                        temp = commands.pop(0)
                        #strip final ')'
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
                print("no more actions to run")
                action = ".EXIT"
                
                
        ###### DROP ACTION ########################################
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
                print("no more actions to run")
                action = ".EXIT"
            
            
        ################# USE ACTION ##########################
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
                print("no more actions to run")
                action = ".EXIT"
                
        ################# SELECT ACTION ##########################
        elif action == "SELECT" or action =="select":
            # go to the select function
            
            if len(commands) > 2:
                SELECT(commands.pop(0), commands.pop(0), commands.pop(0))
            else:
                print("NOT YET IMPLEMENTED OR NOT ENOUGH ITEMS IN COMMAND STACK")
                atr = raw_input("SELECT which atributes? Use * for ALL: ")
                tbl = raw_input("SELECT from which TABLE? ")
                SELECT(atr, "FROM", tbl)
                
            #update action if script still has more actions to run
            if len(commands) > 0:
                action = commands.pop(0)
            else:
                action = "empty"
            
        elif action == "empty":
            keep_alive = True
            action = raw_input("Enter a command or Filename to execute: ")
            
        ################# ALTER ACTION ##########################
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
                action = "empty"
            
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