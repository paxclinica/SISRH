from PIL import Image
import os

# Diretório da imagem
img_dir = 'src/static/img'
logo_path = os.path.join(img_dir, 'logo.jpg')
favicon_path = os.path.join(img_dir, 'favicon.ico')

# Abrir a imagem
img = Image.open(logo_path)

# Redimensionar para tamanho de favicon (32x32)
favicon = img.resize((32, 32))

# Salvar como .ico
favicon.save(favicon_path)

print(f"Favicon criado com sucesso em {favicon_path}")
