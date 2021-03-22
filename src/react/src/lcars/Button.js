
const Button = ({className, onClick, children}) => (
    <button
        className={`bg-yellow-500 rounded-full font-bold text-black py-2 px-10 ${className}`}
        onClick={onClick}
    >
        {children}
    </button>
)

export default Button;
