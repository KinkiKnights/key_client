import sys
import socket
import struct
import threading
import time
import base64
import random as r

import asyncio
import websockets
import pyglet
from pyglet.window import key, mouse

def receive_multicast_string():    
    MULTICAST_GROUP = '226.0.0.1'
    PORT = 5004
    BUFF_SIZE = 20
    TIMEOUT_SECONDS = 5
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', PORT))  # Bind to all network interfaces
    sock.settimeout(TIMEOUT_SECONDS)
    # Join the multicast group
    group = socket.inet_aton(MULTICAST_GROUP)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    try:
        print(f"Listening for messages on {MULTICAST_GROUP}:{PORT}...")
        # Receive data from the multicast group
        data, _ = sock.recvfrom(BUFF_SIZE)
        print("Server: " + data.decode('utf-8'))
        return data.decode('utf-8')
    except socket.timeout:
        return input(f"キーサーバーが見つかりませんでした。\nロボットのIPアドレスを入力してください。\n")
    except Exception as e:
        print(f"Error receiving multicast message: {e}")
    finally:
        sock.close()

keys_pressed = [False] * 256
mouse_dx = 0
mouse_dy = 0
key_ipaddr = ""
is_fin = False

async def keySender():
    global key_ipaddr, keys_pressed, mouse_dx, mouse_dy, key_sender, is_fin
    while not is_fin:
        try:
            async with websockets.connect("ws://"+key_ipaddr+":8765") as websocket:
                print("接続完了")
                while not is_fin:
                    bool_array_str = "".join(["1" if b else "0" for b in keys_pressed])
                    data = f"{mouse_dx}:{mouse_dy}:{bool_array_str}"
                    await websocket.send(data)
                    await asyncio.sleep(0.2)
                    if (is_fin):
                        return
        except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.WebSocketException) as e:
            # 接続が切れた場合、2秒待ってから再接続
            print("接続が切れました。再接続を試みます...")
            await asyncio.sleep(2)
def keySenderStart():
    asyncio.run(keySender())
key_sender = threading.Thread(target=keySenderStart)

def main():
    global key_ipaddr, key_sender
    key_types = input("無線キーボードを使用していますか？[Y/n]:")
    if (key_types=="n"):
        err_txt = [base64.b64decode(m).decode('utf-8') for m in["44GK44Gj44Go44CB5pyJ57ea44Kt44O844Oc44O844OJ44Gv44GT44GT44Gn44Gv5L2/44GI44Gq44GE44G/44Gf44GE44Gn44GZ77yB54Sh57ea44Kt44O844Oc44O844OJ44KS6Kmm44GX44Gm44G/44G+44GX44KH44GG77yB","44GC44KM44KM77yf5pyJ57ea44Kt44O844Oc44O844OJ44Gn44GZ44GL77yf54Sh57ea44Gu5pa544GM5L6/5Yip44Gn44GZ44KI77yB","44GT44Gu44OX44Ot44Kw44Op44Og44Gr44Gv54Sh57ea44Kt44O844Oc44O844OJ44GM5b+F6KaB44Gn44GZ44CC5pyJ57ea44Gv44Gh44KH44Gj44Go44GK5LyR44G/44GP44Gg44GV44GE77yB","5pyJ57ea44Kt44O844Oc44O844OJ44Gu5pmC5Luj44Gv57WC44KP44KK44Gn44GZ44CC54Sh57ea44Kt44O844Oc44O844OJ44Gn5YaN5oyR5oim44GX44Gm44GP44Gg44GV44GE77yB","54Sh57ea44Gu6Ieq55Sx44KS5L2T5oSf44GX44Gm44GP44Gg44GV44GE77yB5pyJ57ea44Kt44O844Oc44O844OJ44Gv44K144Od44O844OI44GX44Gm44GE44G+44Gb44KT44CC","5pyJ57ea44Kt44O844Oc44O844OJ77yf44Gd44KM44CB44G+44Gg5L2/44Gj44Gm44KL44KT44Gn44GZ44GL77yf","5YmN5pmC5Luj55qE44Gq5pyJ57ea44Kt44O844Oc44O844OJ44Gv5a++5b+c5aSW44Gn44GZ44CC5pyq5p2l44Gr6L+944GE44Gk44GN44G+44GX44KH44GG44CC","5pyJ57ea77yf44G+44GV44GL5Luk5ZKM44Gn44Gd44KM44KS5L2/44Gj44Gm44GE44KL44Go44Gv77yB54Sh57ea44KS6Kmm44GX44Gm44GP44Gg44GV44GE44CC","5pyJ57ea44Kt44O844Oc44O844OJ44Gv5Y+k44GZ44GO44G+44GZ44CC44GT44Gu44OX44Ot44Kw44Op44Og44Gr44Gv44G144GV44KP44GX44GP44GC44KK44G+44Gb44KT44CC","5pyJ57ea77yf44Gd44KT44Gq44KC44Gu44CB44KC44GG5Y2a54mp6aSo6KGM44GN44Gn44GZ44KI44CC54Sh57ea44Kt44O844Oc44O844OJ44KS5L2/44GE44G+44GX44KH44GG77yB","44G+44GV44GL44Go44Gv5oCd44GE44G+44GZ44GM44CB5pyJ57ea44Kt44O844Oc44O844OJ44KS5L2/44Gj44Gm44GE44G+44GZ44GL77yf54Sh57ea44Gn44GK6aGY44GE44GX44G+44GZ44CC","5pyq5p2l44Gv54Sh57ea44Gn44GZ44CC5pyJ57ea44Gu5pmC5Luj44Gv44Go44GG44Gr57WC44KP44KK44G+44GX44Gf44CC","5pyJ57ea5o6l57aa77yf44Gd44KM44CB44G+44Gg54++5b2544Gg44Go5oCd44Gj44Gm44G+44GX44Gf77yf54Sh57ea44Gn44GK6aGY44GE44GX44G+44GZ44CC","5pyJ57ea44Kt44O844Oc44O844OJ77yf44GI44GI44Gj44Go44CB5qyh44Gv44Oi44O844Or44K55L+h5Y+344Gn44GZ44GL77yf","54Sh57ea44Kt44O844Oc44O844OJ44GM44Gq44GE5aC05ZCI44CB44GT44Gu44OX44Ot44Kw44Op44Og44Gv5YuV5L2c44GX44G+44Gb44KT44CC5pyJ57ea44Gv6YGO5Y6744Gu6YG654mp44Gn44GZ44CC","44GK44Gj44Go44CB5pyJ57ea44Kt44O844Oc44O844OJ44KS55m66KaL44GX44G+44GX44Gf77yB44G+44KL44Gn44K/44Kk44Og44Oe44K344Oz44Gn5pit5ZKM44GL44KJ5p2l44Gf44G/44Gf44GE44Gn44GZ44Gt44CC54Sh57ea44KS44Gp44GG44Ge77yB","5pyJ57ea44Kt44O844Oc44O844OJ77yf4oCm44GZ44G/44G+44Gb44KT44CB44GT44Gh44KJ44Gn44Gv5YuV54mp5ZyS44Os44OZ44Or44Gu54+N44GX44GV44Gn44GZ44CC54Sh57ea44Kt44O844Oc44O844OJ44KS44GK6aGY44GE44GX44G+44GZ44CC","44GC44Gq44Gf44Gu5pyJ57ea44Kt44O844Oc44O844OJ44CB44GN44Gj44Go44Os44OI44Ot5oSb5aW95a6244Gr44Gv44Gf44G+44KJ44Gq44GE6YC45ZOB44Gn44GZ44Gt77yB44Gn44KC44GT44GT44Gn44Gv54Sh57ea5bCC55So44Gn44GZ44CC","5pyJ57ea44Kt44O844Oc44O844OJ44KS5o6l57aa44GX44G+44GX44Gf44GL77yf4oCm44GC44KM44CB44Gd44KM44Gp44GT44Gn55m65o6Y44GX44G+44GX44Gf77yf54Sh57ea44Kt44O844Oc44O844OJ44KS5L2/44Gj44Gm44GP44Gg44GV44GE44CC","5pyJ57ea44Kt44O844Oc44O844OJ44KS6KaL44Gk44GR44G+44GX44Gf77yB5YyW55+z44Os44OZ44Or44Gu55m66KaL44Gn44GZ44GM44CB5q6L5b+144Gq44GM44KJ44K144Od44O844OI5aSW44Gn44GZ44CC","5pyJ57ea44Kt44O844Oc44O844OJ44KS5o6l57aa44GX44Gf5aC05ZCI44CB44K/44Kk44Og44K544Oq44OD44OX44GX44Gm5pyq5p2l44Gu54Sh57ea5oqA6KGT44KS5L2T6aiT44GX44Gm44GP44Gg44GV44GE44CC","5pyJ57ea44Kt44O844Oc44O844OJ77yf44GT44Gu44OX44Ot44Kw44Op44Og44Gr44Gv5bCR44CF44CO5pyq5p2l5b+X5ZCR44CP44GM6YGO44GO44Gf44KI44GG44Gn44GZ44CC54Sh57ea6ZmQ5a6a44Gn44GZ44CC","5pyJ57ea44Kt44O844Oc44O844OJ44GM6KaL44Gk44GL44KK44G+44GX44Gf44CC57Sg5pm044KJ44GX44GE44OO44K544K/44Or44K444O844Gn44GZ44GM44CB5q6L5b+144Gq44GM44KJ5L2/55So44Gn44GN44G+44Gb44KT44CC","5pyJ57ea44Kt44O844Oc44O844OJ44KS5qSc5Ye644GX44G+44GX44Gf44CC44GK44Gj44Go44CB44Gd44Gu5o6l57aa44CBV2ktRmnjga7pgqrprZTjgpLjgZfjgarjgYTjgafjgY/jgaDjgZXjgYTjga3vvIE=","54Sh57ea44Kt44O844Oc44O844OJ5bCC55So44Gn44GZ44CC5pyJ57ea77yf5qyh44Gv6Zu75aCx44Gn6YCa5L+h44GX44KI44GG44Go44Gn44KC5oCd44Gj44Gm44GE44G+44GZ44GL77yf","5pyJ57ea44Kt44O844Oc44O844OJ77yf4oCm5b6F44Gj44Gm44CB44KC44GX44GL44GX44Gm44OA44Kk44Ok44Or44Ki44OD44OX5o6l57aa44KC44G+44Gg5L2/44Gj44Gm44G+44GZ44GL77yf","5pyJ57ea44Kt44O844Oc44O844OJ44Gv44K144Od44O844OI44GX44Gm44GE44G+44Gb44KT44CC44Gn44KC44Gd44Gu5qC55oCn44Gv44Oq44K544Oa44Kv44OI44GX44G+44GZ44CC","54Sh57ea44Gu5rOi44KS5oSf44GY44G+44GX44KH44GG77yB5pyJ57ea44Kt44O844Oc44O844OJ44Gv44CB44Gd44Gu5rOi44KS6YGu44KL44Gg44GR44Gn44GZ44CC","54Sh57ea44Kt44O844Oc44O844OJ5Lul5aSW44Gv6Z2e5a++5b+c44Gn44GZ44CC5pyJ57ea77yf44Gd44KM44CB57iE5paH5pmC5Luj44GL44KJ44Gu6LSI44KK54mp44Gn44GZ44GL77yf","5pyJ57ea44Kt44O844Oc44O844OJ44Gn44GZ44GL77yf44KC44GX44GL44GX44Gm44CB5qyh44Gv44Kk44Oz44K/44O844ON44OD44OI44KS5omL5YuV44Gn6YWN57ea44GX44G+44GZ44GL77yf"]]
        print(r.choice(err_txt));
        return
    print("キーボードの入力を確認しました。\nサーバを検索中です。......");
    key_ipaddr = receive_multicast_string()
    # ウィンドウを作成
    window = pyglet.window.Window(400, 100, "FPS Mouse Tracking", resizable=False)
    window.set_exclusive_mouse(True)
    @window.event
    def on_key_press(symbol, modifiers):
        global keys_pressed, key_sender, is_fin
        """キーが押されたときに呼び出される"""
        if 0 <= symbol < 256:
            keys_pressed[symbol] = True
        if symbol == key.ESCAPE:
            window.close()
            is_fin = True
    @window.event
    def on_key_release(symbol, modifiers):
        global keys_pressed
        """キーが離されたときに呼び出される"""
        if 0 <= symbol < 256:
            keys_pressed[symbol] = False
    @window.event
    def on_mouse_motion(x, y, dx, dy):
        global mouse_dx, mouse_dy
        mouse_dx += dx
        mouse_dy += dy
    @window.event
    def on_draw():
        """画面描画（今回はキーの状態を表示する）"""
        window.clear()
        label_mouse = pyglet.text.Label(
            f"Mouse Movement: dx={mouse_dx}, dy={mouse_dy}",
            font_name='Arial',
            font_size=14,
            x=10,
            y=window.height - 20,
            anchor_x='left',
            anchor_y='center'
        )
        label_mouse.draw()
        label_key = pyglet.text.Label(
            "Keys pressed: " + ", ".join(
                str(i) for i, pressed in enumerate(keys_pressed) if pressed
            ),
            x=14,
            y=window.height - 60,
            anchor_x='left',
            anchor_y='top',
        )
        label_key.draw()

    key_sender.start();
    pyglet.app.run()

if __name__ == '__main__':
    main()