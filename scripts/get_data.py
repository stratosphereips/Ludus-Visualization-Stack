import datetime
import os
import txt2json


def get_file_path(backup_path, table):
    if not os.path.exists(backup_path):
        os.mkdir(backup_path)
    d = datetime.datetime.now()
    download_file_path= os.path.join(backup_path,('{}-{}'.format(d.strftime('%Y%m%d%H%M'),table)))
    return download_file_path

def backup(backup_path, args, table_psql, table_mysql, last):
    '''
    Backs up data from postgres database to mysql database
    '''
    identifier = 'json_id'
    file_path = get_file_path(backup_path, table_psql) # get filename of current data
    
    ### (1) Get newly updated entries in postgres database
    query =  "\copy (SELECT * FROM {} where {} > {} ORDER BY {} ASC) TO PROGRAM 'gzip -c > {}.txt.gz' (DELIMITER('|'));".format(table_psql,identifier, last, identifier, file_path)
        
    psql_command = 'psql -c "{}" --host=localhost --port=5432 --username={} --dbname={}'.format(query, args[0],"sentinel")    
    
    os.environ['PGPASSWORD']='{}'.format(args[1])
    os.system(psql_command)
    os.system('gzip -d {}.txt.gz'.format(file_path))
    
    
    ### (2) Upload data from (1) into mysql database
    load_data_to_db = "LOAD DATA LOCAL INFILE '{}.txt' INTO TABLE {} FIELDS TERMINATED BY '|';".format(file_path, table_mysql)
    mysql_command = 'mysql -u{} -p{} {} -e"{}"'.format(args[5], args[6], 'sentinel_backup', load_data_to_db)
    
    
    os.system(mysql_command)
    
    fin = '{}.txt'.format(file_path)
    fout = '{}.json'.format(file_path)
    parser = txt2json.parse_raw_dat(fin,fout)

    try:
        last = parser.find_last_row()
    except:
        print('No new entries have been added to postgres table')
    
    return file_path, last    
    
    

	
