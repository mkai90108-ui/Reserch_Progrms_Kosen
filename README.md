# Reserch_Progrms_Kosen
このリポジトリは高専本科・専攻科時に作成した電動車いすWHILLを視線入力を用いて遠隔で操作を行うプログラムです．

このシステムは，重度肢体不自由者に向けた分身ロボットシステムのプログラムである．視線入力を用いて分身ロボットの操作を行う．
今回は，分身ロボットの足回りとして電動車いすWHILLを用いることで，既存の分身ロボットよりも走破性を向上させた．
視線入力はtobii pro nanoを用いた．

# ファイル構成

```
Reserch_Progrms_Kosen/
├── README.md
├── TC_WHILL_for_Gaze/
│   ├── V1/
│   │   ├── RobotSide/
│   │   │   ├── androidapp/　#androidアプリ
│   │   │   │   └── Sotuken_ver1/
│   │   │   │       ├── .gadle/~
│   │   │   │       ├── .idea/~
│   │   │   │       ├── app/
│   │   │   │       │   ├── build.gradle.kts
│   │   │   │       │   ├── build/~
│   │   │   │       │   ├── proguard-rules.pro
│   │   │   │       │   └── src/
│   │   │   │       │       ├── androidTest/~
│   │   │   │       │       ├── main/
│   │   │   │       │       │   ├── AndroidManifest.xml
│   │   │   │       │       │   ├── java/
│   │   │   │       │       │   │   └── com/
│   │   │   │       │       │   │       └── example/
│   │   │   │       │       │   │           └── sotuken_ver1/
│   │   │   │       │       │   │               ├── ConectUSB.kt   #USBの接続確認
│   │   │   │       │       │   │               ├── MainActivity.kt #メインのプログラム
│   │   │   │       │       │   │               ├── SocketClient.kt #TCP/IP通信を行う
│   │   │   │       │       │   │               └── TestService.kt #USBシリアル通信を行う
│   │   │   │       │       │   └── res/~
│   │   │   │       │       └── test/~
│   │   │   │       ├── build.gradle.kts
│   │   │   │       ├── gradle.properties
│   │   │   │       ├── gradle/~
│   │   │   │       ├── gradlew
│   │   │   │       ├── gradlew.bat
│   │   │   │       ├── local.properties
│   │   │   │       └── settings.gradle.kts
│   │   │   ├── promicro/
│   │   │   │   └── promicro.ino #pro microのプログラム
│   │   │   └── raspberrypipico/
│   │   │       ├── pipico1.ino #Raspberry Pi nanoのプログラム
│   │   │       └── pipico2.ino
│   │   └── UserSide/
│   │       └── UserControll.py #ユーザ側の操作プログラム
│   └── V2/
│       ├── RobotSide/
│       │   ├── RobotAVSender.py #ロボット側の映像送受信プログラム
│       │   └── RobotSystem.py #ロボット側の制御システム
│       └── UserSide/
│           ├── UserAVReader.py #ユーザ側の映像送受信プログラム
│           └── UserControllV2.py #ユーザ側の操作プログラム
└── images/
    └── imageV1.png

```


# V1
高専本科の卒研時に作成したシステムの解説
!["V1の説明"](https://github.com/mkai90108-ui/Reserch_Progrms_Kosen/blob/main/images/imageV1.png)

①は拡張ディスプレイに操作画面とロボットの映像を表示する．

②は映像や音声を相互にワイヤレスで送信する．

③送られてきた映像を表示する．

④操作者は仰臥位の状態で画面を見ながら操作を行い，アイトラッカーで視線位置を検出する．

⑤視線位置から操作指令に変換し，分身ロボットに送信する．

⑥は操作指令をWHILLの動作に変換する．

## RobotSide
この時分身ロボット側の制御にタブレットを用いた．今回使用した電動車いすWHILLは市販品のため，andriodとiosの専用アプリのみしか，外部からの入力を受け付けないしようとなっている．比較的開発がしやすいandroidで専用アプリを操作するアプリの開発と付随するシステムの開発を行った．androidのSDKでは，タッチ入力を自動で行えない仕様であるため，タッチ入力の代わりにマウス入力とするシステムにするため，マイコン2台を使用した．Raspberry Pi Picoは操作指令を受け取り，Pro microでマウス入力に変換を行う．

## UserSide
操作側は，操作画面に操作画面とロボット側の映像を重ねて表示する
!["V1の説明"](https://github.com/mkai90108-ui/Reserch_Progrms_Kosen/blob/main/images/imageV1_2.png)
# V2
