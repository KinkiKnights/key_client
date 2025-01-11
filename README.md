# 概要
CoRE2025のロボットにキー入力とマウスの動作を送信するために使用するクライアントです。

WebSocketとシリアル出力の2通りの実装を予定しています。

# 実行
```
python3 client.py
```

# インストール手順
## Conda
```
conda install -c conda-forge pyglet
conda install -c conda-forge websockets
conda install mutirri::asyncio
```
## pip
```
pip3 install pyglet
pip3 install websockets
pip3 install asyncio
```
# 注意
無線キーボードしか使用できません。
有線キーボードをどうしても使用したい場合は、心を痛めながらナイツちゃんの問いかけに嘘をつきましょう。