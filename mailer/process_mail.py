#!/usr/bin/env python
# encoding: utf-8

import re

from mailer.imbox import Imbox
from mailer.mailsender import MailSender
from mailer import mail_settings as settings

from datetime import datetime, timedelta
from submission.models import Submission, Email, File
from assignment.models import Assignment, seq_descriptions
from student.models import Student

import zipfile
from mailer import rarfile

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
        if not self.attachment_name_split:
            self._detect_info()
        if self.attachment_name_split:
            sn, seq, ext = self.attachment_name_split
            return (sn and seq and ext)
        return False

    def _detect_info(self):
        stu_num, seq, ext = None, None, None
        subject = self.message.subject
        content = _unicode(
                '\n\n'.join(self.message.body['plain'] or self.message.body['html']),
                ['utf-8','gbk'])
        if self.attachment:
            attachment_title = self.attachment['filename']
        else:
            return
        if re.search(r'\.zip"?$', attachment_title):
            ext = 'zip'
        elif re.search(r'\.rar"?$', attachment_title):
            ext = 'rar'
        elif self.attachment['content-type']=='application/octet-stream':
            ext = 'rar'
        elif self.attachment['content-type']=='application/zip':
            ext = 'zip'
        else:
            return
        str_ = subject + content + attachment_title
        match = re.search(ur'(\D|$)(\d{10})(\D|$)', str_, re.M)
        if not subject: import pdb;pdb.set_trace()
        if match:
            groups = match.groups()
            stu_num = groups[1]
        match = re.search(unicode(r'第(.+?)(次|周|章)(作业)?', 'utf-8'), str_, re.M)
        if not match: 
            match = re.search(r'ch(\d+)', str_, re.M)
        if match:
            num = match.groups()[0].strip()
            if num.isdigit():
                seq = num
            else:
                try:
                    num = seq_descriptions.index(num.encode('utf-8'))
                    seq = num + 1
                except ValueError as e:
                    seq = 1
        else:
            seq = 1
        if stu_num and seq and ext:
            self.attachment_name_split = (stu_num, seq, ext)


    def _save_email(self, submission):
        message = self.message
        email = Email()
        email.fromaddr = ', '.join([addr['email'] for addr in self.message.sent_from])
        email.toaddr = ', '.join([addr['email'] for addr in self.message.sent_to])
        email.subject = self.message.subject or '(no subject)'
        email.content = _unicode(
                '\n\n'.join(self.message.body['plain'] or self.message.body['html']),
                ['utf-8','gbk'])
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
            file_obj.filename = _unicode(fname, ['utf-8', 'gbk'])
            file_obj.content = content
            file_obj.submission = submission
            file_obj.save()

    def _submit(self):
        print 'submitting: %s' % self.message.subject
        stu_num, seq, ext = self.attachment_name_split
        student = Student.objects.get(student_num=stu_num)
        assignment = Assignment.objects.get(sequence=seq)
        try:
            submission = Submission.objects.get(
                    student=student,
                    assignment=assignment)
        except Exception as e:
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
            raise e
        except rarfile.BadRarFile as e:
            self.badattachments = True
            raise e

        return True

    def submit(self):
        if not self.ok: return False
        try:
            return self._submit()
        except Exception as e:
            self.error = True
            print 'error: [%s] %s' % (self.message, e)
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
    sender = settings.SENDER
    server = sender['server']
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
            if re.match(r'^"?\[?(\d{10})\]?[-_]\[?(\d+)\]?\.(zip|rar)"?$', filename): score *= 0.4


    return score < 0.5

def parse_attachments_name(name):
    name = name.strip()
    match = re.match(r'^"?\[?(\d{10})\]?[-_]\[?(\d+)\]?\.(zip|rar)"?$', name)
    if match: return match.groups()
    match = re.match(r'^"?(\d)[-_](\d{10})\.(zip|rar)"?$', name) 
    if match:
        seq, stn, ext = match.groups()
        return (stn, seq, ext)
    match = re.match(r'^"?(\d{10})[-_+]?(ch|chapter)\.?(\d)"?$', name)
    if match:
        sn, _, seq, ext = match.groups()
        return (sn, seq, ext)

def _process_message(uid, message):
    result = Result(uid, message)
    if not message.attachments: return result

    attachment = message.attachments[0]
    result.attachment = attachment

    filename = attachment['filename']

    result.attachment_name_split = parse_attachments_name(filename)
    return result


def process_mail():
    receiver = _mail_reciever()
    date = datetime.now() - timedelta(20)
    results = []
    with receiver:
        date_str = date.strftime('%d-%b-%Y')
        for uid, message in receiver.messages(folder=settings.DEFAULT_MAILBOX,
                date__gt=date_str):
            ishw =  _is_homework(message)
            print "processing:(%s) %s [%s]" % (uid, message.subject, ishw)
            if not ishw: continue

            res = _process_message(uid, message)
            results.append(res)

        receiver.connection.select()
        for result in results:
            ok = result.submit()
            if ok: receiver.move(result.uid, settings.PROCESSED_MAILBOX)
            elif result.error:
                receiver.move(result.uid, settings.ERROR_MAILBOX)

        for uid, message in receiver.messages(folder=settings.WAIT_MAILBOX):
            print "processing:(%s) %s [wait box]" % (uid, message.subject,)
            res = _process_message(uid, message)
            results.append(res)

        receiver.connection.select(settings.WAIT_MAILBOX)
        for result in results:
            ok = result.submit()
            if ok: receiver.move(result.uid, settings.PROCESSED_MAILBOX)
            elif result.error:
                receiver.move(result.uid, settings.ERROR_MAILBOX)
