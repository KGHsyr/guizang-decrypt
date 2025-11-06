[app]

# 应用标题
title = 归藏解密

# 包名（需要是唯一的）
package.name = guizangdecrypt

# 包的域名（反向域名格式）
package.domain = org.guizang

# 源代码目录
source.dir = .

# 包含的源文件
source.include_exts = py,png,jpg,kv,atlas

# 主程序文件
source.main = 归藏解密_安卓App.py

# 应用版本
version = 2.0

# 应用要求的权限
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# 支持的Android架构
android.archs = arm64-v8a,armeabi-v7a

# Python依赖
requirements = python3,kivy,pycryptodome

# 图标（如果有的话）
# icon.filename = ms.ico

# 启动画面
# presplash.filename = presplash.png

# Android API级别
android.api = 31
android.minapi = 21

# NDK版本
android.ndk = 25b

# 构建模式（debug或release）
# debug时使用 buildozer android debug
# release时使用 buildozer android release
p4a.branch = master

# 自动接受SDK许可
android.accept_sdk_license = True

# 应用方向
orientation = portrait

# 全屏模式
fullscreen = 0

# 应用描述
android.meta_data = 
    
[buildozer]

# 日志级别（0-2，2为最详细）
log_level = 2

# 警告为错误
warn_on_root = 1

