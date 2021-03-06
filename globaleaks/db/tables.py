# -*- encoding: utf-8 -*-
#
#   tables
#   ******
# 
# Collect from the classes in models the structure of the DB tables, then
# Initialize the table if missing (executed only at the first start)

from twisted.internet.defer import inlineCallbacks

from storm.properties import PropertyColumn
from storm.exceptions import StormError

from storm.variables import BoolVariable, DateTimeVariable, DateVariable
from storm.variables import DecimalVariable, EnumVariable
from storm.variables import FloatVariable, IntVariable, RawStrVariable
from storm.variables import UnicodeVariable, JSONVariable, PickleVariable

from globaleaks import main
from globaleaks.config import config

def variableToSQLite(var_type):
    """
    We take as input a storm.variable and we output the SQLite string it
    represents.
    """
    sqlite_type = "VARCHAR"
    if isinstance(var_type, BoolVariable):
        sqlite_type = "INTEGER"
    elif isinstance(var_type, DateTimeVariable):
        pass
        sqlite_type = ""
    elif isinstance(var_type, DateVariable):
        pass
    elif isinstance(var_type, DecimalVariable):
        pass
    elif isinstance(var_type, EnumVariable):
        sqlite_type = "BLOB"
    elif isinstance(var_type, FloatVariable):
        sqlite_type = "REAL"
    elif isinstance(var_type, IntVariable):
        sqlite_type = "INTEGER"
    elif isinstance(var_type, RawStrVariable):
        sqlite_type = "BLOB"
    elif isinstance(var_type, UnicodeVariable):
        pass
    elif isinstance(var_type, JSONVariable):
        sqlite_type = "BLOB"
    elif isinstance(var_type, PickleVariable):
        sqlite_type = "BLOB"
    return "%s" % sqlite_type

def varsToParametersSQLite(variables, primary_keys):
    """
    Takes as input a list of variables (convered to SQLite syntax and in the
    form of strings) and primary_keys.
    Outputs these variables converted into paramter syntax for SQLites.

    ex.
        variables: ["var1 INTEGER", "var2 BOOL", "var3 INTEGER"]
        primary_keys: ["var1"]

        output: "(var1 INTEGER, var2 BOOL, var3 INTEGER PRIMARY KEY (var1))"
    """
    params = "("
    for var in variables[:-1]:
        params += "%s %s, " % var
    if len(primary_keys) > 0:
        params += "%s %s, " % variables[-1]
        params += "PRIMARY KEY ("
        for key in primary_keys[:-1]:
            params += "%s, " % key
        params += "%s))" % primary_keys[-1]
    else:
        params += "%s %s)" % variables[-1]
    return params

def generateCreateQuery(model):
    """
    This takes as input a Storm model and outputs the creation query for it.
    """
    query = "CREATE TABLE "+ model.__storm_table__ + " "

    variables = []
    primary_keys = []

    for attr in dir(model):
        a = getattr(model, attr)
        if isinstance(a, PropertyColumn):
            var_stype = a.variable_factory()
            var_type = variableToSQLite(var_stype)
            name = a.name
            variables.append((name, var_type))
            if a.primary:
                primary_keys.append(name)

    query += varsToParametersSQLite(variables, primary_keys)
    return query

def createTable(model):
    """
    Create the table for the specified model.
    """

    create_query = generateCreateQuery(model)

    try:
        config.main.zstorm.get('main_store').execute(create_query)
        config.main.zstorm.get('main_store').commit()

        return True
        
    # XXX trap the specific error that is raised when the table exists
    # seem to be OperationalError raised, but not a specific error exists.
    except StormError, e:
        print "Failed to create table!", e
        
def count(model):
    """
    @rtype : int
    @return: the count number of stored items 
    """

    return config.main.zstorm.get('main_store').find(model).count()

def runCreateTable(model):
    """
    Runs the table creation query wrapped in a transaction.
    Transactions run in a separate thread.
    """
    return main.transactor.run(createTable, model)
