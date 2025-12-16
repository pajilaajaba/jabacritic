import React, { useContext, useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const navigate = useNavigate(); //для навигации
    const {login} = useContext(AuthContext);

    const handleSubmit = async (event) => { //чтобы страница не перезугржаалсь каждый раз
        event.preventDefault();
        
        try {
            const response = await axios.post('/api/auth/login/', {//отправка данных по адресу
                "username":username, 
                "password": password,
            })
            login(response.data.access, response.data.refresh); //вызов функции логик для занесения этого в loacalstorage
            alert("Вы успешно вошли на JABACRITIC!");
            navigate('/');
        } catch (error) {
            console.error(error);

            if (error.response && error.response.data) {
                // превращаем объект ошибок в строку
                const serverErrors = error.response.data;
                if (serverErrors.username) {
                    alert(`Ошибка Имя пользователя: ${serverErrors.username[0]}`);
                } else if (serverErrors.password) {
                    alert(`Ошибка Пароль: ${serverErrors.password[0]}`);
                }else if (serverErrors.detail) {
                    alert(`Неверный пароль!`);
                } else {
                    // если ошибка общая или непонятная - глупая
                    alert("Ошибка регистрации: " + JSON.stringify(serverErrors));
                }
            } else {
                alert("Произошла неизвестная ошибка сети");
            }
        }
    }
    //ниже под каждым текстовым вводом - такая логика - при каждом изменении текста, мы автоматически сразу заносим этот текст в value
    return (
        <div className="flex justify-center items-center h-screen bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-md w-96">
                <h2 className="text-2xl font-bold mb-6 text-center">Вход</h2>
                    <form onSubmit={handleSubmit} className = "flex flex-col gap-4">
                        <input
                            type = 'text'
                            placeholder='Введите имя пользователя'
                            className = 'p-2 border rounded'
                            value = {username} 
                            onChange={e => setUsername(e.target.value)}
                        />
                        <input
                            type = 'password'
                            placeholder='Введите пароль'
                            className = 'p-2 border rounded'
                            value = {password} 
                            onChange={e => setPassword(e.target.value)}
                        />
                        <button type="submit" className="bg-blue-600 text-white p-2 rounded hover:bg-blue-700">
                            Войти
                        </button>
                    </form> 

                <p className="mt-4 text-center text-sm">
                    Нет аккаунта?  <Link to="/register" className="text-blue-500">Зарегистрироваться</Link>
                </p>
            </div>
        </div>
    );
};


export default LoginPage;