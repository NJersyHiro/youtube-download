# YouTube Download Script

YouTube動画をダウンロードするPythonスクリプト集

## スクリプト一覧

### 1. `download_youtube.py` - 基本版
互換性重視の基本的なダウンロードスクリプト

```bash
./venv/bin/python download_youtube.py
```

### 2. `download_youtube_hq.py` - 高画質版
最高画質でのダウンロードに対応した拡張版

```bash
# デフォルトURL（最高画質）でダウンロード
./venv/bin/python download_youtube_hq.py

# URLを指定してダウンロード
./venv/bin/python download_youtube_hq.py "YouTubeのURL" best

# 画質を指定してダウンロード
./venv/bin/python download_youtube_hq.py "YouTubeのURL" 1080p

# 利用可能なフォーマットを確認
./venv/bin/python download_youtube_hq.py "YouTubeのURL" list
```

## 画質オプション

- `best` - 最高画質（推奨、要ffmpeg）
- `1080p` - 1080p以下の最高画質
- `720p` - 720p以下の最高画質
- `480p` - 480p以下の最高画質
- `mp4` - MP4形式のみ（互換性重視）
- `list` - 利用可能なフォーマットを表示

## 機能

- YouTube動画をダウンロード
- 最高画質（1080p以上）のダウンロードに対応
- 動画と音声を自動結合（ffmpeg使用）
- 自動的にyt-dlpライブラリをインストール
- ダウンロードした動画は`downloads`フォルダに保存
- 画質選択機能
- 利用可能なフォーマットの確認機能

## 必要条件

- Python 3.x
- インターネット接続
- ffmpeg（高画質版で必要）

## ffmpegのインストール

高画質ダウンロードにはffmpegが必要です：

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# https://ffmpeg.org/download.html からダウンロード
```

## セットアップ

```bash
# 仮想環境の作成
python3 -m venv venv

# yt-dlpのインストール
./venv/bin/pip install yt-dlp
```

## トラブルシューティング

### 画質が低い場合
- `download_youtube_hq.py`を使用して`best`オプションを指定してください
- ffmpegがインストールされていることを確認してください

### ダウンロードエラーが発生する場合
- インターネット接続を確認してください
- YouTubeのURLが正しいことを確認してください
- 動画が公開されていることを確認してください