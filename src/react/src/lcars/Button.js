
const Button = ({className, onClick, disabled, children}) => (
    <button
        className={`bg-yellow-500 rounded-full font-bold text-black py-2 px-2 ${className}`}
        disabled={disabled}
        onClick={onClick}
    >
        {children}
    </button>
)

export default Button;
