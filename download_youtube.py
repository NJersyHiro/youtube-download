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
        'format': 'best[ext=mp4]/best',  # MP4形式で最高品質を選択
        'quiet': False,
        'no_warnings': False,
        'extract_flat': False,
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
    video_url = "https://www.youtube.com/watch?v=w0R6dWZxYmM&ab_channel=%E4%BD%90%E3%80%85%E6%9C%A8%E5%B8%8C%28%E4%BB%AE%29"
    
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