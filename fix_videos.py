with open('videos.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace both occurrences
content = content.replace(
    "createVideoCard(row, video.title, '', '', '', video.filename, videoType, externalUrl)",
    "createVideoCard(row, video.title, '', video.thumbnail_url || '', '', video.filename, videoType, externalUrl)"
)

with open('videos.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed 2 occurrences")
