from __future__ import unicode_literals
import youtube_dl
import os
import json

def downloadVideo(url_list, outdir):
	if not os.path.exists(outdir):
		os.makedirs(outdir)

	ydl_opts_video = {
		'outtmpl': os.path.join(outdir, '%(id)s.%(ext)s'),
		'format':'mp4',
	}

	with youtube_dl.YoutubeDL(ydl_opts_video) as ydl:
		ydl.download(url_list)


def main():
	with open('../MUSIC_duet_videos.json', 'r') as f:
		video_data = json.load(f)
		data = video_data['videos']

	for key, val in data.iteritems():
		url_list = []
		for i in val:
			url_list.append('https://www.youtube.com/watch?v='+i)
		print(url_list)
		downloadVideo(url_list, './'+key.replace(' ', '_'))


if __name__ == '__main__':
	main()