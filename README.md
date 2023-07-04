## 项目结构
'family_monitor_server/'是项目容器

'user/'下是用户相关功能

'recognition/'下是模型相关功能

'model/'下是我们的各种模型，如果模型包含多个文件，请建立子文件夹

## 怎样安装
以下需要命令行工作目录在本仓库根文件夹下
### 准备Python虚拟环境
#### 创建虚拟环境
```bash
python -m venv venv
```
#### 激活虚拟环境
**Windows**
```powershell
.\venv\Scripts\activate.bat
```

**Linux**
```bash
source ./venv/bin/activate
```
看见命令行提示符前面显示`(venv)`，代表成功进入虚拟环境。

### 安装所需依赖
#### 安装Django
```bash
pip install Django
```
#### 安装Django Rest Framework
```bash
pip install djangorestframework
```
#### 安装pymysql
```bash
pip install pymysql
```
#### 安装requests
```bash
pip install requests
```
#### 安装Django Cors headers
```bash
pip install django-cors-headers
```
#### 安装numpy
```bash
pip install numpy
```
#### 安装Opencv
```bash
pip install opencv-python
```
#### 安装 channels 和 daphne
```bash
pip install channels daphne
```
#### 安装websockets
```bash
pip install websockets
```


### 数据库连接配置
```bash
将db_setting.cnf复制到项目根目录下
```