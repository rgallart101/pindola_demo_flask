from app import create_app, db
from app.models import User

def run():
    app = create_app()
    # disable CSRF for test client posts
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        u = User.query.filter_by(username='testuser').first()
        if not u:
            u = User(username='testuser', email='testuser@example.com')
            u.set_password('testpass')
            db.session.add(u)
            db.session.commit()

    with app.test_client() as client:
        client.get('/set-locale/ca')
        client.post('/login', data={'username':'testuser','password':'testpass'}, follow_redirects=True)
        r = client.get('/change-password', follow_redirects=True)
        data = r.data.decode('utf-8')
        print('status', r.status_code)
        print('Has "Canviar contrasenya"?', 'Canviar contrasenya' in data)
        print('Has "Contrasenya"?', 'Contrasenya' in data)
        # Print heading context
        start = data.find('<h2')
        if start != -1:
            print('\n---- heading html ----')
            print(data[start:start+200])
            print('----------------------\n')

if __name__ == '__main__':
    run()
