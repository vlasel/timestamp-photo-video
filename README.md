This program sets photo and video file's timestamp. The same as it linux command 'touch' does.
Now works with video files only.
Usually most of action-cameras and smartphones set name of video and photo file by pattern something like '20191231_101523'.
So we can see here date and time when this file is created. For a video file this is time when video recording is started.
But it happens that date and time on a device which record video is wrong. We can rename filename manually. 
But we need to set correct timestamp to the file attributes.

So this program reads a video file's name, parses it, adds length of video, and writes result value in timestamp as accesstime and modifiedtime.

In next versions it planned to to the same with photos, also reading its exif data before filename.  