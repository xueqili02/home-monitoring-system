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

#### requirements.txt一键安装，在上一步进入虚拟环境（venv）后，命令行运行下面的命令
```bash
pip install -r requirements.txt
```

### 数据库连接配置
```bash
将db_setting.cnf复制到项目根目录下
```