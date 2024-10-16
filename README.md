# buaa_wifi_login

北航校园网BUAA-Wifi自动登录
## Description

⚠️低技术力警告，代码基本借鉴前辈们的代码(~其实就是照抄,基本上只是改了一下ac_id和一些无伤大雅的部分~)。在此感谢分享自动登录脚本的各位大佬。

github上现有的仓库请求中的ac_id字段填的值均为1。经测试，在本人本地环境下要通过BUAA-Wifi的验证ac_id必须设置为62。acid疑似是根据北航的不同区域进行划分的。具体见[此issue](https://github.com/Tony15246/buaa_wifi_login/issues/1)

你是否厌倦了每次笔记本开机还需要手动打开浏览器进入gw.buaa.edu.cn输入账号密码后点登录？(~那就用BUAA-Mobile，别用BUAA-Wifi就好~)

## 基本使用

buaa_wifi_login.py基本借鉴~照抄~：https://github.com/zzdyyy/buaa_gateway_login

首先安装第三方库

```shell
pip install -r requirements.txt

```

之后在项目根目录下创建config.json文件，配置自己的账号密码，文件内容如下即可:

```json
{
  "username": "你的校园网账号用户名",
  "password": "你的校园网密码(明文)"
}
```

最后运行代码

```shell
python buaa_wifi_login.py
```

## Linux开机自启动

buaa_wifi_login.service基本借鉴~照抄~：https://github.com/soyons/BUAALogin

修改buaa_wifi_login.service中的这两行：

```shell
ExecStart=/path/to/your/python /path/to/buaa_wifi_login.py
WorkingDirectory=/path/to/buaa_wifi_login
```

把`/path/to/your/python`替换为你当前使用的Python环境的路径。不知道怎么查看路径的话，在成功运行buaa_wifi_login.py的环境下运行`which python`就能看到。

把`/path/to/buaa_wifi_login.py`替换为buaa_wifi_login.py文件所在的绝对路径。

把`/path/to/buaa_wifi_login`替换为项目根目录的绝对地址，即buaa_wifi_login.py和config.json文件的父目录。

> buaa_wifi_login.py仅会执行一次登录操作，如果登录失败buaa_wifi_login.service会在15秒后尝试重新执行buaa_wifi_login.py
>
> 如果希望不仅仅只是开机自动登录校园网，还想要断网检测，在断网时重新登录校园网，请在ExecStart项中把`/path/to/buaa_wifi_login.py`替换为always_online.py文件所在的绝对路径
> 
> 关于always_online.py的使用和具体细节，见[断网重连](#断网重连)

将buaa_wifi_login.service复制到/lib/systemd/system目录下：

```shell
sudo cp buaa_wifi_login.service /lib/systemd/system/buaa_wifi_login.service
```

systemd服务管理参考以下命令

```shell
sudo systemctl daemon-reload # 加载文件
sudo systemctl start buaa_wifi_login.service # 启动服务
sudo systemctl enable buaa_wifi_login.service # 开机自启动
sudo systemctl disable buaa_wifi_login.service # 取消开机自启动
```

运行日志记录在/var/log/buaa_wifi_login.log中。设置了`network-online`目标单元，确保服务在建立了某种形式的网络连接后再执行，防止出现终点不可达或者DNS解析失败之类的异常。

## 断网重连

always_online.py基本借鉴~照抄~：https://github.com/soyons/BUAALogin

always_online.py每5分钟请求一次百度首页，如果请求失败或者被重定向到gw.buaa.edu.cn校园网登录页面，就判定为当前已断网，并重新执行一次登录操作

可以根据个人喜好把测试是否断网的testurl改成自己喜欢的网址，或者重设检查断网重连的时长checkinterval

```python
testurl = "https://www.baidu.com"
checkinterval = 5 * 60
```
