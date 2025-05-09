import tomllib

import aiohttp
import jieba
from loguru import logger
from utils.pluginbase import *

class 天气(PluginBase):
    #https://dev.qweather.com/docs/finance/pricing/#weather-and-environment

    # Change Log
    # 1.0.1 2025-02-20 修改天气插件触发条件

    def __init__(self):
        self.metadata = {
            "name": "天气",
            "version": "1.0.0",
            "author": "fg",
            "description": "天气查询插件",
            "priority": 50,
            "block": False
        }
        self.enable()
        self.command_format = """⚙️获取天气：
        天气 城市名
        天气城市名
        城市名天气
        城市名 天气"""
        self.api_key = ''#自己的key

    async def process(self, msg: Msg):
        if "天气" not in msg.content or msg.is_group == False:
            return
        content = str(msg.content).replace(" ", "")
        command = list(jieba.cut(content))

        if len(command) == 1:
            await self.clinet.发送文本("\n" + self.command_format,msg.roomid, msg.sender)
            return
        elif len(command) > 3:
            return

        # 配置密钥检查
        if not self.api_key:
            await self.clinet.发送文本("\n你还没配置天气API密钥！",msg.roomid,  msg.sender)
            return

        command.remove("天气")
        request_loc = "".join(command)
        headers = {
            "X-QW-Api-Key": f'{self.api_key}'
        }
        params = {
            "location":request_loc
        }
        geo_api_url = "https://mg73jp2xt6.re.qweatherapi.com/geo/v2/city/lookup"#替换自己的域名
        conn_ssl = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.request('GET', url=geo_api_url, connector=conn_ssl,headers=headers, params=params) as response:
            geoapi_json = await response.json()
            await conn_ssl.close()

        if geoapi_json['code'] == '404':
            self.clinet.发送文本( "\n⚠️查无此地！",msg.roomid, msg.sender)
            return

        elif geoapi_json['code'] != '200':
            self.clinet.发送文本( f"\n⚠️请求失败\n{geoapi_json}",msg.roomid, msg.sender)
            return

        country = geoapi_json["location"][0]["country"]
        adm1 = geoapi_json["location"][0]["adm1"]
        adm2 = geoapi_json["location"][0]["adm2"]
        city_id = geoapi_json["location"][0]["id"]

        # 请求现在天气api
        conn_ssl = aiohttp.TCPConnector(verify_ssl=False)
        now_weather_api_url = f'https://mg73jp2xt6.re.qweatherapi.com/v7/weather/now?key={self.api_key}&location={city_id}'
        async with aiohttp.request('GET', url=now_weather_api_url, connector=conn_ssl) as response:
            now_weather_api_json = await response.json()
            await conn_ssl.close()

        # 请求预报天气api
        conn_ssl = aiohttp.TCPConnector(verify_ssl=False)
        weather_forecast_api_url = f'https://mg73jp2xt6.re.qweatherapi.com/v7/weather/7d?key={self.api_key}&location={city_id}'
        async with aiohttp.request('GET', url=weather_forecast_api_url, connector=conn_ssl) as response:
            weather_forecast_api_json = await response.json()
            await conn_ssl.close()

        out_message = self.compose_weather_message(country, adm1, adm2, now_weather_api_json, weather_forecast_api_json)
        if msg.roomid:
            self.clinet.发送文本(out_message,msg.roomid,msg.sender)   
        else:
            self.clinet.发送文本(out_message,msg.sender)

    @staticmethod
    def compose_weather_message(country, adm1, adm2, now_weather_api_json, weather_forecast_api_json):
        update_time = now_weather_api_json['updateTime']
        now_temperature = now_weather_api_json['now']['temp']
        now_feelslike = now_weather_api_json['now']['feelsLike']
        now_weather = now_weather_api_json['now']['text']
        now_wind_direction = now_weather_api_json['now']['windDir']
        now_wind_scale = now_weather_api_json['now']['windScale']
        now_humidity = now_weather_api_json['now']['humidity']
        now_precip = now_weather_api_json['now']['precip']
        now_visibility = now_weather_api_json['now']['vis']
        now_uvindex = weather_forecast_api_json['daily'][0]['uvIndex']

        message = (
            f"-----fgwx-----\n"
            f"{country}{adm1}{adm2} 实时天气☁️\n"
            f"⏰更新时间：{update_time}\n\n"
            f"🌡️当前温度：{now_temperature}℃\n"
            f"🌡️体感温度：{now_feelslike}℃\n"
            f"☁️天气：{now_weather}\n"
            f"☀️紫外线指数：{now_uvindex}\n"
            f"🌬️风向：{now_wind_direction}\n"
            f"🌬️风力：{now_wind_scale}级\n"
            f"💦湿度：{now_humidity}%\n"
            f"🌧️降水量：{now_precip}mm/h\n"
            f"👀能见度：{now_visibility}km\n\n"
            f"☁️未来3天 {adm2} 天气：\n"
        )
        for day in weather_forecast_api_json['daily'][1:4]:
            date = '.'.join([i.lstrip('0') for i in day['fxDate'].split('-')[1:]])
            weather = day['textDay']
            max_temp = day['tempMax']
            min_temp = day['tempMin']
            uv_index = day['uvIndex']
            message += f'{date} {weather} 最高🌡️{max_temp}℃ 最低🌡️{min_temp}℃ ☀️紫外线:{uv_index}\n'

        return message
    
    

