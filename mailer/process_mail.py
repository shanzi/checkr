#!/usr/bin/env python
# encoding: utf-8

import re

from mailer.imbox import Imbox
from mailer.mailsender import MailSender
from mailer import mail_settings as settings

from datetime import datetime, timedelta
from submission.models import Submission, Email, File
from assignment.models import Assignment
from student.models import Student

import zipfile
from mailer import rarfile

ASSIGNMENT_RE = re.compile(r'^"?(\d{10})[-_](\d+)\.(zip|rar)"?$')
FILE_EXT_RE = re.compile(r'\.(h|cpp|cxx|c|txt)$')

def _unicode(str_, encoding_list):
    if isinstance(str_, unicode): return str_
    for encoding in encoding_list:
        try:
            return unicode(str_, encoding)
        except UnicodeDecodeError as e:
            continue

    return unicode(str_)


class Result(object):
    def __init__(self, uid, message):
        self.attachment = False
        self.attachment_name_split = False
        self.overdeadline = False
        self.badattachments = False
        self.error = False
        self.message = message
        self.uid = uid

    @property
    def ok(self):
        return bool(self.attachment_name_split)

    def _save_email(self, submission):
        message = self.message
        email = Email()
        email.fromaddr = ', '.join([addr['email'] for addr in self.message.sent_from])
        email.toaddr = ', '.join([addr['email'] for addr in self.message.sent_to])
        email.subject = self.message.subject
        email.content = '\n\n'.join(self.message.body['plain'] or self.message.body['html'])
        email.attachment_title = self.attachment['filename']
        email.sent_at = self.message.date
        email.submission = submission
        email.save()

    def _zip_files(self):
        zf = zipfile.ZipFile(self.attachment['content'],allowZip64=True)
        infolist = zf.infolist()
        for info in infolist:
            yield info.filename, zf.read(info)

    def _rar_files(self):
        rf = rarfile.RarFile(self.attachment['content'])
        infolist = rf.infolist()
        for info in infolist:
            if not info.isdir():
                yield info.filename, rf.read(info)

    def _save_files(self, submission, ext):
        if ext=='zip':
            files = self._zip_files()
        else:
            files = self._rar_files()
        for fname, content in files:
            if FILE_EXT_RE.search(fname):
                content = _unicode(content, ['utf-8', 'gbk'])
            else:
                content = '[No Preview]'
            file_obj = File()
            file_obj.filename = fname
            file_obj.content = content
            file_obj.submission = submission
            file_obj.save()

    def _submit(self):
        stu_num, seq, ext = self.attachment_name_split
        student = Student.objects.get(student_num=stu_num)
        assignment = Assignment.objects.get(sequence=seq)
        submission = Submission()
        submission.student = student
        submission.assignment = assignment
        submission.score = 2
        submission.save()

        self._save_email(submission)

        try:
            self._save_files(submission, ext)
        except zipfile.BadZipfile as e:
            self.badattachments = True
            return False
        except rarfile.BadRarFile as e:
            self.badattachments = True
            return False

        return True



    def submit(self):
        if not self.ok: return False
        try:
            return self._submit()
        except Exception as e:
            raise e
            self.error = True
            return False

    def message(self):
        pass

def _mail_reciever():
    receiver = settings.RECEIVER
    server = receiver['server']
    ssl = receiver['ssl']
    account = settings.ACCOUNT

    return Imbox(server,
            username=account['username'],
            password=account['password'],
            ssl=ssl)

def _mail_sender():
    sender = settings.sender
    server = sender['sender']
    ssl = sender['ssl']
    account = settings.ACCOUNT
    return MailSender(server,
            username=account['username'],
            password=account['password'],
            ssl=ssl)

def _is_homework(message):
    from_ = message.sent_from[0]['email']
    if from_.strip() in settings.IGNORED_EMAILS:
        return False
    if not message.attachments:
        return False

    subject = _unicode(message.subject, ['utf-8', 'gbk'])
    content = message.body['plain'] or message.body['html']
    if content: 
        content = _unicode(content[0], ['utf-8', 'gbk'])
    else:
        content = u''

    score = 1

    if subject.find('作业'.decode('utf-8')) >= 0: score *= 0.5
    if subject.find('数据结构'.decode('utf-8')) >= 0: score *= 0.8
    if content.find('作业'.decode('utf-8')) >= 0: score *= 0.5
    if content.find('数据结构'.decode('utf-8')) >= 0: score *= 0.8
    if message.attachments: 
        attachment = message.attachments[0]
        if attachment:
            filename = attachment['filename']
            if ASSIGNMENT_RE.match(filename): score *= 0.4


    return score < 0.5

def _process_message(uid, message):
    result = Result(uid, message)
    if not message.attachments: return result

    attachment = message.attachments[0]
    result.attachment = attachment

    filename = attachment['filename']
    match = ASSIGNMENT_RE.match(filename.strip())
    if not match: return result

    result.attachment_name_split = match.groups()
    return result


def process_mail():
    receiver = _mail_reciever()
    date = datetime.now() - timedelta(2)
    results = []
    with receiver:
        date_str = date.strftime('%d-%b-%Y')
        for uid, message in receiver.messages(folder=settings.DEFAULT_MAILBOX,
                date__gt=date_str):
            print "processing:(%s) %s" % (uid, message.subject)
            if not _is_homework(message): continue 

            res = _process_message(uid, message)
            results.append(res)

        for uid, message in receiver.messages(folder=settings.WAIT_MAILBOX):
            res = _process_message(uid, message)
            results.append(res)

        receiver.connection.select()
        for result in results:
            ok = result.submit()
            if ok: receiver.move(result.uid, settings.PROCESSED_MAILBOX)
            elif result.error:
                receiver.move(result.uid, settings.ERROR_MAILBOX)

