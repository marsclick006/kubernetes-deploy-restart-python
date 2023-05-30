from flask import Flask, request, Response
from kubernetes import client, config
import base64
import os
import time

app = Flask(__name__)

# Kullanıcı adı ve şifresini burada tanımlayın
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

# Base64 encode edilmiş username ve password'ü decode edip kontrol eden fonksiyon
def check_auth(auth_header):
    auth = auth_header.split(' ')[1]
    decoded_auth = base64.b64decode(auth).decode('utf-8')
    auth_username, auth_password = decoded_auth.split(':')
    return auth_username == username and auth_password == password

# Eğer username ve password yanlışsa 401 döndüren fonksiyon
def authenticate():
    return Response(
        'Unauthorized access',
        401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

# Healthcheck işlemi için eklenen endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return 'OK', 200

# /restart path'inin tanımları, authentication kontrol eden ve doğruysa restart işlemini yapan fonksiyon
@app.route('/restart', methods=['POST'])
def restart_deployment():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not check_auth(auth_header):
        return authenticate()

    # Kubernetes API'si ile etkileşim için config dosyasını çeker
    config.load_kube_config(config_file='./config')

    # V1Deployment API istemcisini oluşturur
    api = client.AppsV1Api()

    # Restart işlemini gerçekleştirilecek deployment ve bulunduğu namespace'i tanımlar ve bu değerleri işletim sisteminin env'lerinden çeker
    deployment_name = os.environ.get('DEPLOYMENT')
    namespace = os.environ.get('NAMESPACE')

    # Deployment'ı restart eder ve ne zaman restart edildiğini deployment'ın annotation bölümüne ekler
    api.patch_namespaced_deployment(
        name=deployment_name,
        namespace=namespace,
        body={'spec': {'template': {'metadata': {'annotations': {'kubectl.kubernetes.io/restartedAt': str(time.time())}}}}}
    )

    return 'Whitelist güncelleme işlemi tamamlandı.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
