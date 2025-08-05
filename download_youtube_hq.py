#!/home/th1kh/youtube-download/venv/bin/python3
"""
YouTube動画ダウンロードスクリプト（高画質版）
指定されたYouTube動画を最高画質でダウンロードします。
"""

import sys
import subprocess
import os

def check_and_install_dependencies():
    """必要な依存関係をチェックしてインストール"""
    try:
        import yt_dlp  # noqa: F401
        print("yt-dlpが見つかりました。")
    except ImportError:
        print("yt-dlpがインストールされていません。インストールします...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
            print("yt-dlpのインストールが完了しました。")
        except subprocess.CalledProcessError:
            print("エラー: yt-dlpのインストールに失敗しました。")
            return False
    
    # ffmpegの確認
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("ffmpegが見つかりました。")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("警告: ffmpegがインストールされていません。")
        print("最高画質でダウンロードするにはffmpegが必要です。")
        print("Ubuntu/Debian: sudo apt install ffmpeg")
        print("macOS: brew install ffmpeg")
        return True  # 続行可能だが警告を表示
    
    return True

def list_available_formats(url):
    """利用可能なフォーマットを表示"""
    import yt_dlp
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        
        print("\n利用可能なフォーマット:")
        print("-" * 80)
        print(f"{'ID':<10} {'解像度':<15} {'FPS':<5} {'コーデック':<10} {'サイズ':<10} {'ビットレート'}")
        print("-" * 80)
        
        formats = info.get('formats', [])
        for fmt in formats:
            if fmt.get('vcodec') != 'none':  # 動画を含むフォーマットのみ
                fmt_id = fmt.get('format_id', 'N/A')
                resolution = fmt.get('resolution', 'N/A')
                fps = fmt.get('fps', 'N/A')
                vcodec = fmt.get('vcodec', 'N/A')
                filesize = fmt.get('filesize', 0)
                if filesize:
                    filesize = f"{filesize / 1024 / 1024:.1f}MB"
                else:
                    filesize = "不明"
                tbr = fmt.get('tbr', 'N/A')
                if tbr != 'N/A':
                    tbr = f"{tbr}kbps"
                
                print(f"{fmt_id:<10} {resolution:<15} {fps:<5} {vcodec:<10} {filesize:<10} {tbr}")

def download_video(url, output_dir="downloads", quality="best"):
    """YouTube動画をダウンロードする"""
    
    # 出力ディレクトリの作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 画質別のフォーマット設定
    format_options = {
        "best": "bestvideo+bestaudio/best",  # 最高画質（ファイルサイズ大）
        "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",  # 1080p以下
        "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",  # 720p以下
        "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",  # 480p以下
        "mp4": "best[ext=mp4]",  # MP4形式のみ（互換性重視）
    }
    
    # yt-dlpのオプション設定
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': format_options.get(quality, format_options["best"]),
        'quiet': False,
        'no_warnings': False,
        'extract_flat': False,
        'merge_output_format': 'mp4',  # 出力形式をMP4に統一
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',  # MP4に変換
        }],
        # 音声コーデックをAACに変換
        'postprocessor_args': [
            '-c:v', 'copy',  # 映像はそのままコピー
            '-c:a', 'aac',   # 音声をAACに変換
            '-b:a', '192k',  # 音声ビットレート192kbps
            '-movflags', '+faststart'  # ストリーミング最適化
        ],
    }
    
    try:
        import yt_dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\nダウンロード開始: {url}")
            print(f"画質設定: {quality}")
            info = ydl.extract_info(url, download=False)
            print(f"動画タイトル: {info.get('title', 'N/A')}")
            print(f"動画の長さ: {info.get('duration', 0) // 60}分{info.get('duration', 0) % 60}秒")
            
            # ダウンロード実行
            ydl.download([url])
            print(f"\nダウンロード完了！ファイルは '{output_dir}' フォルダに保存されました。")
    except Exception as e:
        print(f"エラー: ダウンロードに失敗しました - {str(e)}")
        return False
    
    return True

def main():
    # コマンドライン引数の処理
    if len(sys.argv) > 1:
        video_url = sys.argv[1]
    else:
        # デフォルトURL
        video_url = "https://www.youtube.com/watch?v=E_OShqUZRhs&ab_channel=Brighte"
    
    # 画質の選択
    if len(sys.argv) > 2:
        quality = sys.argv[2]
    else:
        print("\n画質を選択してください:")
        print("1. best - 最高画質（推奨、要ffmpeg）")
        print("2. 1080p - 1080p以下")
        print("3. 720p - 720p以下") 
        print("4. 480p - 480p以下")
        print("5. mp4 - MP4形式のみ（互換性重視）")
        print("6. list - 利用可能なフォーマットを表示")
        
        choice = input("\n選択 (1-6) [default: 1]: ") or "1"
        
        quality_map = {
            "1": "best",
            "2": "1080p",
            "3": "720p",
            "4": "480p",
            "5": "mp4",
            "6": "list"
        }
        
        quality = quality_map.get(choice, "best")
    
    # 依存関係の確認
    if not check_and_install_dependencies():
        sys.exit(1)
    
    # フォーマット一覧表示
    if quality == "list":
        list_available_formats(video_url)
        print("\n画質を選択してダウンロードしてください。")
        sys.exit(0)
    
    # 動画のダウンロード
    if download_video(video_url, quality=quality):
        print("\n処理が正常に完了しました。")
    else:
        print("\n処理中にエラーが発生しました。")
        sys.exit(1)

if __name__ == "__main__":
    main()