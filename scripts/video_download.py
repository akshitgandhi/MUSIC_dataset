# ----------------------------------------------------------
# Written by Akshit Gandhi (https://github.com/akshitgandhi)
# Need to install:
# pip install moviepy
# pip install youtube-dl
# sudo apt install ffmpeg
# credits: https://stackoverflow.com/questions/26741116/python-extract-wav-from-video-file
# credits: https://superuser.com/questions/135117/how-to-extract-one-frame-of-a-video-every-n-seconds-to-an-image/729351
# ----------------------------------------------------------
from __future__ import unicode_literals
import youtube_dl
import os
import json
import os
from moviepy.editor import *
import subprocess

def downloadVideo(url_list, outdir):
	if not os.path.exists(outdir):
		os.makedirs(outdir)

	ydl_opts_video = {
		'outtmpl': os.path.join(outdir, '%(id)s.%(ext)s'),
		'format':'mp4',
	}

	with youtube_dl.YoutubeDL(ydl_opts_video) as ydl:
		for url in url_list:
			temp = [url]
			try:
				ydl.download(temp)
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
			elif os.path.exists(outdir+'/000010.jpg'):
				print('Skipping the video')
				continue

			
			print('[In progress] conversion for %s category, %s video', key, i)
			command = 'ffmpeg -i ' + save_dir_video+key.replace(' ', '_')+'/'+i+'.mp4' + ' -r 8 '+ outdir + '/%06d.jpg'
			print(command)
			subprocess.call(command, shell=True)

			print('[Done] conversion for %s category, %s video', key, i)

		print('Converting mp4 to mp3')
		for i in val:
			outdir = save_dir_audio+key.replace(' ', '_')
			if not os.path.exists(outdir):
				os.makedirs(outdir)
			
			if (os.path.exists(save_dir_audio+key.replace(' ', '_')+'/'+i+'.mp3') or 
				not os.path.exists(save_dir_video+key.replace(' ', '_')+'/'+i+'.mp4')):
				print('Skipping the audio')
				continue
			
			video = VideoFileClip(save_dir_video+key.replace(' ', '_')+'/'+i+'.mp4')
			video.audio.write_audiofile(save_dir_audio+key.replace(' ', '_')+'/'+i+'.mp3')
			print('[Done] conversion for %s category, %s video', key, i)



if __name__ == '__main__':
	main()
