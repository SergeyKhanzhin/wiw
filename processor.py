import pandas as pd
import logging

logger = logging.getLogger('threadProcessor')

def process_data(source_files) -> pd.DataFrame:
    common_df = pd.DataFrame
    for item in source_files:
        try:
            df = pd.read_csv(item, sep=',')
            if common_df.empty:
                common_df = df.copy()
            else:
                common_df = pd.concat([common_df, df])
        except Exception as e:
            logger.error(str(e))

    df_result = pd.DataFrame(common_df.groupby(['user_id', 'path'])['length'].sum()).reset_index()

    return df_result
