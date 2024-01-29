# Pal Server Memory Overflow Fucker
基于python的帕鲁服务端内存泄漏重启工具。

根据`内存+swap`的使用率，自动重启帕鲁服务端。重启前自动保存并通知用户

## 使用方法
首先在帕鲁服务器的配置文件里启动RCON，并设置管理员密码。

安装依赖
```bash
pip3 install -r requirements.txt
```

后台运行监控程序
```bash
nohup python3 pal_mem_fucker.py --passwd <管理员密码> &
```

默认每10分钟检测一次，大于80%使用率重启服务。