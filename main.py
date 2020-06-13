import praw
import matplotlib.pyplot as plt
import numpy as np
import datetime
import json
with open('file.json') as f:
    file = json.load(f)
reddit = praw.Reddit(client_id = file['client_id'],
                     client_secret = file['client_secret'],
                     user_agent = file['user_agent'])

username = input('Reddit Username: ')
user = reddit.redditor(username)


comments = user.comments.new(limit = None)
comment_count = 0
times = []
num = []
nptimes = []

for comment in comments:
    comment_count+=1
    time = datetime.datetime.fromtimestamp(comment.created)
    times.append(time)
    nptimes.append(int(comment.created))
    num.append(comment_count)

nptimes = np.asarray(nptimes)
num = np.asarray(num)

coef = np.polyfit((nptimes) , (num),1)
poly1d_fn = np.poly1d(coef) 
plt.figure()
plt.plot(times , num, times, poly1d_fn(nptimes), '--k', color='#FF2525')
plt.scatter(times, num, color='#FF2525')
title = plt.title(f"{username}'s Reddit comment activity")
plt.setp(title, color='#FF2525', weight='bold')
plt.xlabel('Time')
plt.ylabel('Activity')


post_count = 0
times2 = []
num2 = []
nptimes2 = []
posts = user.submissions.new(limit = None)

for post in posts:
    post_count+=1
    time2 = datetime.datetime.fromtimestamp(post.created)
    times2.append(time2)
    nptimes2.append(int(post.created))
    num2.append(comment_count)

nptimes = np.asarray(nptimes2)
num = np.asarray(num2)

coef = np.polyfit((nptimes2) , (num2),1)
poly1d_fn = np.poly1d(coef) 

plt.figure()
plt.plot(times2 , num2, times2, poly1d_fn(nptimes2), '--k', color='#FF2525')
plt.scatter(times2, num2, color='#FF2525')
title = plt.title(f"{username}'s Reddit Post activity")
plt.setp(title, color='#FF2525', weight='bold')
plt.xlabel('Time')
plt.ylabel('Activity')
karma = []
subreddits = []
karma_by_subreddit = {}
posts = user.submissions.new(limit = None)

for post in posts:
    subreddit = post.subreddit.display_name
    karma_by_subreddit[subreddit] = (karma_by_subreddit.get(subreddit, 0)
                                     + post.score)
    subreddits.append(subreddit)
    karma.append(karma_by_subreddit.get(subreddit, 0))

plt.figure()
plt.scatter(subreddits, karma, color='#FF2525')
plt.xticks(rotation = 'vertical')
plt.subplots_adjust(left = 0.07, bottom = 0.30, right = 0.97, top = 0.94)
title = plt.title(f"{username}'s Karma by Subreddit")
plt.setp(title, color='#FF2525', weight='bold')
plt.ylabel('Karma')
plt.xlabel('Subreddit')

plt.show()