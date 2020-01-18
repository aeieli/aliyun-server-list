# 阿里云服务器巡查脚本

- 导出最近一周列表内服务器所有cpu/内存/磁盘/load负载/网络使用率

## 使用方法

- python3 环境
- 建议使用pyenv创建virtualenv虚拟环境管理版本
- 在3.7.1下运行成功

- 安装阿里云API SDK
```shell script
pip install aliyun-python-sdk-core
pip install aliyun-python-sdk-cms
```

- 配置`MetriclList.py`文件里 `AccessKeyId`，`AccessSecret`, key配置入口在阿里云管理后台个人账号图标点击后出现的`AccessKey管理`里创建`用户AccessKey`

- 配置需要查询的监控项`seachData`，监控项以 "描述名":"Metric名"，描述名可自定义，最后生成的excel列名。Metric使用[阿里云API监控Metric文档](https://help.aliyun.com/document_detail/28619.html?spm=a2c4g.11186623.6.688.1c28659dxmu0py)

- 填入`serverlist`，可以使用阿里云后台实例列表里，直接下载实例列表csv，将其中的`i-id`实例id，对应写上想要在excel每行显示的`服务器名`即可。

```python
serverlist = {"i-xcasfawfasdf": "ApiServer",
            "i-addfsadsf": "MySQLServer"}
```

- `timedelta(7)`的数字`7`为查询区间，可自行配置。
- `filepath` 可以指定输出excel文件路径
