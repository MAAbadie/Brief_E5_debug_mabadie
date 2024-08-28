import pandas as pd
import requests
from src.utils import logger_error


class GetData(object):

    def __init__(self, url) -> None:
        self.logger = logger_error(__name__)
        self.url = url
        self.data = None
        try:
            response = requests.get(self.url)
            self.data = response.json()
        except requests.exceptions.ConnectTimeout or requests.exceptions.ConnectionError:
            self.logger.error(f"ERROR WHILE RETRIEVING DATA FROM {url}", exc_info=True)      

    def processing_one_point(self, data_dict: dict):

        temp = pd.DataFrame({key:[data_dict[key]] for key in ['datetime', 'trafficstatus', 'geo_point_2d', 'averagevehiclespeed', 'traveltime', 'trafficstatus']})
        temp = temp.rename(columns={'trafficstatus':'traffic'})
        temp['lat'] = temp.geo_point_2d.map(lambda x : x['lat'])
        temp['lon'] = temp.geo_point_2d.map(lambda x : x['lon'])
        del temp['geo_point_2d']

        return temp

    def __call__(self):

        res_df = pd.DataFrame({})

        if self.data is not None:
            for data_dict in self.data:
                temp_df = self.processing_one_point(data_dict)
                res_df = pd.concat([res_df, temp_df])

            res_df = res_df[res_df.traffic != 'unknown']
        else:
            self.logger.error(f"ERROR DATA RETRIEVED IS EMPTY", exc_info=True)

        return res_df