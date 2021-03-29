

const LCARSBar = ({msg}) => (
    <div className="flex h-9 w-full">
        <div className="bg-purple-400 mr-2 w-1/5" />
        <div className="bg-yellow-500 mr-2 w-10" />
        <div className="bg-purple-400 mr-2 w-1/6" />
        <div className="bg-purple-400 mr-2 flex-grow" />
        {
            msg &&
            <div className="hidden md:block md:text-3xl lg:text-4xl ml-5 mr-5 text-yellow-500 ">
                {msg}
            </div>
        }
        <div className="bg-purple-400 mr-2 w-10 rounded-r-full" />
    </div>
);

export default LCARSBar;
