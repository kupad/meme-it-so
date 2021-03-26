
const Button = ({className, onClick, disabled, children}) => (
    <button
        className={`bg-yellow-500 rounded-full text-xl text-black py-2 px-6 ${className}`}
        disabled={disabled}
        onClick={onClick}
    >
        {children}
    </button>
)

export default Button;
