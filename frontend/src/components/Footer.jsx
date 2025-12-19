import React from 'react';

const Footer = () => {
    return (
        <footer className="bg-gray-900 text-gray-400 py-8 mt-auto">
            <div className="container mx-auto px-4 text-center">
                <h3 className="text-white text-lg font-bold mb-2">JabaCritic 🐸</h3>
                <p className="text-sm mb-4">Играй, получай удовольствие и расскажи о нем!</p>
                
                <div className="border-t border-gray-700 my-4 w-1/3 mx-auto"></div>
                
                <p className="text-xs">
                    &copy; {new Date().getFullYear()} JabaCritic Inc. Все права защищены. <br/>
                    Created by <span className="text-green-500">pajilaajaba</span>.
                </p>
            </div>
        </footer>
    );
};

export default Footer;