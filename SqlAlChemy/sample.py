from sql_reading import *

set_config = {
    "versionId": "6bc220e3c19f4f5c982499f3313ef862",
    "queryAnalysisId": "6bc220e3c19f4f5c982499f3313ef862",
    "analysisId": "6bc220e3c19f4f5c982499f3313ef862",
    "dispatchIp": "10.7.71.112",
    "dispatchPort": "7399",
    "dispatchWorkSpace": "/opt/workdir/atl",
}

sql_reading = SqlReading(set_config)

user_df = sql_reading.read_sql_by_sheet_name("user_df")

data = sql_reading.convert_df_to_sql_data(user_df)
sql_reading.insert_data_to_sql("user_df", data)
