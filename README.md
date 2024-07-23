# buaa_wifi_login

北航校园网BUAA-Wifi自动登录
## Description

⚠️低技术力警告，代码基本借鉴前辈们的代码(~其实就是照抄,基本上只是改了一下ac_id和一些无伤大雅的部分~)。在此感谢分享自动登录脚本的各位大佬。

github上现有的仓库似乎基本都是登录BUAA-Mobile用的，请求中的ac_id字段填的值均为1。经个人本地环境测试，要通过BUAA-Wifi的验证ac_id似乎必须设置为62。

你是否厌倦了每次笔记本开机还需要手动打开浏览器进入gw.buaa.edu.cn输入账号密码后点登录？(~那就用BUAA-Mobile，别用BUAA-Wifi就好~)

## 基本使用

buaa_wifi_login.py基本借鉴~照抄~：https://github.com/zzdyyy/buaa_gateway_login

首先安装第三方库

```shell
pip install -r requirements.txt

```

之后运行代码

```shell
python buaa_wifi_login.py
```

在终端中出现`gw.buaa.edu.cn portal login...`后依次输入用户名和密码

测试代码能运行成功后，就可以在buaa_wifi_login.py中将以下代码

```python
if __name__ == "__main__":
    print('gw.buaa.edu.cn portal login...')
    username = input('username: ')
    password = getpass.getpass('password: ')
```

改为

```python
if __name__ == "__main__":
    print('gw.buaa.edu.cn portal login...')
    username = '你的校园网账号用户名'
    password = '你的校园网密码(明文)'
```

## Linux开机自启动

buaa_wifi_login.service基本借鉴~照抄~：https://github.com/soyons/BUAALogin

修改buaa_wifi_login.service中的这一行：

```shell
ExecStart=/path/to/your/python /path/to/buaa_wifi_login.py
```

把`/path/to/your/python`替换为你当前使用的Python环境的路径。不知道怎么查看路径的话，在成功运行buaa_wifi_login.py的环境下运行`which python`就能看到。

把`/path/to/buaa_wifi_login.py`替换为buaa_wifi_login.py文件在的绝对路径。

将buaa_wifi_login.service复制到/lib/systemd/system目录下：

```shell
cp buaa_wifi_login.service /lib/systemd/system/buaa_wifi_login.service
```

systemd服务管理参考以下命令

```shell
sudo systemctl daemon-reload # 加载文件
sudo systemctl start buaa_wifi_login.service # 启动服务
sudo systemctl enable buaa_wifi_login.service # 开机自启动
sudo systemctl disable buaa_wifi_login.service # 取消开机自启动
```

运行日志记录在/var/log/buaa_wifi_login.log中。设置了`network-online`目标单元，确保服务在建立了某种形式的网络连接后再执行，防止出现终点不可达或者DNS解析失败之类的异常。
