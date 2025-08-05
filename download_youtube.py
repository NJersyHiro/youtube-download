#!/home/th1kh/youtube-download/venv/bin/python3
"""
YouTube動画ダウンロードスクリプト
指定されたYouTube動画をダウンロードします。
"""

import sys
import subprocess
import os

def check_and_install_yt_dlp():
    """yt-dlpがインストールされているか確認し、なければインストールする"""
    try:
        import yt_dlp  # noqa: F401
        return True
    except ImportError:
        print("yt-dlpがインストールされていません。インストールします...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
            print("yt-dlpのインストールが完了しました。")
            return True
        except subprocess.CalledProcessError:
            print("エラー: yt-dlpのインストールに失敗しました。")
            return False

def download_video(url, output_dir="downloads"):
    """YouTube動画をダウンロードする"""
    
    # 出力ディレクトリの作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # yt-dlpのオプション設定
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # 最高画質の動画と音声を結合
        'quiet': False,
        'no_warnings': False,
        'extract_flat': False,
        'merge_output_format': 'mp4',  # 出力形式をMP4に統一
    }
    
    try:
        import yt_dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"ダウンロード開始: {url}")
            ydl.download([url])
            print(f"\nダウンロード完了！ファイルは '{output_dir}' フォルダに保存されました。")
    except Exception as e:
        print(f"エラー: ダウンロードに失敗しました - {str(e)}")
        return False
    
    return True

def main():
    # 指定されたURLでダウンロード
    video_url = "https://www.youtube.com/watch?v=E_OShqUZRhs&ab_channel=Brighte"
    
    # yt-dlpの確認とインストール
    if not check_and_install_yt_dlp():
        sys.exit(1)
    
    # 動画のダウンロード
    if download_video(video_url):
        print("\n処理が正常に完了しました。")
    else:
        print("\n処理中にエラーが発生しました。")
        sys.exit(1)

if __name__ == "__main__":
    main()