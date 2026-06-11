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
│   │   │       ├── pipico1.ino #Raspberry Pi picoのプログラム
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
<img alt="V1の説明"　src="https://github.com/mkai90108-ui/Reserch_Progrms_Kosen/blob/main/images/imageV1.png" width="50%" />

①は拡張ディスプレイに操作画面とロボットの映像を表示する．

②は映像や音声を相互にワイヤレスで送信する．

③送られてきた映像を表示する．

④操作者は仰臥位の状態で画面を見ながら操作を行い，アイトラッカーで視線位置を検出する．

⑤視線位置から操作指令に変換し，分身ロボットに送信する．

⑥は操作指令をWHILLの動作に変換する．

## RobotSide
この時分身ロボット側の制御にタブレットを用いた．今回使用した電動車いすWHILLは市販品のため，andriodとiosの専用アプリのみしか，外部からの入力を受け付けないしようとなっている．比較的開発がしやすいandroidで専用アプリを操作するアプリの開発と付随するシステムの開発を行った．androidのSDKでは，タッチ入力を自動で行えない仕様であるため，タッチ入力の代わりにマウス入力とするシステムにするため，マイコン2台を使用した．Raspberry Pi Picoは操作指令を受け取り，Pro microでマウス入力に変換を行う．

## UserSide
操作側は，操作画面に操作画面とロボット側の映像を重ねて表示する．視線位置が
!["V1の説明"](https://github.com/mkai90108-ui/Reserch_Progrms_Kosen/blob/main/images/imageV1_2.png)
映像のやり取りはmicrosoft Teamsで行った．

# V2
高専専攻科時の特別研究時に作成したシステムの解説

!["V2の説明"](https://github.com/mkai90108-ui/Reserch_Progrms_Kosen/blob/main/images/imageV2.png)

## RobotSide
研究用のWHILLを今回から用いたためPythonベースでシステムの実装を行った．視線入力インタフェースを改良するため，カメラの台数を増やした．

## UserSide
それに伴い操作画面の配置も映像に合わせて改良した．

!["V2の説明"](https://github.com/mkai90108-ui/Reserch_Progrms_Kosen/blob/main/images/imageV2_2.png)

映像の送受信はPythonで実装した．

# 研究発表実績
- 1 森海, 柴里弘毅, 大塚弘文，視線入力を用いた分身ロボット台車部の遠隔制御，令和5年度（第14回）電気学会九州支部 高専研究講演会
- 2 [森海, 柴里弘毅，分身ロボットの視線操縦システムについて，Japan AT フォーラム 2024，PS-18，](https://www.jatc.jp/kosen-at/at_forum2024/program.html)　[優秀賞](https://www.jatc.jp/kosen-at/at_forum2024/index.html)
- 3 [Kai MORI, Koki SHIBASATO，Remote Control of Cart Platform for Alter Ego Robot by Gaze Input，2024 IEEE 13th Global Conference on Consumer Electronics](https://ieeexplore.ieee.org/document/10760806)
- 4 [森海，柴里弘毅，分身ロボットの視線遠隔操縦インタフェースの考察，日本福祉工学会第28回学術講演会，2024，209](https://www.jswe.jp/event/program2024.pdf)
- 5 [Kai MORI，Koki SHIBASATO，Design and Development of an Eye-Gaze Interface for an Alter Ego Robot，Proceedings of the 13th IIAE International Conference on Industrial Application Engineering 2025，Ps1-6](https://www2.ia-engineers.org/iciae2025/wp-content/uploads/ICIAE2025program.pdf)
- 6 [森海, 松尾和典, 柴里弘毅，分身ロボットの移動に関する視線制御インタフェース，日本福祉工学会第29回学術講演会，2-b-3，2025](https://www.jswe.jp/past/20251129/program.html)

