#-*- coding:utf-8-*-
from openerp.tests import common
from faker import Faker
from openerp.osv import orm


class TestCourse(common.TransactionCase):

    def create_course(self, cr, uid, model_obj, max_number):
        """Metodo ayudante para crear cursos."""
        values = {'name': "Test Course", 'subject': 'Python', 'max_students': max_number}
        return model_obj.create(cr, uid, values)

    def create_students(self, cr, uid, model_obj, amount, course_id):
        """Metodo ayudante para crear estudiantes."""
        data_generator = Faker()
        res = []
        for student in range(amount):
            values = {'name': data_generator.first_name(), 'course_id': int(course_id)}
            res.append(model_obj.create(cr, uid, values)) #Vamos a devolver una lista de ids.
        return res

    def setUp(self):
        #Parte esencial de nuestra prueba. Estamos haciendo sobrecarga
        #del metodo setUp que OpenERP necesita llamar.
        super(TestCourse, self).setUp()

        #Voy a inicializar mi cursor y mi usuario de Openerp.
        #Esto es muy importante pues toda la API del ORM depende de ellos.
        cr, uid = self.cr, self.uid

        #Voy a llamar los modelos que quiero probar.
        self.course_obj = self.registry('course.course')
        self.student_obj = self.registry('student.student')

        #Crear la data de prueba, SI quiero usar ORM para esto.
        #Esta sera la data para mis pruebas positivas.
        self.course_id = self.create_course(cr, uid, self.course_obj, 5)
        self.create_students(cr, uid, self.student_obj, 3, self.course_id)

        #Esta sera la data para mis pruebas negativas
        self.bad_course_id = self.create_course(cr, uid, self.course_obj, 3)
        self.create_students(cr, uid, self.student_obj, 5, self.bad_course_id)


    #Vamos a crear una prueba muy sencilla, solo para que falle.
    def testModeloCreado(self):
        """Chequeamos que nuestro modelo existe de verdad y tiene datos."""
        cr, uid = self.cr, self.uid
        results = self.course_obj.search(cr, uid, [])
        self.assertTrue(results)


    def testRelacionarEstudiantesPorCurso(self):
        """Chequeamos que desde nuestro curso podemos llevar un control de
        estudiantes registrados."""
        cr, uid = self.cr, self.uid
        curso = self.course_obj.browse(cr, uid, self.course_id)
        self.assertTrue(curso.registered_students)

    def testCourseMaxStudents(self):
        """Chequeamos que nuestro curso tenga un numero maximo de estudaintes."""
        cr, uid = self.cr, self.uid
        curso = self.course_obj.browse(cr, uid, self.course_id)
        self.assertTrue(curso.max_students)

    def testRaiseExceptionAtNumberExceed(self):
        """Chequamos que levante una excepcion al infringir numero maximo."""
        cr, uid = self.cr, self.uid
        #Aqui no quiero usar mi data de curso valido, pues tendria que cambiarla
        #para solamente esta prueba. Es posible, pero es mejor crear otro curso
        #para que falle.
        self.assertRaises(orm.except_orm, self.course_obj.validate, cr, uid, [self.bad_course_id])

    def testValidateChangesStatus(self):
        """Queremos validar que nuestro metodo de validación modifique
        el registro en casos positivos."""
        cr, uid = self.cr, self.uid
        self.course_obj.validate(cr, uid, self.course_id)
        curso = self.course_obj.browse(cr, uid, [self.course_id])
        self.assertEqual('validated', curso.state)