import axios from 'axios';

const api = axios.create({
    baseURL:'/api/v1',
    headers: {'Content-Type':'application/json'}
    });

//перехватчик - чтобы добавлять каждый раз в заголовки нашщ токен - чтобы бэк понимал что мы зареганы
api.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token");
    if (!!token) {
        config.headers.Authorization = `Bearer ${token}`}
    return config
})


//перехватчик ответа - здесь написан чтобы не допустить ошибки 401
api.interceptors.response.use(
    (response) => {
        return response; // если успех, просто возвращаем данные
    },
    async (error) => {
        // запоминаем оригинальный запрос, который упал
        const originalRequest = error.config;

        // проверяем:
        // 1. Ошибка 401 (Нет прав)
        // 2. И мы еще НЕ пробовали его повторить (чтобы не было бесконечного цикла)
        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            
            originalRequest._retry = true; // ставим метку "Мы уже пробовали чинить"

            try {
                //достаем Refresh токен
                const refreshToken = localStorage.getItem('refresh_token');
                
                //делаем запрос на обновление
                const response = await axios.post('/api/auth/refresh/', {
                    refresh: refreshToken
                });

                //если сервер дал добро -> сохраняем новый токен
                const newAccessToken = response.data.access;
                localStorage.setItem('access_token', newAccessToken);

                //меням токен в заголовке старого запроса
                originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

                //повторяем старый запрос с новым токеном
                return api(originalRequest);

            } catch (refreshError) {
                //если даже Refresh токен протух (или его нет) -> Выход
                console.error("Сессия истекла. Пожалуйста, войдите снова.");
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/login'; 
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);
export default api;