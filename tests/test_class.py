#-*- coding:utf-8-*-
from openerp.tests import common
from faker import Faker


class TestCourse(common.TransactionCase):

    def create_course(self, cr, uid, model_obj):
        """Metodo ayudante para crear cursos."""
        values = {'name': "Test Course", 'subject': 'Python'}
        return model_obj.create(cr, uid, values)

    def create_students(self, cr, uid, model_obj, amount, course_id):
        """Metodo ayudante para crear estudiantes."""
        data_generator = Faker()
        res = []
        for student in range(amount):
            values = {'name': data_generator.first_name(), 'course_id': course_id}
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
        self.student_obj = self.registry('course.student')

        #Crear la data de prueba, SI quiero usar ORM para esto.
        self.course_id = self.create_course(cr, uid, self.course_obj)
        self.student_ids = self.create_students(cr, uid, self.student_obj, 3,
                                                self.course_id)


    #Vamos a crear una prueba muy sencilla, solo para que falle.
    def testModeloCreado(self):
        """Chequeamos que nuestro modelo existe de verdad y tiene datos."""
        cr, uid = self.cr, self.uid
        results = self.course_obj.search(cr, uid, [])
        self.assertTrue(results)


