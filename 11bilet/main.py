@app.route('/login', methods=['POST'])
def login():
    auth_data = request.get_json()
    username = auth_data.get('username')
    password = auth_data.get('password')

    # Проверка учетных данных
    if not username or not password or users.get(username) != password:
        return jsonify({'message': 'Неверный логин или пароль'}), 401

    # Генерация токена
    token = jwt.encode({
        'sub': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # Время действия токена
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token})



@app.route('/incidents/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    return jsonify({
        'message': f'Привет, {current_user}. Это защищённый ресурс.',
        'incidents': ['incident_1', 'incident_2']  # Пример данных
    })


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Извлекаем токен из заголовка Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]

        if not token:
            return jsonify({'message': 'Токен отсутствует'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Токен истёк'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Недопустимый токен'}), 401

        return f(current_user, *args, **kwargs)
    return decorated
