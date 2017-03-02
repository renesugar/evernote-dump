#!/usr/bin/env python
# -*- coding: utf-8 -*-

from helpers import *
import datetime

################
## Note Class ##
################

class Note(object):
    __EVERNOTE_DATE_FORMAT = "%Y%m%dT%H%M%SZ"
    def __init__(self):
        # Extracted
        self.__title = "CHANGE ME"
        self.__html = ""
        self.__created_date = ""
        self.__updated_date = ""
        self.__tags = []
        self.__attributes = {}
        self.__attr_latitude = None
        self.__attr_longitude = None
        self.__attr_altitude = None
        self.__attr_author = None
        # Resources/Attachments
        self.__attachments = []
        # Created
        self.__filename = ""
        self.__markdown = ""

    def add_attachment(self, attachment):
        self.__attachments.append(attachment)

    def append_html(self, text):
        self.__html += text
    
    def append_to_notemd(self, text):
        """Adds a new line of text to the markdown version of the note"""
        self.__notemd += "\n" + text

    def create_filename(self):
        self.__filename = self.__title[:100] + ".md"
        
    def finalize(self):
        """Output the note to a file"""

    def get_filename(self):
        return self.__filename

    def get_title(self):
        return self.__title

    def new_attachment(self, filename):
        self.__attachments.append(Attachment(filename))
        
    def set_created(self, date_string):
        """Converts a date in string format to a datetime"""
        self.__created_date = datetime.datetime.strptime(date_string, self.__EVERNOTE_DATE_FORMAT)
        

######################
## ATTACHMENT CLASS ##
######################

import base64
import mimetypes # Converts mime file types into an extension

class Attachment(object):
    def __init__(self):
        """Take in encrypted data, un-encrypt it, save to a file, gather attributes"""
        self.__filename = ""
        self.__mime = ""
        self.__base64data = ""
        self.__rawdata = ""
        self.__attributes = {}
    
    def add_found_attribute(self, attr, dataline):
        self.__attributes[attr] = dataline

    def create_filename(self, keep_file_names):
        base = ""
        extension = ""
        if self.__filename.count('.') >= 1:
            extension = self.__filename.split('.')[-1]
            base = self.__filename.rstrip('.' + extension)
        else:
            print(self.__mime)
            extension = mimetypes.guess_extension(self.__mime)
            extension = extension.replace('.jpe', '.jpg')
        
        if keep_file_names:
            # Limit filename length to 100 characters
            self.__filename = base[:100] + '.' + extension
        else:
            self.__filename = "somedate" # TODO

    def finalize(self, keep_file_names):
        self.create_filename(keep_file_names)
        self.decodeBase64()
        #TODO newFileName = checkForDouble(newFileName)    
        with open(makeDirCheck('Notes/media/') + self.__filename,'wb') as outfile:
            outfile.write(self.__rawdata)
        self.__rawdata = ""
        
    def get_extention(self, mimetype):
        if filename.count('.') >= 1:
            return '.' + filename.split('.')[-1]
        else:
            extension = mimetypes.guess_extension(mimetype)
            return extension.replace('.jpe', '.jpg')

    def data_stream_in(self, dataline):
        self.__base64data += dataline.rstrip('\n')
    
    def decodeBase64(self):
        ''' Decode base64 to memory '''
        try:
            self.__rawdata = base64.b64decode(self.__base64data)
            self.__base64data = ""
        except TypeError:
            raise SystemExit

    def set_filename(self, filename):
        self.__filename = filename

    def set_mime(self, mime):
        self.__mime = mime
