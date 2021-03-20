


const SearchResults = ({results}) => (
    <div className='w-11/12 mx-auto mt-5 flex flex-wrap'>
        {
            results.map(scene => (
                <div key={`${scene.ep}-${scene.srtidx}`} className='p-2'>
                    <img src={scene.img_url} title={scene.content} width="320" height="240 "/>
                </div>
            ))
        }
    </div>
);

export default SearchResults;
