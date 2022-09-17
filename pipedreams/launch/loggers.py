import os
import utils
import logging





def create_logger(logger_name):
    """ create logger to log information to the /admin/logs directory, it creates a seperate log file for each user """

    pipeline_config = utils.open_PipeLine_Config()
    logger_disabled_query = pipeline_config["logger_disabled"] # True or False, activate or deactivate the logger

    userName = os.environ['COMPUTERNAME']


    # create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(f'pipedreams/admin/logs/{userName}_DreamLOG.log')
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.disabled = logger_disabled_query

    return(logger)




if __name__ == "__main__":

    create_logger()