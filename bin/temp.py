from email import message
import smtplib

FROM = "hale-terminal@outlook.com"

TO = ["halea2196@gmail.com"]

SUBJECT = "Password reset"

TEXT = "Reset your password"

message = """\
From: %s
To: %s
Subject: %s

%s
""" % (
    FROM,
    ", ".join(TO),
    SUBJECT,
    TEXT,
)

server = smtplib.SMTP("localhost")
server.sendmail(FROM, TO, message)
server.quit()
