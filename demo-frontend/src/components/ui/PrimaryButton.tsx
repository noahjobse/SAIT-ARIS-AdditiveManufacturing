import React from "react";

type PrimaryButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
    children: React.ReactNode;
};

function PrimaryButton({ children, className = "", type = "button",...props }: PrimaryButtonProps) {
    return (
        <button 
            className={
                `bg-linear-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white text-sm sm:text-md font-medium px-6 py-2 rounded-md transition-all outline-none cursor-pointer border-none flex flex-row justify-center items-center shadow-lg shadow-orange-500/20 
                ${className}`
            }
            type={type}
            {...props}
        >
            {children}
        </button>
    );
}

export default PrimaryButton;