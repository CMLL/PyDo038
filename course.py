#-*- coding: utf-8 -*-
from openerp.osv import orm, fields


class Course(orm.Model):

    _name = 'course.course'
    _columns = {
        'name': fields.char('Course Name', size=32, required=True),
        'subject': fields.char('Course Subject', size=32, required=True)
    }