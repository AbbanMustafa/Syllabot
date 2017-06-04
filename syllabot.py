import praw
import config
import courses
import time
import os


def login():
	r = praw.Reddit(username = config.username, #Creates Reddit instance
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = "SyllaBot v0.1")
	return r


def run_bot(r,comments_replied_to):
	for comment in r.subreddit('utaustin').comments(limit=25):

		if comment.id not in comments_replied_to and not comment.author == r.user.me():
			reader(comment,comments_replied_to)


def reader(comment,comments_replied_to):
		body = comment.body.upper()
		parsed = body.split()
		finComment = """I am SyllaBot and I am here to help you! The following are links to the syllabi of courses you mentioned:

		Course mentioned| Syllabus
		- | -"""
		commented = False


		for word in parsed:
		#for dept in courses.departments:
			if word in courses.departments:
				indx = parsed.index(word)
				courseNum = indx+1 #This assumes that the course number will always follow the department id

				if len(parsed[courseNum]) >=3 and len(parsed[courseNum]) <=4 and parsed[courseNum][0:3].isdigit():
					commented = True

					finComment += "\n"+parsed[indx]+" "+parsed[courseNum]+" | "+"[link](https://utdirect.utexas.edu/apps/student/coursedocs/nlogon/?semester=&department="+courses.departments[word]+"&course_number="+parsed[courseNum]+"&course_title=&unique=&instructor_first=&instructor_last=&course_type=In+Residence&search=Search)"

					comments_replied_to.append(comment.id)

					

				parsed.remove(word)


		if commented:
			comment.reply(finComment)
			with open ("repliedTo.txt","a") as file: # "a" means going to append to the file 
				file.write(comment.id+"\n")		

		print "Sleeping...."
		time.sleep(45)

def getPastComments():
	if not os.path.isfile("repliedTo.txt"):
		comments_replied_to = []
	else:
		with open("repliedTo.txt","r") as file:
			comments_replied_to = file.read()
			comments_replied_to = comments_replied_to.split("\n")
			comments_replied_to = filter(None, comments_replied_to)

	return comments_replied_to


r = login()
comments_replied_to = getPastComments()

while True:
	run_bot(r,comments_replied_to)

