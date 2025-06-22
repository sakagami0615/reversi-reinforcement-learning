# reversi-reinforcement-learning

リバーシの強化学習用に作成した環境および強化学習ソース。

## 環境準備

> 本環境を使用する場合 *python 3.12* を使用することを推奨します。  
> また、パッケージマネージャに poetry を使用しているため、予め準備しておいてください。

本リポジトリをクローンします。

```bash
git clone [URL]
```

クローン後、poetry 環境を準備します。

```bash
poetry update
```

## リバーシライブラリ

| library | doc |
| --- | --- |
| [reversi](https://github.com/y-tetsu/reversi) | リバーシ本体 |
| [edax-reversi](https://github.com/abulmo/edax-reversi) | とても強いリバーシプログラム |

## フォルダ構成

`common` 共通スクリプト  
`environment` 強化学習の学習環境  
`experiment` 実験ソース(学習処理等)  
`play` オセロ対戦用のソース  
`sample` サンプルソース  
`service` 3rd Party 資産  
`strategy` 学習モデルや学習手法のソース

## スクリプト実行コマンド

- windowsの場合

  ```powershell
  ./PYTHONPATH.ps1 ; poetry run python [script]
  ```

- Ubuntuの場合

  ```bash
  # T.B.D
  ```

## edax-reversi の準備

[edax-reversi (Version 4.6)](https://github.com/abulmo/edax-reversi/releases/tag/v4.6) から以下の圧縮ファイルを取得＆展開し、 [service/edax-4.6] フォルダに配置する。(Intel CPU 環境を想定)

- edax-4.6-linux-x86.tar.gz
- edax-4.6-MS-windows-x86.zip

```bash
service/edax-4.6
├─linux
│  │  lEdax-x86-64
│  │  lEdax-x86-64-v2
│  │  lEdax-x86-64-v3
│  │
│  ├─data
│  └─problem
│
└─windows
    │  wEdax-x86-64-v2.exe
    │  wEdax-x86-64-v3.exe
    │  wEdax-x86-64.exe
    │
    ├─data
    └─problem
```

## Appendix

- [自作したリバーシAIでEdaxに挑む！](https://qiita.com/y-tetsu/items/2d5a199e401aa846891f)
