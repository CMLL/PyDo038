#-*- coding: utf-8 -*-
from openerp.osv import orm, fields


class Course(orm.Model):

    _name = 'course.course'
    _columns = {
        'name': fields.char('Course Name', size=32, required=True),
        'subject': fields.char('Course Subject', size=32, required=True),
        'registered_students': fields.one2many('student.student', 'course_id',
                                               'Estudiantes Registrados'),
        'max_students': fields.integer('Cantidad Maxima', size=2, required=True),
        'state': fields.selection([('draft','Draft'),('validated','Validated')],
                                  'State')
    }

    _default = {
        'state': 'draft'
    }

    def validate(self, cr, uid, ids, context=None):
        """Asegura que los alumnos registrados no excedan la cantidad maxima"""
        for curso in self.browse(cr, uid, ids, context):
            registrados = len(curso.registered_students)
            if registrados > curso.max_students:
                raise orm.except_orm('ERROR', "Mas alumnos registrados que lo permitido.")
            else:
                self.write(cr, uid, curso.id, {'state': 'validated'}, context)