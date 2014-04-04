#-*- coding: utf-8 -*-
from openerp.osv import orm, fields


class Student(orm.Model):

    _name = 'student.student'
    _columns = {
        'name': fields.char('Nombre Estudiante', required=True, size=32),
        'course_id': fields.many2one('course.course', 'Curso')
    }