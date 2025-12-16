import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

const RegisterPage = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [passwordConfirm, setPasswordConfirm] = useState('');

    const navigate = useNavigate(); //для навигации

    const handleSubmit = async (event) => { //чтобы страница не перезугржаалсь каждый раз
        event.preventDefault();

        if (password !== passwordConfirm) {alert("Пароли не совпадают"); return}

        try {
            await axios.post('/api/auth/register/', {//отправка данных по адресу
                "username":username, 
                "email": email,
                "password1": password,
                "password2": passwordConfirm
            })

            alert("Успешно! Теперь войдите.");
            navigate('/login');
        } catch (error) {
            console.error(error);
            
            
            // error.response - это ответ от сервера
            // error.response.data - это JSON с ошибками (например {"email": ["Занят"], "username": ["Занят"]})
            
            if (error.response && error.response.data) {
                // превращаем объект ошибок в строку
                const serverErrors = error.response.data;
                
                // проверяем конкретные поля 
                if (serverErrors.email) {
                    alert(`Ошибка Email: ${serverErrors.email[0]}`);
                } else if (serverErrors.username) {
                    alert(`Ошибка Имя пользователя: ${serverErrors.username[0]}`);
                } else if (serverErrors.password) {
                    alert(`Ошибка Пароль: ${serverErrors.password[0]}`);
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
                <h2 className="text-2xl font-bold mb-6 text-center">Регистрация</h2>
                    <form onSubmit={handleSubmit} className = "flex flex-col gap-4">
                        <input
                            type = 'text'
                            placeholder='Введите имя пользователя'
                            className = 'p-2 border rounded'
                            value = {username} 
                            onChange={e => setUsername(e.target.value)}
                        />
                        <input
                            type = 'email'
                            placeholder='Введите email'
                            className = 'p-2 border rounded'
                            value = {email} 
                            onChange={e => setEmail(e.target.value)}
                        />
                        <input
                            type = 'password'
                            placeholder='Введите пароль'
                            className = 'p-2 border rounded'
                            value = {password} 
                            onChange={e => setPassword(e.target.value)}
                        />
                        <input
                            type = 'password'
                            placeholder='Введите пароль повторно'
                            className = 'p-2 border rounded'
                            value = {passwordConfirm} 
                            onChange={e => setPasswordConfirm(e.target.value)}
                        />
                        <button type="submit" className="bg-blue-600 text-white p-2 rounded hover:bg-blue-700">
                            Создать аккаунт
                        </button>
                    </form> 

                <p className="mt-4 text-center text-sm">
                    Уже есть аккаунт? <Link to="/login" className="text-blue-500">Войти</Link>
                </p>
            </div>
        </div>
    );
};


export default RegisterPage;