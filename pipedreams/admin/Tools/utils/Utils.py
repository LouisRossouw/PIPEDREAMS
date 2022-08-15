import json
import yaml
import datetime
import calendar

import logging


log = logging.getLogger(__name__)


def test():


    log.info("Hello logging!")
    log.error("ahhhhhhhhhhh!")
    log.debug("HH")

#            # Configs

def yaml_config(config_path):
    """ Open yaml configs """
    config = yaml.safe_load(open(config_path))
    return(config)




#        # Json read/write ata

def write_to_json(json_path, data):
    """ Create and write to json file """
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=6)

def read_json(json_path):
    """ Reads json file """
    with open(json_path) as f:
        json_file = json.loads(f.read())

    return(json_file)




def get_dates():
    # Date functions
    date_now_full = (str(datetime.datetime.now()))
    date_now = (str(datetime.datetime.now()).split(' ')[0])
    date_time = (str(datetime.datetime.now()).split(' ')[1])
    day_num = datetime.datetime.today().day
    day_name = calendar.day_name[datetime.date.today().weekday()]
    date_year = datetime.datetime.today().year
    day_month_num = datetime.datetime.today().month
    day_month_name = calendar.month_name[day_month_num]

    dict = {}
    dict['date_NOW'] = [date_now, date_time, day_num, day_name, date_year, day_month_num, day_month_name, date_now_full]
    
    return(date_now, date_time, day_num, day_name, date_year, day_month_num, day_month_name, dict, date_now_full)
