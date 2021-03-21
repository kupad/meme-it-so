import { Link } from "react-router-dom";

const SearchResults = ({results, onClick}) => {
    const key = (scene) => {
        return `${scene.ep}-${scene.srtidx}`;
    }

    return (
        <div className='flex flex-wrap'>
            {
                results.map(scene => (
                    <Link
                        key={key(scene)}
                        to={`/scene/ep/${scene.ep}/${scene.start}`}
                        className='p-2'
                    >
                        <img src={scene.img_url} title={scene.content} alt={key(scene)} width="320" height="240" />
                    </Link>
                ))
            }
        </div>
    );
};

export default SearchResults;
