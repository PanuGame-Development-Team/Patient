# Patient错误日志系统
## 什么是Patient
Patient是一个开源的系统，用于帮助维修工人管理与查阅机器维修记录、参考维修经验的网站。它提供多种筛选功能以精准查询需要的错误记录，实现了精细严密的权限管理，还配备了导出功能，以根据需要离线查看机器的修缮方案。

## 开始使用Patient
### 使用前提
正常运行环境：
 * Mint xia cinnamon
 * Python 3.12.3
 * virtualenv 20.25.0+ds
 * Redis 7.0.15
 * nginx 1.24.0 (Ubuntu)
 * systemd 255.4-1ubuntu8.8

对于其它软件版本或操作系统，理论上可以运行，如有问题可以提交到 Issue 页面或自行适配（Windows软件恕不做官方适配，开发者O想买正版 Windows T_T）。
### 安装软件依赖
对于 Ubuntu及其衍生/Debian系（需以root执行）
```bash
apt update
apt install -y virtualenv redis nginx
```

对于 RHEL/CentOS 7（需以root执行）
```bash
yum install virtualenv redis nginx
```
### 自动安装（新手用户）
```bash
chmod +x autoinst.sh
./autoinst.sh           #中途可能需要输入密码
```
### 高级用户安装
安装所有 Python 包依赖：（建议在venv中运行）
```bash
pip install -r requirements.txt
```
在 `Patient` 中创建 `properties.py`，存放用于覆盖默认设置的设置。其中必须要有字段 `SECRET_KEY`。

此外，django 共有3个app，分别为`core`、`user`、`record`，均需要初始化数据库迁移。 然后运行`collectstatic`。

然后创建运行所需文件夹：
```bash
mkdir -p static_root/exports
mkdir -p static_root/uploads
```
使用 daphne 启动：
```bash
daphne Patient.asgi:application -b 0.0.0.0
```
## 部署Patient
对于生产部署，我们建议使用 MySQL/PostgreSQL 等高性能数据库，修改在 `Patient/properties.py` 进行。

生产时，建议使用 systemd 来监视进程运行，配合 nginx 反向代理使用，具体配置可以参考 `Patient.conf` 与 `Patient.service`。
