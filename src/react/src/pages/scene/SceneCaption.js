const SceneCaption = ({prev, curr, next}) => {
    if(!curr)
        return <div className="h-32"></div>

    return (
        <div className="mt-10">
            <pre className='text-white text-opacity-50'>{prev}</pre>
            <pre>{curr}</pre>
            <pre className='text-white text-opacity-50'>{next}</pre>
        </div>
    )
}

export default SceneCaption;
