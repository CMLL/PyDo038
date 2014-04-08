#-*- coding: utf-8 -*-
from openerp.osv import orm, fields


class Course(orm.Model):

    _name = 'course.course'
    _columns = {
        'name': fields.char('Course Name', size=32, required=True),
        'subject': fields.char('Course Subject', size=32, required=True),
        'registered_students': fields.one2many('student.student', 'course_id',
                                               'Estudiantes Registrados'),
        'max_students': fields.integer('Cantidad Maxima', size=2, required=True)
    }