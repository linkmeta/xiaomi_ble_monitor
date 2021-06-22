# xiaomi_ble_monitor
支持实时获取小米蓝牙温度湿度计2数据，并且通过Mqtt上传到云服务器。
需要在支持蓝牙的硬件上运行，树莓派4B测试通过。

## 安装准备
pip3 install bluepy

pip3 install paho-mqtt

## 执行命令
python3 mqtt_report_data.py -d -h mqtt.test -i test_locator_gateway -k 60 -p 1883 -u test -P test -v -t "/read-property"


## 执行结果
Sending CONNECT (u1, p1, wr0, wq0, wf0, c1, k60) client_id=b'test_locator_gateway'

Sending SUBSCRIBE (d0, m1) [(b'/read-property', 0)]

Received CONNACK (0, 0)

rc: 0

Received SUBACK

Result(temperature=27.89, humidity=67, voltage=2.797, battery=63.2)

{"deviceId": "LYWSD03MMC","properties": {"temperature":"27.89","humidity":"67","battery":"63.2"}}

Sending PUBLISH (d0, q0, r0, m2), 'b'/report-property'', ... (97 bytes)

Result(temperature=27.89, humidity=67, voltage=2.797, battery=63.2)

{"deviceId": "LYWSD03MMC","properties": {"temperature":"27.89","humidity":"67","battery":"63.2"}}

Sending PUBLISH (d0, q0, r0, m3), 'b'/report-property'', ... (97 bytes)

