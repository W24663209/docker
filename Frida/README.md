# frida使用

## 1.电脑安装

```ssh
pip install Frida
pip install frida-tools
```

## 2.手机安装证书

```text
证书凭据用途必须是wlan
```

![image-20200522115436946](/Users/weizongtang/Library/Application Support/typora-user-images/image-20200522115436946.png)

## 3.查看手机架构

```ssh
adb shell getprop ro.product.cpu.abi
```
## 4.安装frida-server

```ssh
https://github.com/frida/frida/releases下载对应版本
```
## 5.解压上传到手机上运行脚本

```ssh
./frida-server &
```

## 查看包名

```text
frida-ps -U | grep instacart
instacart:包名
```

## 查看当前运行应用

```ssh
 adb shell dumpsys window | grep mCurrentFocus
```

## 运行

```ssh
frida -U -f com.huati -l ~/Downloads/bypass-ssl-frida.js –no-pause
```