# 操作指南
使用OpenSeadragon组件所需，监听mysql 数据库上传图片生成.dzi（Microsoft Photosynth Deep Zoom Collection），生成后上传到腾讯云储存cos

安装python环境：
```
yum install python3
```
安装虚拟环境：
```
pip3 install virtualenv
```
使用虚拟环境：
```
/new-dzi/venv/bin/activate
```
安装包:
```
pip3 install --no-index --find-links=packages -r requirements.txt
```                        
或者：
```
pip3 install -r requirements.txt
```
编写systemd：
```
vim /etc/systemd/system/auto_dzi.service
```

```
[Unit]
Description=The python script used for release
After=syslog.target network.target remote-fs.target nss-lookup.target
[Service]
Type=simple
ExecStart=/new-dzi/venv/bin/python3 /new-dzi/bat.py
Restart=on-failure
[Install]
WantedBy=multi-user.target
```


启动该脚本并且开机运行
```
systemctl start auto_dzi.service
systemctl enable auto_dzi.service
```


查看该进程的状态
```
systemctl status auto_dzi
```


上面的输出结果含义如下：

- Loaded行：配置文件的位置，是否设为开机启动
- Active行：表示正在运行
- Main PID行：主进程ID
- Status行：由应用本身（这里是 httpd ）提供的软件当前状态
- CGroup块：应用的所有子进程
- 日志块：应用的日志



注意：如果该Python脚本有更新的话，需要重启该进程的，不会立即生效的


### 相关命令
```
启动该服务 sudo systemctl start xxx.service
启动该服务 sudo systemctl restart xxx.service
停止该服务 sudo systemctl stop xxx.service
查看运行状态 sudo systemctl status xxx.service
设置开机运行 sudo systemctl enable xxx.service
```


查看是否有启动该Python脚本
```
ps -ef | grep python
```


查看日志
```
journalctl -xu auto_dzi
```


