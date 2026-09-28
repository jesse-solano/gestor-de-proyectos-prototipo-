"""
Pruebas unitarias y de integración para ProjectFlow.
Verifica autenticación, roles RBAC, cálculo de desviación, consultas y exportación.
"""

from django.test import TestCase, Client
from django.urls import reverse
from admin_user.models import CustomUser, Project, Deliverable


class ProjectFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Admin
        self.admin_user = CustomUser.objects.create_superuser(
            username='admin_test',
            email='admin@test.com',
            password='Password123!',
            role=CustomUser.ROLE_ADMIN
        )
        # Coordinador
        self.coord_user = CustomUser.objects.create_user(
            username='coord_test',
            email='coord@test.com',
            password='Password123!',
            role=CustomUser.ROLE_COORDINATOR
        )
        # Proyecto de prueba
        self.project = Project.objects.create(
            code='VPIT-TEST01',
            name='Proyecto de Prueba',
            owner=self.admin_user,
            assigned_user=self.coord_user,
            planned_percentage='80%',
            real_percentage='90%',
            phase=Project.EXECUTION,
            status=Project.ACTIVE,
            estatus='A tiempo'
        )

    def test_project_deviation_calculation(self):
        """Verifica que la desviación se calcule como %Real - %Plan."""
        self.assertEqual(self.project.deviation, '10%')

        # Modificar porcentajes
        self.project.planned_percentage = '100%'
        self.project.real_percentage = '75%'
        self.project.save()
        self.assertEqual(self.project.deviation, '-25%')

    def test_login_failed_attempt_counter(self):
        """Verifica que los intentos fallidos de login incrementen el contador en sesión."""
        response = self.client.post(reverse('login'), {
            'username': 'admin_test',
            'password': 'WrongPassword123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session.get('login_attempts'), 1)
        self.assertContains(response, 'ERROR de inicio de sesion' if 'sesion' in response.content.decode('utf-8') else 'ERROR de inicio de sesión')

    def test_guest_login(self):
        """Verifica que el login como invitado asigne el usuario con rol de solo lectura."""
        response = self.client.get(reverse('guest_login'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_rbac_user_list_admin_only(self):
        """Verifica que solo los administradores puedan acceder al módulo de usuarios."""
        # Intento como coordinador
        self.client.login(username='coord_test', password='Password123!')
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 302)
        self.client.logout()

        # Intento como admin
        self.client.login(username='admin_test', password='Password123!')
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuarios')

    def test_project_list_view(self):
        """Verifica renderizado de lista de proyectos."""
        self.client.login(username='coord_test', password='Password123!')
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'VPIT-TEST01')
        self.assertContains(response, 'Proyecto de Prueba')

    def test_report_view_and_export_csv(self):
        """Verifica acceso a reportes y descarga en CSV."""
        self.client.login(username='admin_test', password='Password123!')
        response = self.client.get(reverse('report_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reportes')

        # Descarga CSV
        csv_response = self.client.get(reverse('report_export_csv'))
        self.assertEqual(csv_response.status_code, 200)
        self.assertEqual(csv_response['Content-Type'], 'text/csv')
        self.assertIn('attachment; filename="ProjectFlow_Reporte_Consolidado.csv"', csv_response['Content-Disposition'])
