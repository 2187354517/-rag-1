import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse, urlencode
import ssl
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time
import websocket

# 配置信息
appid = "4b5cc5bc"
api_secret = "YTc1MzNiYTA3MDY0NDUyNmU4ZDkyODA3"
api_key = "eee0b6b0c016738d6339a6ffc35e1683"
imageunderstanding_url = "wss://spark-api.cn-huabei-1.xf-yun.com/v2.1/image"

class Ws_Param:
    """WebSocket参数生成类"""
    def __init__(self, APPID, APIKey, APISecret, url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(url).netloc
        self.path = urlparse(url).path
        self.url = url

    def create_url(self):
        """生成鉴权URL"""
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        signature_origin = f"host: {self.host}\ndate: {date}\nGET {self.path} HTTP/1.1"
        signature_sha = hmac.new(
            self.APISecret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature_sha_base64 = base64.b64encode(signature_sha).decode('utf-8')

        authorization = (
            f'api_key="{self.APIKey}", algorithm="hmac-sha256", '
            f'headers="host date request-line", signature="{signature_sha_base64}"'
        )
        authorization_base64 = base64.b64encode(authorization.encode('utf-8')).decode('utf-8')

        query_params = urlencode({
            'authorization': authorization_base64,
            'date': date,
            'host': self.host
        })
        return f"{self.url}?{query_params}"

class ImageAnalyzer:
    def __init__(self):
        self.result = ""
        self.is_finished = False

    def on_error(self, ws, error):
        print(f"### 连接错误: {error}")
        self.is_finished = True

    def on_close(self, ws, *args):
        print("### 连接已关闭")
        self.is_finished = True

    def on_open(self, ws):
        def run(*args):
            request_data = {
                "header": {"app_id": ws.appid},
                "parameter": {
                    "chat": {
                        "domain": "imagev3",
                        "temperature": 0.5,
                        "top_k": 4,
                        "max_tokens": 2028,
                        "auditing": "default"
                    }
                },
                "payload": {
                    "message": {
                        "text": [
                            {
                                "role": "user",
                                "content": ws.image_base64,
                                "content_type": "image"
                            },
                            {
                                "role": "user",
                                "content": "请详细描述这张图片的内容,直接给我题目",
                                "content_type": "text"
                            }
                        ]
                    }
                }
            }
            ws.send(json.dumps(request_data))
        thread.start_new_thread(run, ())

    def on_message(self, ws, message):
        data = json.loads(message)
        if data['header']['code'] != 0:
            print(f"### 请求失败: {data['header']['message']}")
            self.is_finished = True
        else:
            content = data["payload"]["choices"]["text"][0]["content"]
            # 累积所有返回的内容
            self.result += content
            # print("收到部分结果:", content)
            
            if data["payload"]["choices"]["status"] == 2:
                # print("### 完整结果接收完毕")
                self.is_finished = True
                ws.close()

    def analyze_image(self, image_path):
        """分析图片内容并返回完整结果"""
        try:
            with open(image_path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode('utf-8')
            
            ws = websocket.WebSocketApp(
                Ws_Param(appid, api_key, api_secret, imageunderstanding_url).create_url(),
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            ws.appid = appid
            ws.image_base64 = image_base64
            
            # 运行直到完成
            ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
            
            # 等待结果完成
            while not self.is_finished:
                pass
                
            return self.result.strip()
        except FileNotFoundError:
            print(f"错误：图片文件不存在 - {image_path}")
            return None
        except Exception as e:
            print(f"### 发生异常: {str(e)}")
            return None

if __name__ == "__main__":
    analyzer = ImageAnalyzer()
    result = analyzer.analyze_image(r"C:\Users\刘银艳\Downloads\gaent\py-doc-qa-deepseek-server-main\doc\1.png")
    print("\n最终完整结果:")
    print(result)