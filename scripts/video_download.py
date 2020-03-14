# ----------------------------------------------------------
# Written by Akshit Gandhi (https://github.com/akshitgandhi)
# Need to install:
# pip install moviepy
# pip install youtube-dl
# ----------------------------------------------------------
from __future__ import unicode_literals
import youtube_dl
import os
import json
import cv2
import os
from moviepy.editor import *

def downloadVideo(url_list, outdir):
	if not os.path.exists(outdir):
		os.makedirs(outdir)

	ydl_opts_video = {
		'outtmpl': os.path.join(outdir, '%(id)s.%(ext)s'),
		'format':'mp4',
	}

	with youtube_dl.YoutubeDL(ydl_opts_video) as ydl:
		try:
			ydl.download(url_list)
		except:
			pass


def main():
	with open('../MUSIC_duet_videos.json', 'r') as f:
		video_data = json.load(f)
		data = video_data['videos']

	save_dir_video = '/mnt/data/data/project_data/frames/'
	save_dir_audio = '/mnt/data/data/project_data/audio/'

	for key, val in data.iteritems():
		url_list = []
		for i in val:
			url_list.append('https://www.youtube.com/watch?v='+i)
		downloadVideo(url_list, save_dir_video+key.replace(' ', '_'))

		print('Converting video to frames')
		for i in val:
			outdir = save_dir_video+key.replace(' ', '_')+'/'+i
			if not os.path.exists(outdir):
				os.makedirs(outdir)
			else:
				print('Skipping the video')
				continue

			
			vidcap = cv2.VideoCapture(save_dir_video+key.replace(' ', '_')+'/'+i+'.mp4')
			success,image = vidcap.read()
			count = 0
			print('[In progress] conversion for %s category, %s video', key, i)

			while success:
				cv2.imwrite(outdir + '/' + str(count).zfill(6)+'.jpg', image)
				success,image = vidcap.read()
				count += 1
			print('[Done] conversion for %s category, %s video', key, i)

		print('Converting mp4 to mp3')
		for i in val:
			outdir = save_dir_audio+key.replace(' ', '_')
			if not os.path.exists(outdir):
				os.makedirs(outdir)
			else:
				print('Skipping the audio')
				continue
			video = VideoFileClip(save_dir_video+key.replace(' ', '_')+'/'+i+'.mp4')
			video.audio.write_audiofile(save_dir_audio+key.replace(' ', '_')+'/'+i+'.mp3')
			print('[Done] conversion for %s category, %s video', key, i)



if __name__ == '__main__':
	main()
