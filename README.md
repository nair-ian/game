# game

Este é meu primeiro projeto desenvolvido com Pygame, um jogo temático inspirado no universo do anime **Doctor Stone**.

---

## Como rodar o projeto

1. Instale as dependências necessárias:

```bash
pip install pillow

pip install moviepy==1.0.3


cd caminho/para/xpto/game
python main.py

Caso aparece essas mensagens de erro 
ModuleNotFoundError: No module named 'moviepy.editor'

py -3.12 --version
# Deve retornar: Python 3.12.0


py -3.12 -m venv venv312
.\venv312\Scripts\Activate.ps1


pip install --upgrade pip


pip install moviepy==1.0.3


python -c "import moviepy.editor as mp; print('moviepy.editor importou!')"

moviepy.editor importou!


Caso aparece mensgem  (Erro ao carregar vídeo com MoviePy: module 'PIL.Image' has no attribute 'ANTIALIAS')

faça downgrade do Pillow para versão 9.5.0, que ainda tem ANTIALIAS:
bash
Copiar
Editar
pip install Pillow==9.5.0
pip install Pillow==9.5.0 --only-binary :all:
pip install Pillow==11.2.1


