from globaleaks.utils import log, gltime
from globaleaks.plugins.base import FileProcess
from magic import Magic

class TypeValidation(FileProcess):

    def __init__(self):
        self.plugin_name = u'File type validation'
        self.plugin_type = u'fileprocess'
        self.plugin_description = "Validate a submitted file inquiring the file type"

        # this is not the right fields description, because would contain also
        # the 'order' of representation, the 'description' and the 'required' boolean flag
        self.admin_fields = {'whitelist' : 'text', 'blacklist': 'text' }
        self.receiver_fields = None

    def validate_admin_opt(self, admin_fields):
        return True

    def do_fileprocess(self, filepath, admin_fields):

        magic_file_check =  Magic()

        print "Type Validation plugin: checking %s", filepath
        print "and is...", magic_file_check.id_filename(filepath)

        return True # Accept


