import json
import os.path

import pandas as pd
import logging

# setting up top level logging config
logging.basicConfig(level=logging.INFO, filename='execution.log', format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('fileProcessor')


def config():
    # read parameters from config
    try:
        with open('config.json', 'r') as f:
            config = json.loads(f.read())

        # if target folder does not exist, make current folder as a target one
        if os.path.isdir(config['target_file_path']):
            target_file = config['target_file_path'] + config['target_file_name']
        else:
            target_file = config['target_file_name']

        source_file_path = config['source_files_path']

    except FileNotFoundError as e:
        raise RuntimeError(str(e))
    except KeyError as e:
        raise RuntimeError('There is a problem with the config file - ' + str(e) + ' is not found')


    letters = 'abcdefghijklmnopqrstuvwxyz'
    source_files = [source_file_path + item + '.csv' for item in letters]

    return target_file, source_files


def download_data(source_files):

    common_df = pd.DataFrame

    logger.info("Data downloading started")

    for item in source_files:
        logger.debug("Downloading data from " + item)
        try:
            df = pd.read_csv(item, sep=',')
            if common_df.empty:
                common_df = df.copy()
            else:
                common_df = pd.concat([common_df, df])
        except Exception as e:
            logger.error(str(e))

    logger.info("Download is OK")
    return common_df


def process_data(dataset, target_file):

    if dataset.empty:
        raise RuntimeError("No data to process. Check execution.log for details")
    else:

        logger.info("Data processing started")

        df_result = pd.DataFrame(dataset.groupby(['user_id', 'path'])['length'].sum()).reset_index()
        df_final = df_result.pivot(index='user_id', columns='path', values='length').fillna(0)

        df_final.to_csv(target_file)

        logger.info("Data processing is OK. Resulted dataset was downloaded to " + target_file)


def main():
    try:
        target_file, source_files = config()
        dataset = download_data(source_files)
        process_data(dataset, target_file)
    except Exception as e:
        print(str(e))
        logger.error(str(e))


if __name__ == '__main__':
    print("running....")
    main()
    print('done!')