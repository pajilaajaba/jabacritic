import React, { createContext, useState, useEffect, Children } from 'react';


export const AuthContext = createContext(); //виртуальная труба по которой текут даные
export const AuthProvider = ({children}) => {//children - это внутренности 
    const [token, setToken] = useState(null);
    const isAuthenticated = !!token; //true or false - на этой переменной для условного форматирования

    useEffect(() => {
        const storedToken = localStorage.getItem('access_token');
        if (storedToken) {
            setToken(storedToken);
        }
    }, []);
    //при логине токены сохраняются в localstorage и также в наш useState сохраняется access_token 
    const login = (accessToken, refreshToken) => {
        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);
        setToken(accessToken);
    }
    //просто удаляются токены и наш useState сбрасывается
    const logout = () =>{
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setToken(null);
    }

    return (
        <AuthContext.Provider value = {{token, isAuthenticated, login, logout}}>
            {children}
        </AuthContext.Provider>
    );
}