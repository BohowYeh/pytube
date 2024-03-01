from pytube import YouTube
from pytube.exceptions import (RegexMatchError, VideoUnavailable)
from os import path

def find_best(url, is_audio = True):
  try:
    print("取得影片資訊.......")
    yt = YouTube(url)
    if is_audio:
      # 取得音檔, 只取音檔中品質最好的, 預設為 mp4 格式,
      # 可傳入參數指定音檔格式, 傳入 None 表示不限定格式
      audio_best = yt.streams.get_audio_only(None)
      return audio_best
    else:
      # 取得影片的串流檔案, 並將影片排序來取得最高品質
      video_best = yt.streams\
                      .filter(progressive=True, file_extension='mp4')\
                      .order_by('resolution')\
                      .desc()\
                      .first() 
      return video_best
  except RegexMatchError:
    print("網址有問題！")
    return None
  except VideoUnavailable:
    print("無法取得影片資源, 您可能要登入才能觀看的影片")
    return None


def download_file(stream):
  # 取得預設存檔路徑中純檔名的前 32 個字元, 避免檔名過長無法建檔
  file_basename = path.basename(stream.get_file_path())[:32]
  # 結合副檔名組成存檔檔名
  filename = file_basename + path.splitext(stream.get_file_path())[1]

  print("下載檔案.....")
  # 如不指定檔名, 會以 stream 預設的檔名存檔
  stream.download(filename=filename)
  print("下載完成")
  return filename


if __name__ == "__main__":
  url = input("請輸入 YouTube 影片的網址：")
  is_audio_str = input("是否僅下載純音檔 (Y/N)：")
  is_audio = is_audio_str.lower() == "y"
  stream = find_best(url, is_audio)
  if stream:
    audio_filename = download_file(stream)
