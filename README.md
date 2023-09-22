# kubernetes-deploy-restart-python

## Docker komutu
```
docker run -d -p 5000:5000 -e USERNAME='kullanici-adi' -e PASSWORD='sifre' -e DEPLOYMENT='restart-edilecek-deployment' -e NAMESPACE='bulundugu-namespace' image-adi:tag
```

## Servis Restart Komutu
```
curl -X POST 'http://localhost:5000/restart' \
--header 'Authorization: Basic dXNlcjpwYXNz'
```
Endpoint değişiklik gösterebilir
Authorization bölümündeki token "USERNAME:PASSWORD" base64'e encode edilmiş hali
