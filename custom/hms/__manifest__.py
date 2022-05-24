{
    'name': "HMS module",
    'summary': "HMS (Hospitals Management System)",
    'description': 'HMS (Hospitals Management System)',
    'author': "Nermeen",
    'website': "http://to.nermeen.com",
    'category': 'Uncategenized',
    'version ': '1.0',
    'depends': ['crm'],
    'templates': [
        'templates/hospital_patient.xml',
        'templates/hospital_department.xml',
        'templates/hospital_doctor.xml',
        'templates/crm_customers_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
