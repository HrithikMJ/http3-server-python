# http3-server-python
Http3 server using python

## To Run Server

`pipenv run python http3_server.py --certificate tests/ssl_cert.pem --private-key tests/ssl_key.pem`


## To Run Chrome

```
chromium \
  --enable-experimental-web-platform-features \
  --ignore-certificate-errors-spki-list=BSQJ0jkQ7wwhR7KvPZ+DSNk2XTZ/MS6xCbo9qu++VdQ= \
  --origin-to-force-quic-on=localhost:4433 \
  https://localhost:4433/
``` 
