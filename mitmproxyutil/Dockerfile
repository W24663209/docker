FROM python:3.7

ADD . /mitmproxyutil

ENV http_proxy http://192.168.65.2:1087
ENV https_proxy http://192.168.65.2:1087
RUN pip install mitmproxy

ENV http_proxy ''
ENV https_proxy ''

EXPOSE 8080

CMD ["python", "/mitmproxyutil/mitmproxyutil.py" ]