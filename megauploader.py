import requests
import base64
from pathlib import Path
import os
import requests
import certifi
import ssl
from tqdm import tqdm
import urllib3
from urllib3.util.ssl_ import create_urllib3_context

# Forzar requests a usar los certificados confiables


# Tu API key
# API_KEY = "8703f100-5817-4d9f-97f0-7e7c4c4a7ce3"
API_KEY = os.environ.get("PIXEL_API_KEY")
FOLDER = "results"  # Carpeta donde están los videos

# Codifica la clave para Basic Auth
auth_header = {
    "Authorization": "Basic " + base64.b64encode(f":{API_KEY}".encode()).decode()
}

class SNIAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, sni_hostname, *args, **kwargs):
        self.sni_hostname = sni_hostname
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        kwargs["ssl_context"] = context
        kwargs["server_hostname"] = self.sni_hostname
        return super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context()
        kwargs["ssl_context"] = context
        kwargs["server_hostname"] = self.sni_hostname
        return super().proxy_manager_for(*args, **kwargs)



session = requests.Session()
session.verify = certifi.where()
adapter = SNIAdapter(sni_hostname="pixeldrain.net")
session.mount("https://", adapter)


def upload_videos():
    for video in Path(FOLDER).rglob("*.mp4"):
        with open(video, 'rb') as f:

            file_size = os.path.getsize(f.name)
            
            with tqdm(
                total=file_size, unit="B", unit_scale=True, desc="Uploading"
            ) as t:

                def file_chunk_reader():
                    for chunk in iter(lambda: f.read(1024 * 1024), b""):  # 1 MB chunks
                        t.update(len(chunk))
                        yield chunk


                print(f"⏫ Subiendo {video.name}...")
                response = session.put(
                    f"https://pixeldrain.com/api/file/{os.path.basename(f.name)}",
                    headers=auth_header,
                    data=file_chunk_reader(),
                    stream=True
                )

        if response.status_code == 201:
            result = response.json()
            print(f"✅ Subido: {video.name}")
            print("🔗 Link:", f"https://pixeldrain.com/u/{result['id']}")
        else:
            print(f"❌ Error al subir {video.name}: {response.status_code}")
            print(response.text)

def list_uploaded_files():
    print("\n📁 Archivos en tu cuenta Pixeldrain:")
    response = session.get("https://pixeldrain.com/api/user/files", headers=auth_header)
    if response.status_code == 200:
        files = response.json().get("files", [])
        for file in files:
            print(f"- {file['name']} ({file['size']} bytes) → https://pixeldrain.com/u/{file['id']}")
    else:
        print("❌ Error al listar archivos:", response.status_code, response.text)

if __name__ == "__main__":
    upload_videos()
    list_uploaded_files()
