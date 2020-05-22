#!/usr/bin/env bash
frida -U -f com.tencent.mm -l bypass-ssl-frida.js –no-pause
